"""Interface de campanha e adaptação do duelo original para PvE."""
import tkinter as tk
from tkinter import ttk, messagebox
from interface import MedievalBattleGUI
from personagem import CLASSES_DISPONIVEIS
from equipe import SAVE, COMPANHEIROS, CONVERSAS, PARES
from reliquias import Campanha, CATALOGO, POR_DISTRITO, chance_raro, CHANCE_ARTEFATO
from audio import Audio, contexto, TRILHAS, fonte
from masmorras import MASMORRAS, inimigo_onda, PADROES_CHEFE, acao_chefe
from expansao import ITENS, MERCADOS, EVENTOS, NPCS
from pathlib import Path
from mundo import DISTRITOS, POR_SIGNO, CLASSES_MUNDO, RECEITAS, FACCOES, DIALOGOS

class RPG(MedievalBattleGUI):
    def __init__(self,root):
        self.transicoes=[]; self.audio=Audio(); self.aviso=None; self.falas_locais={}; self.imagens={}; self.c=None; self.modo='menu'; self.ai_job=None; self.arma_usada=False; self.perguntas={}
        super().__init__(root)
        # Reserve espaço para a barra de tarefas e a moldura da janela.
        largura=max(1,root.winfo_screenwidth()-32); altura=max(1,root.winfo_screenheight()-100)
        root.minsize(min(950,largura),min(540,altura))
        root.geometry(f'{min(1240,largura)}x{min(880,altura)}+8+8')
        root.title('The Battle - A Conjunção Dos Doze (V5.2)')
        try: root.iconbitmap(str(__import__('pathlib').Path(__file__).with_name('icon.ico')))
        except tk.TclError: pass
        root.protocol('WM_DELETE_WINDOW',self.sair)
        self.menu()
    def sair(self):
        if self.c:
            try: self.c.salvar()
            except OSError as e:
                if not messagebox.askyesno('Erro ao salvar',f'{e}\nSair mesmo assim?'): return
        if self.ai_job: self.root.after_cancel(self.ai_job)
        self.cancelar_transicoes(); self.audio.parar(); self.root.destroy()
    def cancelar_transicoes(self):
        for job in self.transicoes:
            self.root.after_cancel(job)
        self.transicoes.clear()
    def _limpar_tela(self):
        self.cancelar_transicoes()
        super()._limpar_tela()
    def label(self,parent,txt,size=11,color=None,**kw):
        return tk.Label(parent,text=txt,bg=parent.cget('bg'),fg=color or self.FG_TEXTO,font=('Segoe UI',size),**kw)
    def botao(self,parent,txt,cmd,**kw):
        opt=dict(bg='#49382b',fg=self.FG_TEXTO,activebackground='#6b5035',activeforeground='white',disabledforeground='#91877a',relief='flat',font=('Segoe UI',10,'bold'),padx=12,pady=7,cursor='hand2',wraplength=640,justify='left')
        opt.update(kw); return tk.Button(parent,text=txt,command=cmd,**opt)
    def heading(self,parent,txt,size=22):
        self.label(parent,txt,size,self.FG_TITULO,anchor='w').pack(fill='x',pady=(0,8))
    def menu(self):
        self.modo='menu'; self.audio.tocar('menu'); self._limpar_tela()
        f=tk.Frame(self.root,bg=self.BG_FUNDO,padx=35,pady=45); f.pack(expand=True)
        self.heading(f,'THE BATTLE',36); self.heading(f,'A Conjunção dos Doze',24)
        self.label(f,'Uma cidade. Doze distritos. Uma noite para decidir quem terá poder sobre todos.',12,wraplength=650,justify='left').pack(pady=18)
        for txt,cmd in [('Nova campanha',self.criacao),('Continuar campanha',self.carregar),('Duelo local — modo original',self.arena),('Guia de jogo',self.guia),('Áudio e créditos',lambda:self.config_audio(self.menu)),('Sair',self.sair)]:
            b=self.botao(f,txt,cmd); b.pack(fill='x',pady=4)
            if txt=='Continuar campanha' and not SAVE.exists(): b.config(state='disabled')
    def arena(self):
        self.modo='arena'; self.audio.tocar('menu'); super()._construir_tela_criacao()
        self.botao(self.root,'Voltar ao menu',self.menu).pack(pady=4)
    def _construir_tela_criacao(self):
        if self.modo=='arena': self.arena()
        else: self.menu()
    def carregar(self):
        try: self.c=Campanha.carregar(); self.perguntas={k:set(v) for k,v in self.c.perguntas.items()}; self.modo='campanha'; self.mundo() if self.c.prologo else self.prologo()
        except (OSError,ValueError,KeyError,TypeError) as e: messagebox.showerror('Salvamento',str(e))
    def salvar(self):
        try: self.c.salvar()
        except OSError as e: messagebox.showerror('Salvamento',str(e))
    def painel_rolavel(self,parent,bg,padx=0,pady=0):
        """Painel com largura ajustável e barra de rolagem independente."""
        canvas=tk.Canvas(parent,bg=bg,highlightthickness=0,width=1,height=1)
        scroll=ttk.Scrollbar(parent,orient='vertical',command=canvas.yview)
        canvas.configure(yscrollcommand=scroll.set)
        scroll.pack(side='right',fill='y'); canvas.pack(side='left',fill='both',expand=True)
        frame=tk.Frame(canvas,bg=bg,padx=padx,pady=pady)
        wid=canvas.create_window((0,0),window=frame,anchor='nw')
        frame.bind('<Configure>',lambda e:canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.bind('<Configure>',lambda e:canvas.itemconfigure(wid,width=e.width))
        return frame,canvas
    def rolagem_mouse(self,*areas):
        def scroll_active(e):
            for pane,canvas in areas:
                if not canvas.winfo_exists(): continue
                if e.widget is pane or str(e.widget).startswith(str(pane)+'.'):
                    if e.num==4: delta=-3
                    elif e.num==5: delta=3
                    else: delta=-int(e.delta/120)*3 or (-1 if e.delta>0 else 1 if e.delta<0 else 0)
                    canvas.yview_scroll(delta,'units'); return 'break'
        for ev in ('<MouseWheel>','<Button-4>','<Button-5>'): self.root.bind(ev,scroll_active)
    def criacao(self):
        if SAVE.exists() and not messagebox.askyesno('Nova campanha','Uma nova campanha substituirá o salvamento existente. Continuar?'): return
        self._limpar_tela()
        outer=tk.Frame(self.root,bg=self.BG_FUNDO,padx=24,pady=12); outer.pack(fill='both',expand=True)
        self.heading(outer,'Criação de personagem')
        footer=tk.Frame(outer,bg=self.BG_FUNDO); footer.pack(side='bottom',fill='x',pady=(10,0))
        pane=tk.Frame(outer,bg=self.BG_CARD); pane.pack(fill='both',expand=True)
        f,canvas=self.painel_rolavel(pane,self.BG_CARD,18,12); self.rolagem_mouse((pane,canvas))
        self.label(f,'Nome',12).pack(anchor='w'); nome=tk.Entry(f,font=('Segoe UI',13)); nome.insert(0,'Aventureiro'); nome.pack(fill='x',pady=5)
        self.label(f,'Classe — os bônus e atributos são os do duelo original.',12).pack(anchor='w',pady=(12,0))
        classe=ttk.Combobox(f,values=list(CLASSES_DISPONIVEIS),state='readonly'); classe.set('Guerreiro'); classe.pack(fill='x',pady=5)
        info=self.label(f,'',11,wraplength=800,justify='left'); info.pack(anchor='w')
        self.label(f,'Distrito de origem — qualquer classe pode nascer em qualquer distrito.',12).pack(anchor='w',pady=(15,0))
        origem=ttk.Combobox(f,values=[f'{d.signo} | {d.nome} — {d.povo}' for d in DISTRITOS],state='readonly'); origem.current(0); origem.pack(fill='x',pady=5)
        lore=self.label(f,'',11,wraplength=800,justify='left'); lore.pack(anchor='w',pady=10)
        preview=tk.Label(f,bg=self.BG_CARD); preview.pack(anchor='w')
        def ajustar_texto(e):
            for label in (info,lore): label.configure(wraplength=max(200,e.width-42))
        canvas.bind('<Configure>',ajustar_texto,add='+')
        def update(*_):
            cl=classe.get(); d=DISTRITOS[origem.current()]; preview.config(image=self.imagem(f'portrait_{origem.current()}_calm',True)); info.config(text=CLASSES_DISPONIVEIS[cl]['descricao']+'\nVantagem: '+CLASSES_MUNDO[cl][0]+'\nLimitação: '+CLASSES_MUNDO[cl][1]); lore.config(text=d.regiao+'\n'+d.lore+'\nSua linhagem cultural: '+d.povo+' (sem modificador racial de status).')
        classe.bind('<<ComboboxSelected>>',update); origem.bind('<<ComboboxSelected>>',update); update()
        def start():
            if classe.get() not in CLASSES_DISPONIVEIS or not 0<=origem.current()<len(DISTRITOS):
                messagebox.showwarning('Criação','Escolha uma classe e um distrito válidos.',parent=self.root); return
            try:
                nova=Campanha(nome.get().strip()[:50] or 'Aventureiro',classe.get(),DISTRITOS[origem.current()].signo)
                nova.salvar()
            except (OSError,ValueError) as e:
                messagebox.showerror('Criação de personagem',f'Não foi possível iniciar a campanha:\n{e}\nVerifique o acesso à pasta de salvamento e tente novamente.',parent=self.root); return
            self.perguntas={}; self.c=nova; self.modo='campanha'; self.prologo()
        self.botao(footer,'Voltar',self.menu).pack(side='left')
        self.botao(footer,'Começar a história',start).pack(side='right')
        self.label(footer,'Role o painel acima para ler toda a origem.',10,self.FG_MUTED).pack(side='left',padx=12)
    def guia(self):
        self.popup('Guia de jogo', '''[!] História / caso local — converse, escolha uma solução e obtenha provas.\n[?] Arquivo — leia a história do bairro; registre no diário.\n[+] Oficina — trabalhe até duas vezes por distrito, receba materiais e moedas; fabrique armas.\n[→] Mapa — viaje livremente entre os 12 distritos. Nenhuma classe é bloqueada.\n[✓] Caso resolvido.\n\nFICHA ORIGINAL\nForça: ataque físico e dano. Defesa: oposição a ataques. Agilidade: afinidade mágica, mana e ataque rápido. Vitalidade: vida máxima (×5) e cura. Mana máxima = 20 + 2 × Agilidade. Atributos iniciais = 10 + D6 + bônus original.\n\nCOMBATE\nRole D20 para Ataque Básico, Bola de Fogo e Ataque Rápido. Role D6 para Golpe Poderoso, Cura Mágica e Meditar; o D6 também pode ser preparado para dano. Uma ação termina o turno. Mana regenera 4 no início de cada turno.\nAtaque básico: D20 + Força contra D20 + Defesa; dano Força + D6.\nGolpe Poderoso (8 MP): 2 × Força + D6, acerto automático.\nBola de Fogo (12 MP): D20 + Agilidade contra D20 + metade da Defesa; dano Agilidade + 2 × D6.\nAtaque Rápido (6 MP): D20 + Agilidade + 2 contra D20 + Defesa; dano metade inteira de Força + metade inteira de Agilidade + D6.\nCura (10 MP): Vitalidade + D6, limitada à vida máxima. Meditar: 10 + D6 de mana, limitada ao máximo.\nArmas fabricadas permitem uma nova rolagem opcional de um dado já preparado por luta, sem bônus numérico à ficha.\n\nCAMPANHA\nTrês categorias de prova liberam a audiência. Escolha uma facção e confronte o regente. Quatro casos resolvidos, dos quais três sem luta, permitem solução pacífica final. Você pode explorar depois do final. Descanso custa 3 moedas e recupera HP/MP. Derrota ou retirada restaura o estado anterior ao combate. Salvamento automático local entre ações.\n\nEXPANSÃO — MERCADORES DA CONJUNÇÃO\nNível: a experiência é obtida por exploração, arquivos, encomendas, diálogos, fabricação e casos. Cada nível concede 2 pontos de atributo, distribuídos manualmente. As fórmulas originais continuam válidas. O inimigo recebe um pequeno ajuste de acordo com o nível. Mercados: estoque por dia; viagens e descanso avançam um dia. Mochila: consumíveis recuperam HP/MP; em combate, consomem um turno. Derrota ou retirada devolve os itens usados durante o confronto. Encontros de viagem: decida ou ignore antes de continuar. NPCs recorrentes mudam de distrito e desbloqueiam conversas com o avanço da investigação.\n\nV3 — COMPANHIA: converse com Ione, Raska, Vesper ou Maelis e recrute a partir de 15 de afinidade. Até três aliados ativos; os demais ficam na reserva. Cada missão tem três etapas com escolhas e combate opcional. O apoio pode ser usado uma vez por luta, sem gastar o turno; a partir de 70 de afinidade ele fica mais forte. Uma vitória com apoio concede +3 afinidade. Derrota restaura o checkpoint, inclusive os consumíveis. Confira o perfil para saber o próximo destino.\n\nV4: Cada distrito tem uma masmorra opcional com dez ondas e um chefe na décima. A equipe pode ter três NPCs, cada um com um apoio por luta. Diálogos de pares alteram a coesão e a eficácia do apoio. Derrotas restauram apenas a onda atual; abandonar reinicia a expedição, sem recompensas repetidas. HP e MP recuperam parcialmente entre ondas.\n\nV5 — RELÍQUIAS: em cada vitória nas masmorras, chance de raro de 8% (1–3), 12% (4–6), 18% (7–9), 35% (chefe). Artefato lendário: 15% independente no chefe. Equipe um raro e um lendário na mochila; cada poder pode ser usado uma vez por luta. Revanches repetem apenas drops. Áudio: instale as faixas oficiais pelo BAIXAR_BGM.bat; os arquivos provisórios já estão incluídos. Som alterna música ligada/desligada.''')
    def popup(self,titulo,txt):
        win=tk.Toplevel(self.root); win.title(titulo); win.geometry('720x530'); win.configure(bg=self.BG_FUNDO)
        t=tk.Text(win,wrap='word',bg=self.BG_LOG,fg=self.FG_TEXTO,font=('Segoe UI',11),padx=18,pady=15); s=ttk.Scrollbar(win,command=t.yview); t.configure(yscrollcommand=s.set); s.pack(side='right',fill='y'); t.pack(fill='both',expand=True); t.insert('1.0',txt); t.config(state='disabled')
    def layout(self,title,com_rodape=False):
        self.audio.tocar(contexto(title,MERCADOS[self.c.local],POR_SIGNO[self.c.local].local))
        self._limpar_tela(); outer=tk.Frame(self.root,bg=self.BG_FUNDO,padx=15,pady=12); outer.pack(fill='both',expand=True)
        top=tk.Frame(outer,bg=self.BG_FUNDO); top.pack(fill='x'); self.label(top,title,20,self.FG_TITULO).pack(side='left')
        self.botao(top,'Som',self.alternar_audio).pack(side='right',padx=3); self.botao(top,'Guia [?]',self.guia).pack(side='right',padx=3); self.botao(top,'Menu',lambda:(self.salvar(),self.menu())).pack(side='right',padx=3)
        p=self.c.p; line=f'{p.nome} · {p.classe} · {POR_SIGNO[self.c.origem].povo}  |  HP {p.vida}/{p.vida_maxima}  ·  MP {p.mana}/{p.mana_maxima}  |  {self.c.ouro} moedas  |  Nv. {self.c.nivel} · XP {self.c.xp}/{self.c.xp_meta}'
        self.label(outer,line,11).pack(anchor='w',pady=5); self.label(outer,f'Força {p.forca}  ·  Defesa {p.defesa}  ·  Agilidade {p.agilidade}  ·  Vitalidade {p.vitalidade}',10,self.FG_MUTED).pack(anchor='w')
        self.rodape=None
        if com_rodape:
            self.rodape=tk.Frame(outer,bg=self.BG_CARD,padx=12,pady=6); self.rodape.pack(side='bottom',fill='x')
        body=tk.Frame(outer,bg=self.BG_FUNDO); body.pack(fill='both',expand=True,pady=10)
        nav_pane=tk.Frame(body,bg=self.BG_CARD,width=265); nav_pane.pack(side='left',fill='y',padx=(0,10)); nav_pane.pack_propagate(False)
        nav,nav_canvas=self.painel_rolavel(nav_pane,self.BG_CARD,8,8)
        self.heading(nav,'Mapa dos distritos',14)
        for d in DISTRITOS:
            mark='✓' if d.signo in self.c.resolvidos else '›' if d.signo==self.c.local else '·'
            b=self.botao(nav,f'{mark} {d.signo} — {d.nome}',lambda s=d.signo:self.viagem(s),anchor='w',font=('Segoe UI',9),pady=2,wraplength=240); b.pack(fill='x',pady=1)
            if not self.c.prologo or self.c.expedicao: b.config(state='disabled')
        for txt,fn in [('Diário e provas',self.diario),('Itens / mochila',self.mochila),('Forja',self.forja),('Nível / atributos',self.progressao),('Companhia / vínculos',self.vinculos),('Conselho [!]',self.conselho)]:
            b=self.botao(nav,txt,fn,anchor='w',pady=3); b.pack(fill='x',pady=1)
            if not self.c.prologo or self.c.expedicao: b.config(state='disabled')
        pane=tk.Frame(body,bg=self.BG_CARD); pane.pack(side='left',fill='both',expand=True)
        self.content,canvas=self.painel_rolavel(pane,self.BG_CARD,18,15)
        self.rolagem_mouse((pane,canvas),(nav_pane,nav_canvas))
        self.banner(title)
        if self.aviso:
            self.texto(self.aviso,self.FG_TITULO); self.aviso=None
        return self.content
    def texto(self,txt,color=None):
        w=self.label(self.content,txt,11,color,anchor='w',justify='left',wraplength=620); w.pack(fill='x',pady=(2,12)); return w
    def choice(self,txt,cmd,state='normal'):
        self.botao(self.content,txt,cmd,anchor='w',state=state).pack(fill='x',pady=4)
    def acao(self,fn,ret=None):
        try:
            result=fn(); self.salvar()
            if isinstance(result,str): self.aviso=result
            (ret or self.mundo)()
        except ValueError as e: messagebox.showwarning('Ação indisponível',str(e))
    def prologo(self):
        d=POR_SIGNO[self.c.origem]; self.layout('Prólogo — O sino que não tocou',com_rodape=True)
        self.heading(self.content,d.nome,18)
        self.texto(f'No ano 47 do Pacto, na cidade-estado de Merídia, você retorna a {d.nome} para a festa da Conjunção. {d.regiao}: as lanternas são acesas e os comerciantes fecham as bancas. No instante em que o décimo segundo sino deveria tocar, a água para de correr. Um clarão corta o céu. O chão estremece.')
        self.texto('Uma arquivista chamada Ione tropeça na rua, segurando um astrolábio quebrado. Você a ajuda a alcançar uma porta iluminada. “Não foi acidente”, diz ela. “Cassian quer que o Conselho vote poderes de emergência amanhã. Os doze distritos alimentam a máquina sob o observatório. Se alguém reuniu as peças sem autorização, precisamos provar antes da conjunção.”')
        self.texto('Ione pede três tipos de prova: quem desviou os materiais, quem assinou as ordens e quem viu a operação. Ela não pode circular sem ser reconhecida. Você conhece a cidade e pode andar onde os guardas a seguiriam. “Escolha como vai começar. Eu guardarei cópias no Conselho.”')
        self.label(self.rodape,'Escolha como começar — role a narrativa acima para ler o prólogo.',10,self.FG_TITULO).pack(anchor='w')
        for txt,op in [('Assinar uma denúncia pública — confiança no distrito natal.','testemunhar'),('Manter Ione anônima — ela fornece 4 moedas para despesas.','sigilo'),('Examinar o astrolábio — conservar um fragmento de cristal.','investigar')]:
            self.botao(self.rodape,txt,lambda op=op:self.acao(lambda:self.c.iniciar(op)),anchor='w',pady=4).pack(fill='x',pady=2)
    def mundo(self):
        if self.c.expedicao: self.masmorra(); return
        if self.c.evento: self.encontro(); return
        self.modo='campanha'; d=POR_SIGNO[self.c.local]; self.layout(f'{d.signo}  /  {d.nome}')
        self.texto(f'{d.povo} · {d.regiao} · Confiança local: {self.c.reputacao[d.signo]}',self.FG_TITULO)
        self.texto(d.lore)
        if self.c.evento: self.choice('[!] Encontro em andamento — resolver antes de viajar',self.encontro)
        for n in NPCS:
            if self.c.npc_disponivel(n): self.choice(f'[Diálogo] {n} está aqui — conversa recorrente',lambda n=n:self.npc(n))
        for n in self.c.equipe:
            self.texto(f'Companhia: {n} · {self.c.grau(n)} ({self.c.afinidade[n]}/100)',self.FG_TITULO)
            if self.c.missao_disponivel(n): self.choice('[Missão pessoal] '+self.c.etapa_missao(n)[2],lambda n=n:self.missao(n))
        for n in COMPANHEIROS:
            if self.c.pode_recrutar(n): self.choice('[Recrutar] '+n,lambda n=n:self.acao(lambda:self.c.recrutar(n),self.vinculos))
        self.heading(self.content,'Locais exploráveis',16)
        self.choice(f'[Masmorra {self.c.recordes[d.signo]}/10] {MASMORRAS[d.signo].nome}',self.masmorra)
        self.choice(f'[?] {d.arquivo} — história e documentos',self.arquivo)
        self.choice(f'[{"✓" if d.signo in self.c.resolvidos else "!"}] {d.local} — conversar com {d.npc}',self.caso)
        self.choice(f'[+] {d.oficina} — encomendas, materiais e construção de armas',self.oficina)
        for i,n in enumerate(MERCADOS[d.signo]): self.choice(f'[Mercado] {n}',lambda i=i:self.mercado(i))
        self.choice('Hospedagem de viajantes — recuperar vida e mana (3 moedas)',lambda:self.acao(self.c.descansar))
        self.heading(self.content,'Objetivo atual',16)
        if self.c.final: self.texto('Campanha concluída. Continue explorando os casos restantes. '+self.c.epilogo())
        elif self.c.alianca: self.texto('Vá ao Conselho e decida como impedir a ativação do observatório. Ou reúna mais apoio para negociar.')
        else: self.texto(f'Reúna ordens, suprimentos e testemunhos. Categorias: {len(self.c.categorias())}/3. '+('Audiência disponível no Conselho.' if self.c.audiencia_liberada() else 'Escolha outros distritos no mapa.'))
    def arquivo(self):
        d=POR_SIGNO[self.c.local]; self.c.ler(); self.salvar(); self.layout(d.arquivo); self.heading(self.content,'Crônicas do distrito',18); self.texto(d.lore); self.texto('Nota de Ione: “Compare o arquivo com as outras regiões. Nenhum bairro é autossuficiente: é isso que torna a cidade forte, e o que torna a máquina perigosa.”'); self.choice('Voltar ao distrito',self.mundo)
    def caso(self):
        d=POR_SIGNO[self.c.local]; self.layout(d.local); self.heading(self.content,d.npc,18)
        if d.signo in self.c.resolvidos:
            self.texto(d.retorno); self.texto('Prova arquivada: '+d.prova,self.FG_TITULO)
        else:
            self.texto(d.cena)
            self.heading(self.content,'Conversa',15); self.falas_locais={}
            for i, pergunta in enumerate(('O que está em jogo para você?', 'Que detalhe confirma a suspeita?', 'O que espera do Conselho?')):
                self.choice('Perguntar: '+pergunta,lambda i=i:self.dialogar(d.signo,i))
                fala=self.label(self.content,'',11,self.FG_TITULO,anchor='w',justify='left',wraplength=620); fala.pack(fill='x',pady=(0,6)); self.falas_locais[i]=fala
                if i in self.perguntas.get(d.signo,set()): fala.config(text=f'{d.npc}: '+DIALOGOS[d.signo][i])
            self.texto('A investigação pode ser resolvida de três formas. Uma prova será obtida em qualquer rota bem-sucedida. A forma como você age muda o apoio político e os recursos.')
            self.choice('[Combate] '+d.luta,lambda:self.iniciar_luta('local'))
            self.choice(f'[Acordo · {self.c.custo_acordo()} moedas] '+d.acordo,lambda:self.acao(lambda:self.c.resolver('acordo'),self.caso))
            self.choice(f'[{d.classe_forte} · gratuito] '+d.atalho,lambda:self.acao(lambda:self.c.resolver('classe'),self.caso),'normal' if self.c.p.classe==d.classe_forte else 'disabled')
            if self.c.p.classe==d.classe_fraca: self.texto('Limitação de classe: esta comunidade exige um intermediário adicional (+4 moedas na rota de acordo). O combate permanece disponível.',self.FG_MUTED)
        self.choice('Voltar ao distrito',self.mundo)
    def dialogar(self,signo,i):
        self.perguntas.setdefault(signo,set()).add(i); self.c.perguntas[signo]=sorted(self.perguntas[signo])
        d=POR_SIGNO[signo]; registro=f'{d.npc}: {DIALOGOS[signo][i]}'
        if registro not in self.c.diario: self.c.diario.append(registro); self.salvar()
        fala=self.falas_locais.get(i)
        if fala is not None and fala.winfo_exists(): fala.config(text=registro)
        else: self.caso()
    def oficina(self):
        d=POR_SIGNO[self.c.local]; self.layout(d.oficina); self.texto(f'O artesão oferece trabalho em encomendas públicas. Cada encomenda entrega 2 unidades de {d.material} e 3 moedas. Restam {2-self.c.coletados.get(d.signo,0)} encomendas.'); self.choice('Trabalhar na oficina',lambda:self.acao(self.c.coletar,self.oficina),'normal' if self.c.coletados.get(d.signo,0)<2 else 'disabled'); self.choice('Abrir bancada de construção',self.forja); self.choice('Voltar',self.mundo)
    def forja(self):
        self.layout('Inventário e construção de armas'); self.texto('Materiais: '+'  |  '.join(f'{k}: {v}' for k,v in self.c.materiais.items())); self.texto('Equipamento atual: '+(self.c.equipada or 'Nenhum')+'. As armas não alteram status nem fórmulas de dano; pontos de nível são distribuídos separadamente.');
        for nome,(req,dado,desc) in RECEITAS.items():
            self.heading(self.content,nome,15); self.texto(' / '.join(f'{v} {k}' for k,v in req.items())+' — '+desc)
            if nome in self.c.armas: self.choice('Equipar'+(' (equipada)' if nome==self.c.equipada else ''),lambda n=nome:self.acao(lambda:self.c.equipar(n),self.forja),'disabled' if nome==self.c.equipada else 'normal')
            else: self.choice('Fabricar e equipar',lambda n=nome:self.acao(lambda:self.c.fabricar(n),self.forja),'normal' if all(self.c.materiais[k]>=v for k,v in req.items()) else 'disabled')
        self.choice('Desequipar arma',lambda:self.acao(lambda:self.c.equipar(None),self.forja)); self.choice('Voltar',self.mundo)
    def diario(self):
        self.layout('Diário de investigação'); self.texto(f'Distritos visitados: {len(self.c.visitados)}/12 | Arquivos lidos: {len(self.c.lidos)}/12 | Casos: {len(self.c.resolvidos)}/12 | Apoio não violento: {self.c.apoio()}')
        for cat in ('ordens','suprimentos','testemunhos'):
            provas=[POR_SIGNO[k].prova for k in self.c.resolvidos if POR_SIGNO[k].categoria==cat]; self.heading(self.content,('✓ ' if provas else '· ')+cat.capitalize(),15); self.texto('\n'.join(provas) if provas else 'Nenhuma prova ainda.')
        self.heading(self.content,'Missões pessoais',16); self.texto('\n'.join(f'{n}: {COMPANHEIROS[n]["titulo"]} — {len(self.c.missoes[n])}/3' for n in self.c.recrutados) or 'Nenhuma missão pessoal iniciada.'); self.heading(self.content,'Registro de decisões',16); self.texto('\n\n'.join(self.c.diario)); self.choice('Voltar',self.mundo)
    def conselho(self):
        self.layout('Conselho — A Praça do Meridiano'); c=self.c
        if c.final: self.heading(self.content,'Epílogo — A cidade depois da noite',18); self.texto(c.epilogo()); self.choice('Voltar a explorar',self.mundo); return
        if not c.audiencia_liberada(): self.texto('Ione: “Uma suspeita isolada não basta. Traga ordens, suprimentos e testemunhos. Só então os magistrados serão obrigados a convocar uma sessão.”'); self.choice('Consultar provas',self.diario); self.choice('Voltar',self.mundo); return
        if not c.alianca:
            self.heading(self.content,'Ato II — O preço da proteção',18); self.texto('Ione espalha as provas sobre a mesa. O desvio de materiais abasteceu o astrolábio; as ordens prepararam o fechamento dos portões; os testemunhos ligam a operação ao observatório. Cassian não nega a máquina. “Durante a guerra perdemos milhares porque ninguém podia dar uma ordem a tempo. Com uma chave, posso proteger todos.”\nMaelis responde: “Com uma chave, também pode punir todos.” Os delegados pedem uma proposta sua antes de votar.')
            for nome,desc in FACCOES.items(): self.choice(f'Apoiar {nome} — {desc}',lambda n=nome:self.acao(lambda:c.escolher_alianca(n),self.conselho))
        else:
            self.heading(self.content,'Ato III — A última conjunção',18); self.texto('A proposta de '+c.alianca+' ganha votos suficientes para uma investigação. Cassian abandona a sessão e leva a chave ao observatório. A máquina começa a puxar água dos canais e energia das torres. Ione acompanha você até a escadaria; guardas locais aguardam suas instruções.')
            self.texto('No observatório, Cassian ergue a chave. “Se a entrego, o próximo desastre será culpa de vocês.” Você pode desarmá-lo em combate ou convencer os operadores a suspender a máquina. Para isso, eles precisam confiar que os distritos agirão juntos.')
            self.choice('[Combate] Impedir Cassian de acionar a chave. Ele se defende com magia.',lambda:self.iniciar_luta('final'))
            self.choice(f'[Negociação] Convocar os operadores e exigir a entrega da chave — {len(c.resolvidos)}/4 casos, {c.apoio()}/3 soluções pacíficas.',lambda:self.acao(lambda:c.encerrar('acordo'),self.conselho),'normal' if c.final_pacifico_liberado() else 'disabled')
        self.choice('Voltar e reunir apoio',self.mundo)
    def iniciar_luta(self,tipo,nome=None):
        try: inimigo=self.c.iniciar_onda() if tipo=='masmorra' else self.c.decidir_missao(nome,2) if tipo=='pessoal' else self.c.resolver('combate') if tipo=='local' else self.c.encerrar('combate')
        except ValueError as e: messagebox.showwarning('Combate',str(e)); return
        self.salvar(); self.modo='pve'; self.p1=self.c.p; self.p2=inimigo; self.jogador_atual=self.p1; self.alvo_atual=self.p2; self.turno=1; self.arma_usada=False; self.btn_arma=None
        self.audio.tocar('chefe' if tipo=='final' or (tipo=='masmorra' and self.c.pendente['onda']==10) else 'combate'); self.retrato_luta=None; self.btn_item=None; self.btn_apoio=None; self.botoes_apoio={}; self.botoes_reliquia={}; super()._construir_tela_combate(); self.retrato_luta=tk.Label(self.card_p1,bg=self.BG_CARD,image=self.imagem(f'portrait_{self.indice(self.c.origem)}_battle',True)); self.retrato_luta.pack(side='right'); bar=tk.Frame(self.root,bg=self.BG_FUNDO); bar.pack(fill='x',padx=20,pady=(0,8),before=self.txt_log); self.botao(bar,'Retirada (restaurar checkpoint)',self.retirar).pack(side='right'); self.botao(bar,'Som',self.alternar_audio).pack(side='right',padx=3); self.botao(bar,'Guia [?]',self.guia).pack(side='right',padx=5); self.btn_item=self.botao(bar,'Usar item (1 turno)',self.item_combate); self.btn_item.pack(side='right',padx=5)
        if self.c.equipada:
            dado=RECEITAS[self.c.equipada][1]; self.btn_arma=self.botao(bar,f'{self.c.equipada}: rolar novamente {dado}',self.reroll); self.btn_arma.pack(side='left')
        asset=f'enemy_{self.indice(self.c.local)}_{self.c.pendente["onda"]}' if tipo=='masmorra' else f'enemy_personal_{list(COMPANHEIROS).index(nome)}' if tipo=='pessoal' else 'enemy_final' if tipo=='final' else f'enemy_local_{self.indice(self.c.local)}'
        tk.Label(self.card_p2,bg=self.BG_CARD,image=self.imagem(asset,True)).pack(side='right')
        if self.c.equipe:
            support=tk.Frame(self.root,bg=self.BG_CARD); support.pack(fill='x',padx=20,pady=(0,5),before=self.txt_log)
            for n in self.c.equipe:
                col=tk.Frame(support,bg=self.BG_CARD); col.pack(side='left',expand=True,fill='x',padx=3)
                tk.Label(col,bg=self.BG_CARD,image=self.imagem('npc_'+n,True)).pack(side='left')
                self.botoes_apoio[n]=self.botao(col,f'{n} — {self.c.descricao_apoio(n)}',lambda n=n:self.apoio_combate(n),wraplength=230,font=('Segoe UI',9),padx=4); self.botoes_apoio[n].pack(side='left',fill='x',expand=True)
        if self.c.reliquias_ativas():
            row=tk.Frame(self.root,bg=self.BG_CARD); row.pack(fill='x',padx=20,pady=3,before=self.txt_log)
            for rid in self.c.reliquias_ativas():
                obj=CATALOGO[rid]; b=self.botao(row,obj.nome+' — '+obj.descricao.split(' — ')[0],lambda rid=rid:self.reliquia_combate(rid),wraplength=400,font=('Segoe UI',9),pady=4); b.pack(side='left',expand=True,fill='x',padx=4); self.botoes_reliquia[rid]=b
        inicio=f'Onda {self.c.pendente["onda"]}/10 — {inimigo.nome} bloqueia a passagem.' if tipo=='masmorra' else COMPANHEIROS[nome]['inicio_luta'] if tipo=='pessoal' else 'Cassian tenta conservar a chave.' if tipo=='final' else POR_SIGNO[self.c.local].luta
        self._log('O confronto começou. '+inicio)
        if tipo=='masmorra' and self.c.pendente['onda']==10: self._log(PADROES_CHEFE[self.c.local][2])
        self._comecar_turno_jogador()
    def apoio_combate(self,n=None):
        if self.modo!='pve' or self.jogador_atual is not self.p1: return
        try: msg=self.c.usar_apoio(self.p2,n)
        except ValueError as e: messagebox.showwarning('Apoio',str(e)); return
        self._log(msg)
        if not self.p2.esta_vivo(): self.fim_luta(True); return
        self._atualizar_status()
    def _construir_tela_combate(self):
        super()._construir_tela_combate()
        if self.modo=='arena':
            self.audio.tocar('combate'); self.botao(self.root,'Voltar ao menu',lambda: self.menu() if messagebox.askyesno('Duelo','Encerrar duelo?') else None).pack(pady=(0,8))
    def _atualizar_status(self):
        super()._atualizar_status()
        if self.modo=='pve':
            if self.c.pendente and self.c.pendente['tipo']=='masmorra': self.lbl_turno.config(text=f'Onda {self.c.pendente["onda"]}/10 · '+self.lbl_turno.cget('text'))
            if getattr(self,'retrato_luta',None) and self.retrato_luta.winfo_exists(): self.retrato_luta.config(image=self.imagem(f'portrait_{self.indice(self.c.origem)}_'+('hurt' if self.p1.vida<self.p1.vida_maxima*.35 else 'battle'),True))
            for rid,b in getattr(self,'botoes_reliquia',{}).items():
                if b.winfo_exists(): b.config(state='normal' if self.jogador_atual is self.p1 and self.c.reliquia_disponivel(rid) else 'disabled')
            for n,b in getattr(self,'botoes_apoio',{}).items():
                if b.winfo_exists(): b.config(state='normal' if self.jogador_atual is self.p1 and self.c.apoio_disponivel(n) else 'disabled')
            if getattr(self,'btn_item',None) and self.btn_item.winfo_exists(): self.btn_item.config(state='normal' if self.jogador_atual is self.p1 else 'disabled')
        if self.modo=='pve' and getattr(self,'btn_arma',None):
            dado=RECEITAS[self.c.equipada][1]; prep=self.p1.d20_preparado if dado=='D20' else self.p1.d6_preparado
            self.btn_arma.config(state='normal' if self.jogador_atual is self.p1 and prep is not None and not self.arma_usada else 'disabled')
    def reroll(self):
        if self.modo!='pve' or self.arma_usada or self.jogador_atual is not self.p1: return
        dado=RECEITAS[self.c.equipada][1]; attr='d20_preparado' if dado=='D20' else 'd6_preparado'; old=getattr(self.p1,attr)
        if old is None: return
        new=(self.p1.d20 if dado=='D20' else self.p1.d6).rolar(); setattr(self.p1,attr,new); self.arma_usada=True; self._log(f'Arma: {dado} {old} → {new}. O novo valor substitui o anterior.'); self._atualizar_status()
    def _finalizar_acao_turno(self):
        if self.modo!='pve': return super()._finalizar_acao_turno()
        self.p1.d20_preparado=self.p1.d6_preparado=None
        if not self.p2.esta_vivo(): self.fim_luta(True); return
        self.jogador_atual=self.p2; self.alvo_atual=self.p1; self._comecar_turno_jogador(); self._bloquear_botoes()
        self.ai_job=self.root.after(450,self.ia)
    def ia(self):
        self.ai_job=None
        if self.modo!='pve': return
        p=self.p2; alvo=self.p1
        boss=self.c.pendente['tipo']=='masmorra' and self.c.pendente['onda']==10
        if boss:
            nome,habilidade=acao_chefe(self.c.local,self.turno)
            if p.tem_mana(p.habilidades[habilidade]):
                _,msg=p.usar_habilidade(habilidade,alvo); msg=f'{nome} — {habilidade}\n'+msg
            else: msg=p.meditar()
        elif p.vida<p.vida_maxima*.35 and p.tem_mana(10) and self.c.pendente['tipo']!='masmorra': _,msg=p.usar_habilidade('Cura Mágica',alvo)
        elif p.classe=='Mago' and p.tem_mana(12): _,msg=p.usar_habilidade('Bola de Fogo',alvo)
        elif p.classe=='Ladino' and p.tem_mana(6): _,msg=p.usar_habilidade('Ataque Rápido',alvo)
        elif p.tem_mana(8) and (p.classe=='Guerreiro' or alvo.vida<=p.forca*2): _,msg=p.usar_habilidade('Golpe Poderoso',alvo)
        elif p.mana<6: msg=p.meditar()
        else: msg=p.atacar(alvo)
        self._log(msg)
        if not alvo.esta_vivo(): self.fim_luta(False); return
        self.turno+=1; self.jogador_atual=self.p1; self.alvo_atual=self.p2; self._comecar_turno_jogador()
        if boss: self._log('Próxima técnica do chefe: '+acao_chefe(self.c.local,self.turno)[1]+'.')
    def retirar(self):
        if messagebox.askyesno('Retirada','Abandonar a luta e restaurar o estado anterior?'): self.fim_luta(False)
    def fim_luta(self,vitoria):
        if self.ai_job: self.root.after_cancel(self.ai_job); self.ai_job=None
        masmorra=self.c.pendente and self.c.pendente['tipo']=='masmorra'
        pessoal=self.c.pendente.get('nome') if self.c.pendente and self.c.pendente['tipo']=='pessoal' else None
        self._bloquear_botoes(); self.c.resultado_combate(vitoria); self.salvar(); self.modo='campanha'; self.btn_arma=None
        if masmorra:
            self.masmorra();
            if vitoria: self.audio.tocar('vitoria')
            return
        if vitoria: self.audio.tocar('vitoria')
        messagebox.showinfo('Confronto encerrado','Vitória! A decisão e as recompensas foram registradas.' if vitoria else 'O confronto foi interrompido. Seu estado anterior foi restaurado; tente outra abordagem ou descanse.')
        if pessoal: self.perfil_companheiro(pessoal)
        else: self.conselho() if self.c.alianca and self.c.final else self.mundo()
    def indice(self,signo): return next(i for i,d in enumerate(DISTRITOS) if d.signo==signo)
    def imagem(self,nome,pequena=False):
        key=(nome,pequena)
        if key not in self.imagens:
            img=tk.PhotoImage(file=str(Path(__file__).with_name('artes')/(nome+'.png')))
            self.imagens[key]=img.subsample(2,2) if pequena else img
        return self.imagens[key]
    def banner(self,title):
        c=self.c; i=self.indice(c.local); orig=self.indice(c.origem)
        mode='level' if title.startswith('Nível') else 'travel' if title.startswith('Travessia') else 'dialog' if title.startswith(('Conversa','Prólogo','Conselho')) or title==POR_SIGNO[c.local].local else 'calm'
        if c.p.vida<c.p.vida_maxima*.35 and mode=='calm': mode='hurt'
        name=f'dungeon_{i}' if title.startswith('Masmorra') else 'journal' if title.startswith(('Diário','Crônicas')) else f'market_{i}' if title in MERCADOS[c.local] else f'travel_{i}' if mode=='travel' else f'district_{i}'
        row=tk.Frame(self.content,bg=self.BG_CARD); row.pack(fill='x',pady=(0,12))
        compacta=self.root.winfo_width()<1100
        scene=tk.Label(row,bg=self.BG_CARD,image=self.imagem(name+'_fade0',compacta)); scene.pack(side='left',anchor='n')
        for delay,asset in [(65,name+'_fade1'),(140,name)]: self.transicoes.append(self.root.after(delay,lambda w=scene,a=asset,small=compacta: w.configure(image=self.imagem(a,small)) if w.winfo_exists() else None))
        p=tk.Frame(row,bg=self.BG_CARD); p.pack(side='left',padx=8,anchor='n'); tk.Label(p,bg=self.BG_CARD,image=self.imagem(f'portrait_{orig}_{mode}')).pack(); self.label(p,c.p.nome,10,self.FG_TITULO,wraplength=100).pack(); self.label(p,POR_SIGNO[c.origem].povo,9,wraplength=100).pack()
        # Short reveal of the heading accent; no modal timers or input blocking.
        shade=tk.Frame(self.content,bg='#584735',height=3); shade.pack(fill='x',pady=(0,8))
        for delay,col in [(60,'#80613e'),(120,'#b18a4b'),(180,'#e5bf77')]: self.transicoes.append(self.root.after(delay,lambda w=shade,col=col: w.configure(bg=col) if w.winfo_exists() else None))
    def viagem(self,signo):
        if signo==self.c.local: self.mundo(); return
        antigo=self.c.local
        try: self.c.viajar(signo); self.salvar()
        except ValueError as e: messagebox.showwarning('Travessia',str(e)); return
        self.layout('Travessia — '+POR_SIGNO[signo].nome); self.heading(self.content,f'{POR_SIGNO[antigo].nome} → {POR_SIGNO[signo].nome}',17); self.texto(f'Dia {self.c.dia}. Você chega a {POR_SIGNO[signo].regiao}. '+POR_SIGNO[signo].lore)
        self.choice('Chegar ao distrito'+(' — encontro na estrada!' if self.c.evento else ''),self.encontro if self.c.evento else self.mundo)
    def encontro(self):
        if not self.c.evento: self.mundo(); return
        signo,i=self.c.evento; e=EVENTOS[signo][i]; self.layout('Encontro — '+e[0]); self.heading(self.content,e[0]); self.texto(e[1]);
        for k in (0,1):
            ef=e[3+2*k]; labels={'ouro':'moedas','rep':'reputação','xp':'XP','material':'material local','dano':'HP perdido','item':'item','selo':'selo ou 4 moedas'}
            self.choice(e[2+2*k]+'  ['+' · '.join((f'{v:+d} {labels[a]}' if type(v)==int and a!='dano' else f'{v} HP perdidos' if a=='dano' else labels[a] if a=='selo' else str(v)) for a,v in ef.items())+']',lambda k=k:self.acao(lambda:self.c.decidir_evento(k),self.mundo))
        self.choice('Seguir sem intervir',lambda:self.acao(lambda:self.c.decidir_evento(2),self.mundo))
    def item_icon(self,n): return dict(zip(ITENS,('potion','essence','elixir','ration','seal'))).get(n,'material')
    def item_row(self,icon,title,desc,btn=None,cmd=None,state='normal'):
        row=tk.Frame(self.content,bg=self.BG_CARD); row.pack(fill='x',pady=4); tk.Label(row,bg=self.BG_CARD,image=self.imagem('icon_'+icon)).pack(side='left',padx=(0,8),anchor='n'); t=tk.Frame(row,bg=self.BG_CARD); t.pack(side='left',fill='x',expand=True); self.label(t,title,12,self.FG_TITULO,anchor='w').pack(fill='x'); self.label(t,desc,10,wraplength=400,justify='left',anchor='w').pack(fill='x')
        if btn: self.botao(row,btn,cmd,state=state).pack(side='right',padx=3)
    def mercado(self,loja):
        c=self.c; self.layout(MERCADOS[c.local][loja]); self.texto(f'Dia {c.dia} · {c.ouro} moedas. Estoque: três unidades por produto a cada dia. Viajar ou descansar avança um dia.')
        for n,preco in c.oferta(loja).items():
            qtd=c.estoque(loja,n); desc=ITENS[n][3] if n in ITENS else 'Material para construção de armas.'
            self.item_row(self.item_icon(n),f'{n} — {preco} moedas',f'{desc} | Estoque: {qtd}', 'Comprar',lambda n=n:self.acao(lambda:c.comprar(loja,n),lambda:self.mercado(loja)),'normal' if qtd and c.ouro>=preco else 'disabled')
        self.choice('Abrir mochila',self.mochila); self.choice('Voltar ao distrito',self.mundo)
    def mochila(self):
        c=self.c; self.layout('Mochila — itens e consumíveis'); self.texto('Itens comprados e encontrados ficam guardados. Usar fora de combate não consome turno. Os selos são utilizados nas opções de pedágio.')
        for n,q in c.inventario.items(): self.item_row(self.item_icon(n),f'{n} × {q}',ITENS[n][3],'Usar',lambda n=n:self.acao(lambda:c.usar_item(n),self.mochila),'normal' if q and ITENS[n][0]!='selo' else 'disabled')
        self.texto('Materiais: '+ ' · '.join(f'{k}: {v}' for k,v in c.materiais.items())); self.choice('Equipamentos raros e artefatos',self.reliquias); self.choice('Forja e armas',self.forja); self.choice('Voltar',self.mundo)
    def progressao(self):
        c=self.c; p=c.p; self.layout('Nível e atributos'); self.heading(self.content,f'Nível {c.nivel} · {c.pontos} pontos disponíveis',19); self.item_row('xp',f'Experiência: {c.xp}/{c.xp_meta}','+2 pontos por nível. Ganhe XP ao descobrir distritos, ler arquivos, resolver casos, fabricar e conversar.'); ttk.Progressbar(self.content,maximum=c.xp_meta,value=c.xp).pack(fill='x',pady=7)
        for k,n,desc in [('forca','Força','Ataque físico e dano.'),('defesa','Defesa','Resistência aos ataques físicos e mágicos.'),('agilidade','Agilidade','Ataques mágicos e rápidos; +2 mana máxima por ponto.'),('vitalidade','Vitalidade','Cura e +5 vida máxima por ponto.')]: self.item_row(k,f'{n}: {getattr(p,k)}',desc,'+1 ponto',lambda k=k:self.acao(lambda:c.investir(k),self.progressao),'normal' if c.pontos else 'disabled')
        self.item_row('vida',f'Vida {p.vida}/{p.vida_maxima}','Vitalidade × 5.'); self.item_row('mana',f'Mana {p.mana}/{p.mana_maxima}','20 + Agilidade × 2.'); self.choice('Voltar',self.mundo)
    def vinculos(self):
        c=self.c; self.layout('Companhia — vínculos e missões'); self.texto('Recrute após a primeira conversa (15 de afinidade). Até três companheiros acompanham você; os demais ficam na reserva. Troque livremente fora de expedições e combates.')
        self.texto('Afinidade: 0–14 Distante · 15–39 Respeito · 40–69 Confiança · 70–100 Lealdade. Lealdade fortalece o apoio em combate.',self.FG_MUTED)
        self.heading(self.content,f'Equipe ativa — {len(c.equipe)}/3',16)
        self.texto('Em campo: '+(', '.join(c.equipe) or 'Nenhum companheiro')+'. Cada membro tem um apoio por combate.',self.FG_TITULO)
        self.choice('Relações e diálogos de grupo',self.relacoes_equipe)
        for n,d in COMPANHEIROS.items():
            estado='ATIVO' if n in c.equipe else 'RESERVA' if n in c.recrutados else 'Não recrutado'
            self.item_row_npc(n, f'{n} — {d["papel"]} | {estado}',f'{c.grau(n)} · Afinidade {c.afinidade[n]}/100 · Missão {len(c.missoes[n])}/3',True)
            ttk.Progressbar(self.content,maximum=100,value=c.afinidade[n]).pack(fill='x',pady=(0,5))
            self.choice('Ver perfil de '+n,lambda n=n:self.perfil_companheiro(n))
            if n in c.recrutados: self.choice(('Retirar ' if n in c.equipe else 'Adicionar ')+n,lambda n=n:self.acao(lambda:c.selecionar(n),self.vinculos),state='normal' if n in c.equipe or len(c.equipe)<3 else 'disabled')
        self.choice('Voltar',self.mundo)
    def relacoes_equipe(self):
        c=self.c; self.layout('Companhia — relações de grupo')
        self.texto('A relação entre cada par é independente da afinidade com você. Rivalidade reduz apoios em 2; cooperação a partir de +25 aumenta apoios em 2. Se ambos ocorrerem, cancelam-se. Os diálogos desbloqueiam ao viajar juntos e após dois casos ou uma onda concluída.')
        if not c.pares_ativos(): self.texto('Adicione pelo menos dois NPCs à equipe.')
        for k in c.pares_ativos():
            self.heading(self.content,k.replace('|',' × '),16); self.texto(f'{c.relacao_grupo(k)} ({c.vinculos_grupo[k]:+d}) · cenas {len(c.cenas_grupo[k])}/2')
            ttk.Progressbar(self.content,maximum=200,value=c.vinculos_grupo[k]+100).pack(fill='x',pady=3)
            if c.cena_disponivel(k): self.choice('[Diálogo de grupo] '+PARES[k][len(c.cenas_grupo[k])+1][0],lambda k=k:self.dialogo_grupo(k))
            elif len(c.cenas_grupo[k])<2: self.texto('Próxima cena: resolva dois casos locais ou uma onda de masmorra.')
            else: self.texto('Os dois já concluíram suas conversas de grupo.')
        self.choice('Voltar à companhia',self.vinculos)
    def item_row_npc(self,n,titulo,desc,pequena=False):
        row=tk.Frame(self.content,bg=self.BG_FUNDO,padx=10,pady=8); row.pack(fill='x',pady=5)
        tk.Label(row,bg=self.BG_FUNDO,image=self.imagem('npc_'+n,pequena)).pack(side='left',padx=(0,12))
        f=tk.Frame(row,bg=self.BG_FUNDO); f.pack(side='left',fill='both',expand=True)
        self.label(f,titulo,13,self.FG_TITULO,wraplength=500,justify='left').pack(anchor='w'); self.label(f,desc,10,wraplength=500,justify='left').pack(anchor='w',pady=5)
    def perfil_companheiro(self,n):
        c=self.c; d=COMPANHEIROS[n]; self.layout('Conversa — '+n)
        self.item_row_npc(n,n+' · '+NPCS[n][0],d['papel']+' — '+c.grau(n)+f' ({c.afinidade[n]}/100)')
        ttk.Progressbar(self.content,maximum=100,value=c.afinidade[n]).pack(fill='x',pady=7)
        self.texto(d['historia']); self.texto('Valores: '+d['preferencia']); self.texto('Apoio: '+c.descricao_apoio(n)+' (1 vez por combate, sem gastar o turno).')
        etapa=len(c.relacoes[n]); self.texto(f'Conversas da campanha: {etapa}/3.');
        if etapa: self.texto('Memória: '+'\n'.join(NPCS[n][2][i][2+v] for i,v in enumerate(c.relacoes[n])),self.FG_MUTED)
        if c.npc_disponivel(n): self.choice('Conversar sobre a investigação',lambda:self.npc(n))
        elif etapa<3:
            self.texto(('Desbloqueia após dois casos resolvidos.' if etapa==1 else 'Desbloqueia após escolher uma facção.' if etapa==2 else 'Encontre o NPC no distrito indicado.'))
            if n not in c.equipe: self.choice('Viajar até '+POR_SIGNO[c.npc_local(n)].nome,lambda:self.viagem(c.npc_local(n)))
        if n not in c.recrutados:
            if c.pode_recrutar(n): self.choice('[Recrutar] Convidar '+n+' para viajar',lambda:self.acao(lambda:c.recrutar(n),lambda:self.perfil_companheiro(n)))
            elif etapa:
                self.choice('Viajar ao ponto de recrutamento: '+POR_SIGNO[c.local_recrutamento(n)].nome,lambda:self.viagem(c.local_recrutamento(n)))
            self.texto('Requisito: uma conversa e pelo menos 15 de afinidade. Recrute para abrir a missão pessoal.')
        elif n in c.equipe:
            self.choice('Deixar na reserva (pode voltar a qualquer momento)',lambda:self.acao(lambda:c.selecionar(n),lambda:self.perfil_companheiro(n)))
            if c.conversas_pessoais[n] is None: self.choice('Conversar durante a viagem',lambda:self.conversa_pessoal(n))
        else: self.choice('Adicionar à equipe',lambda:self.acao(lambda:c.selecionar(n),lambda:self.perfil_companheiro(n)))
        if n in c.recrutados:
            self.heading(self.content,d['titulo']+f' ({len(c.missoes[n])}/3)',16)
            for i,v in enumerate(c.missoes[n]): self.texto('✓ '+d['etapas'][i][2]+' — '+d['etapas'][i][4][v][2])
            e=c.etapa_missao(n)
            if e:
                self.texto('Próximo objetivo: '+e[2]+' · '+e[1]+' / '+POR_SIGNO[e[0]].nome,self.FG_TITULO)
                if c.missao_disponivel(n): self.choice('Entrar em '+e[1],lambda:self.missao(n))
                elif c.local!=e[0]: self.choice('Viajar para '+POR_SIGNO[e[0]].nome,lambda:self.viagem(e[0]))
                else: self.texto('Selecione este companheiro e resolva qualquer encontro pendente.')
            else: self.texto('Missão concluída. O desfecho será registrado no epílogo.',self.FG_TITULO)
        self.choice('Voltar à companhia',self.vinculos)
    def conversa_pessoal(self,n):
        self.layout('Conversa — '+n); self.item_row_npc(n,n,COMPANHEIROS[n]['historia']); self.texto(CONVERSAS[n][0])
        for i,txt in enumerate(CONVERSAS[n][1]): self.choice(txt,lambda i=i:self.acao(lambda:self.c.conversa_pessoal(n,i),lambda:self.perfil_companheiro(n)))
        self.choice('Conversar depois',lambda:self.perfil_companheiro(n))
    def missao(self,n):
        c=self.c
        if not c.missao_disponivel(n): self.perfil_companheiro(n); return
        e=c.etapa_missao(n); self.layout('Conversa — missão de '+n); self.item_row_npc(n,COMPANHEIROS[n]['titulo'],f'Etapa {len(c.missoes[n])+1}/3 · {e[1]}'); self.heading(self.content,e[2],18); self.texto(e[3]); self.texto('Suas escolhas afetam o vínculo e o desfecho pessoal. Todas as classes podem completar esta missão.',self.FG_MUTED)
        for i,opt in enumerate(e[4]):
            self.choice(('[Combate] ' if i==2 else '[Diálogo] ')+opt[0],lambda i=i:self.iniciar_luta('pessoal',n) if i==2 else self.acao(lambda:c.decidir_missao(n,i),lambda:self.perfil_companheiro(n)))
        self.choice('Voltar sem decidir',lambda:self.perfil_companheiro(n))
    def npc(self,n):
        c=self.c
        if not c.npc_disponivel(n): self.vinculos(); return
        etapa=len(c.relacoes[n]); cena=NPCS[n][2][etapa]; self.layout('Conversa — '+n); tk.Label(self.content,bg=self.BG_CARD,image=self.imagem('npc_'+n)).pack(anchor='w',pady=5); self.heading(self.content,cena[0],18); self.texto(cena[1]);
        if etapa: self.texto('Ele(a) recorda sua posição anterior: '+NPCS[n][2][etapa-1][2+c.relacoes[n][-1]],self.FG_MUTED)
        for k in (0,1): self.choice(cena[2+k],lambda k=k:self.acao(lambda:c.npc_decidir(n,k),lambda:self.perfil_companheiro(n)))
        self.choice('Conversar depois',self.vinculos)
    def item_combate(self):
        if self.modo!='pve' or self.jogador_atual is not self.p1: return
        w=tk.Toplevel(self.root); w.title('Consumíveis — custo de um turno'); w.configure(bg=self.BG_CARD); w.transient(self.root); w.grab_set()
        def usar(n):
            if self.modo!='pve' or self.jogador_atual is not self.p1: w.destroy(); return
            try: msg=self.c.usar_item(n)
            except ValueError as e: messagebox.showwarning('Item',str(e),parent=w); return
            w.destroy(); self._log(msg); self._finalizar_acao_turno()
        for n,q in self.c.inventario.items():
            if n in ('Ração de viagem','Selo de passagem'): continue
            self.botao(w,f'{n} × {q} — {ITENS[n][3]}',lambda n=n:usar(n),state='normal' if q else 'disabled').pack(fill='x',padx=10,pady=5)
        self.botao(w,'Cancelar',w.destroy).pack(pady=8)

    def dialogo_grupo(self,k):
        c=self.c
        if not c.cena_disponivel(k): self.vinculos(); return
        a,b=k.split('|'); cena=PARES[k][len(c.cenas_grupo[k])+1]; self.layout('Conversa — '+cena[0])
        self.item_row_npc(a,a,cena[1],True); self.item_row_npc(b,b,cena[2],True)
        self.texto('Medie o conflito ou tome partido. As respostas afetam a afinidade e a relação entre os dois.',self.FG_MUTED)
        for i in range(3): self.choice(cena[3+i],lambda i=i:self.acao(lambda:c.decidir_grupo(k,i),self.relacoes_equipe))
        self.choice('Conversar depois',self.relacoes_equipe)
    def masmorra(self):
        c=self.c; s=c.local; m=MASMORRAS[s]; self.modo='campanha'; self.layout('Masmorra — '+m.nome)
        # Durante a expedição, navegação e mudanças externas ficam bloqueadas.
        self.texto(m.historia); self.heading(self.content,f'Recorde: {c.recordes[s]}/10 · Chefe: {m.chefe}',16)
        ttk.Progressbar(self.content,maximum=10,value=c.recordes[s]).pack(fill='x',pady=4)
        r,a=POR_DISTRITO[s]; self.texto(f'Saque: {CATALOGO[r].nome} (8%, 12%, 18% ou 35% conforme a onda); {CATALOGO[a].nome} (15% no chefe). Rolagens independentes.',self.FG_TITULO)
        if c.ultimo_saque and c.historico_drops and c.historico_drops[-1]['signo']==s: self.texto('Última vitória: '+' / '.join(c.ultimo_saque),self.FG_TITULO)
        if s in c.conquistas:
            self.texto('✓ Conquistada. '+m.revelacao+f' Vitórias contra o chefe: {c.vitorias_chefe[s]}. Revanche disponível; apenas o saque pode se repetir.',self.FG_TITULO)
        self.texto('Dez ondas consecutivas. A vitória recupera 12 HP e 10 MP entre ondas; cada terceira onda concede suprimentos na primeira conclusão. A derrota restaura a onda atual. XP, moedas e recompensas de primeira conquista não se repetem; os drops podem ser sorteados novamente.')
        if not c.expedicao:
            tk.Label(self.content,bg=self.BG_CARD,image=self.imagem(f'enemy_{self.indice(s)}_10',True)).pack(anchor='w')
            self.texto('Equipe: '+(', '.join(c.equipe) or 'Exploração solo')+'. Monte o grupo antes de entrar.'); self.choice('Iniciar revanche' if s in c.conquistas else 'Iniciar expedição',lambda:self.acao(c.iniciar_expedicao,self.masmorra)); self.choice('Voltar ao distrito',self.mundo); return
        self.choice('Equipar relíquias entre ondas',self.reliquias)
        o=c.expedicao['onda']; self.heading(self.content,f'Onda {o}/10 — '+inimigo_onda(s,o),18)
        tk.Label(self.content,bg=self.BG_CARD,image=self.imagem(f'enemy_{self.indice(s)}_{o}',True)).pack(anchor='w')
        if o==10: self.texto(PADROES_CHEFE[s][2]+' Primeira ação prevista: '+acao_chefe(s,1)[1],self.FG_TITULO)
        self.texto(f'Chance nesta onda: {chance_raro(o)}% de equipamento raro'+(' e 15% de artefato lendário.' if o==10 else '.'))
        self.choice('Enfrentar '+inimigo_onda(s,o),lambda:self.iniciar_luta('masmorra'))
        for n,q in c.inventario.items():
            if q and n!='Selo de passagem': self.choice(f'Usar {n} × {q}',lambda n=n:self.acao(lambda:c.usar_item(n),self.masmorra))
        self.choice('Abandonar expedição (reinicia ondas)',lambda:self.acao(c.abandonar_expedicao,self.mundo) if messagebox.askyesno('Expedição','Abandonar? Recompensas já obtidas não se repetem.') else None)

    def reliquia_combate(self,rid):
        if self.modo!='pve' or self.jogador_atual is not self.p1: return
        try: msg=self.c.usar_reliquia(rid,self.p2)
        except ValueError as e: self._log(str(e)); return
        self._log(msg)
        if not self.p2.esta_vivo(): self.fim_luta(True); return
        self._atualizar_status()
    def reliquias(self):
        c=self.c; self.layout('Relíquias — equipamentos e coleção'); self.texto('Equipe um item raro e um artefato lendário simultaneamente, além da arma fabricada. Os poderes são independentes dos atributos e só funcionam uma vez por combate. Todas as classes podem usá-los.')
        for slot,label in [('equip_raro','Equipamento raro'),('equip_artefato','Artefato lendário')]:
            rid=getattr(c,slot); self.heading(self.content,label+': '+(CATALOGO[rid].nome if rid else 'Vazio'),16)
            if rid: self.choice('Desequipar '+CATALOGO[rid].nome,lambda slot=slot:self.acao(lambda:c.equipar_reliquia(None,slot),self.reliquias))
        self.heading(self.content,f'Coleção: {len(c.equipamentos)}/24',18)
        for s,(r,a) in POR_DISTRITO.items():
            self.heading(self.content,s+' — '+MASMORRAS[s].chefe,15)
            for rid in (r,a):
                obj=CATALOGO[rid]; slot='equip_raro' if rid==r else 'equip_artefato'; owned=rid in c.equipamentos; eq=getattr(c,slot)==rid
                self.item_row('loot_'+rid,('✓ ' if owned else '🔒 ')+obj.nome+' · '+obj.raridade, obj.descricao+' '+obj.lore, 'Equipado' if eq else 'Equipar' if owned else 'Não obtido',lambda rid=rid,slot=slot:self.acao(lambda:c.equipar_reliquia(rid,slot),self.reliquias),'normal' if owned and not eq else 'disabled')
        self.choice('Voltar à expedição' if c.expedicao else 'Voltar à mochila',self.masmorra if c.expedicao else self.mochila)
    def alternar_audio(self):
        self.audio.alternar()
    def config_audio(self,voltar):
        import webbrowser
        self._limpar_tela(); f=tk.Frame(self.root,bg=self.BG_CARD,padx=24,pady=18); f.pack(fill='both',expand=True)
        self.heading(f,'Áudio — trilha adaptativa'); status=self.label(f,self.audio.status(),12); status.pack(anchor='w')
        def alternar(): self.audio.alternar(); status.config(text=self.audio.status())
        self.botao(f,'Ativar / desativar música',alternar).pack(anchor='w',pady=6)
        self.label(f,'Volume (requer pygame)').pack(anchor='w'); scale=tk.Scale(f,from_=0,to=100,orient='horizontal',command=self.audio.ajustar); scale.set(round(self.audio.volume*100)); scale.pack(fill='x')
        self.label(f,'Trilhas oficiais opcionais: execute BAIXAR_BGM.bat. As provisórias originais já acompanham o jogo.',11,wraplength=850,justify='left').pack(anchor='w',pady=8)
        self.label(f,'Kevin MacLeod (incompetech.com) — CC BY 4.0',12).pack(anchor='w')
        for k,(nome,_) in TRILHAS.items():
            self.botao(f,k+' — '+nome,lambda k=k:webbrowser.open(fonte(k)),pady=2).pack(anchor='w',pady=1)
        self.botao(f,'Voltar',voltar).pack(anchor='w',pady=8)
