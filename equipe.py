"""V4: grupo, relações entre aliados e expedições persistentes."""
import json
from itertools import combinations
from pathlib import Path
from companheiros import Campanha as Base, COMPANHEIROS, CONVERSAS, SAVE, ficha, restaurar, Personagem
from campanha import Campanha as Original
from progressao import Campanha as V2
from masmorras import MASMORRAS, CLASSES_ONDA, inimigo_onda
from mundo import POR_SIGNO

# Par, tensão inicial, duas cenas: título, fala de cada NPC, três respostas e consequências.
PARES={
'Ione|Raska': (5,('Uma ordem ou uma prova','Ione: “Se entregarmos o registro à guarda, podemos perder a única cópia.”','Raska: “Se agirmos sozinhas, a testemunha fica sem escolta.”','Copiar o registro e organizar escolta com guardas de confiança.','Entregar o original à Vigília.','Manter tudo fora da guarda.'),('O preço de uma assinatura','Ione: “Um uniforme não absolve quem assinou as ordens.”','Raska: “Concordo. Mas não condene os recrutas junto com os oficiais.”','Separar responsabilidades individuais e proteger os recrutas.','Defender a responsabilidade coletiva da guarda.','Deixar a investigação exclusivamente com Raska.')),
'Ione|Vesper': (0,('Nomes no papel','Ione: “Sem nomes, a denúncia pode ser contestada.”','Vesper: “Com nomes, pessoas podem desaparecer.”','Guardar os nomes sob custódia e publicar apenas as provas.','Publicar todos os nomes.','Ocultar todos os registros.'),('A segunda cópia','Ione: “Precisamos de um arquivo que sobreviva a nós.”','Vesper: “E de alguém que saiba quando não abrir esse arquivo.”','Criar um arquivo selado com acesso independente.','Dar a Ione acesso irrestrito.','Deixar a rede decidir quem pode ler.')),
'Ione|Maelis': (10,('A verdade no tribunal','Ione: “A população precisa saber o que aconteceu.”','Maelis: “E os acusados precisam de um julgamento, não de uma multidão.”','Publicar os fatos verificados e preservar o direito de defesa.','Publicar as acusações imediatamente.','Manter o caso inteiramente em segredo.'),('O arquivo dos inocentes','Ione: “As famílias merecem as páginas que perderam.”','Maelis: “Algumas páginas contêm dados que podem feri-las outra vez.”','Devolver os registros com consentimento das famílias.','Abrir todos os registros.','Restringir o acesso ao tribunal.')),
'Raska|Vesper': (-25,('A lanterna e a espada','Raska: “Uma rota sem fiscalização pode servir aos sequestradores.”','Vesper: “A última fiscalização levou meu irmão à dívida.”','Fiscalizar cargas, não identidades; investigar abusos.','Autorizar inspeções sem exceção.','Proibir qualquer fiscalização.'),('Quem guarda a saída','Raska: “Posso proteger a rota, mas preciso conhecer o caminho.”','Vesper: “Promessas de oficiais já custaram vidas.”','Organizar escolta com um contato escolhido pela rede.','Dar a Raska todos os mapas.','Dispensar a escolta militar.')),
'Raska|Maelis': (0,('O dever de recusar','Raska: “Às vezes precisamos agir antes que chegue a ordem.”','Maelis: “E precisamos responder pelo que fazemos sem ela.”','Registrar decisões de emergência para revisão posterior.','Dar autonomia total à guarda.','Exigir autorização prévia mesmo em emergência.'),('A capitã e a juíza','Raska: “Meus soldados não confiam no tribunal.”','Maelis: “Eles têm razões. Quero ouvi-los sem seus superiores presentes.”','Organizar depoimentos protegidos e voluntários.','Deixar a guarda selecionar testemunhas.','Obrigar todos a depor publicamente.')),
'Vesper|Maelis': (-20,('A lei e a dívida','Vesper: “O contrato era legal. Foi assim que prenderam Lio.”','Maelis: “Legalidade não basta para tornar um contrato legítimo.”','Investigar coerção e oferecer defesa gratuita.','Invalidar todo contrato sem revisão.','Defender apenas os contratos já reconhecidos pelo tribunal.'),('O nome da testemunha','Vesper: “Ela não falará se tiver de revelar quem é.”','Maelis: “A defesa precisa poder contestar o relato.”','Usar depoimento protegido com revisão por juiz neutro.','Aceitar a acusação sem possibilidade de contestação.','Exigir que a testemunha revele sua identidade em público.')),
}

def chave(a,b): return '|'.join(sorted((a,b),key=list(COMPANHEIROS).index))

class Campanha(Base):
    def __init__(self,nome,classe,origem):
        super().__init__(nome,classe,origem)
        self.equipe=[]; self.vinculos_grupo={k:v[0] for k,v in PARES.items()}; self.cenas_grupo={k:[] for k in PARES}
        self.expedicao=None; self.recordes={s:0 for s in MASMORRAS}; self.conquistas=[]
    def livre(self):
        super().livre()
        if self.expedicao: raise ValueError('Conclua ou abandone a expedição antes de sair da masmorra.')
    def _sincronizar(self): self.ativo=self.equipe[0] if self.equipe else None
    def recrutar(self,n):
        super().recrutar(n)
        if len(self.equipe)<3: self.equipe.append(n)
        self._sincronizar()
    def selecionar(self,n):
        self.vinculo_livre()
        if n not in self.recrutados: raise ValueError('Companheiro ainda não recrutado.')
        if n in self.equipe: self.equipe.remove(n)
        elif len(self.equipe)>=3: raise ValueError('Equipe cheia: retire um membro antes de adicionar outro.')
        else: self.equipe.append(n)
        self._sincronizar()
    def npc_local(self,n): return self.local if n in self.equipe else V2.npc_local(self,n)
    def conversa_pessoal(self,n,escolha):
        self.vinculo_livre()
        if n not in self.equipe: raise ValueError('Adicione o companheiro à equipe.')
        anterior=self.ativo; self.ativo=n
        try: return super().conversa_pessoal(n,escolha)
        finally: self.ativo=anterior
    def missao_disponivel(self,n):
        e=self.etapa_missao(n)
        return bool(e and n in self.equipe and self.local==e[0] and not self.pendente and not self.evento and not self.expedicao and self.prologo)
    def pares_ativos(self): return [chave(a,b) for a,b in combinations(self.equipe,2)]
    def relacao_grupo(self,k):
        v=self.vinculos_grupo[k]; return 'Rivalidade' if v<0 else 'Cooperação' if v>=25 else 'Neutralidade'
    def cena_disponivel(self,k):
        if k not in self.pares_ativos(): return False
        n=len(self.cenas_grupo[k]); return n==0 or (n==1 and (len(self.resolvidos)>=2 or any(self.recordes.values())))
    def decidir_grupo(self,k,op):
        self.vinculo_livre()
        if not self.cena_disponivel(k) or op not in (0,1,2): raise ValueError('Diálogo indisponível.')
        a,b=k.split('|'); cena=PARES[k][len(self.cenas_grupo[k])+1]; self.cenas_grupo[k].append(op)
        delta=(25,-15,-15)[op]; self.vinculos_grupo[k]=max(-100,min(100,self.vinculos_grupo[k]+delta))
        self.alterar_afinidade(a,(5,8,-5)[op]); self.alterar_afinidade(b,(5,-5,8)[op]); self.ganhar_xp(10)
        texto=('Os dois aceitam o compromisso e combinam agir juntos.' if op==0 else f'{a} aprova a decisão; {b} discorda.' if op==1 else f'{b} aprova a decisão; {a} discorda.')
        self.diario.append(f'Companhia — {cena[0]}: {cena[3+op]} {texto}')
        return texto
    def bonus_equipe(self,n):
        vals=[self.vinculos_grupo[k] for k in self.pares_ativos() if n in k.split('|')]
        return (2 if any(v>=25 for v in vals) else 0)-(2 if any(v<0 for v in vals) else 0)
    def apoio_disponivel(self,n=None):
        if n is None: return any(self.apoio_disponivel(a) for a in self.equipe)
        return bool(self.pendente and n in self.equipe and n not in self.pendente.get('apoios_usados',[]) and self.p.esta_vivo())
    def valor_apoio(self,n): return max(1,COMPANHEIROS[n]['valores'][int(self.afinidade[n]>=70)]+self.bonus_equipe(n))
    def descricao_apoio(self,n):
        d=COMPANHEIROS[n]; v=self.valor_apoio(n); return f'{d["tecnica"]}: '+{'mana':f'+{v} MP','vida':f'+{v} HP','dano':f'{v} de dano'}[d['efeito']]+f' (coesão {self.bonus_equipe(n):+d})'
    def usar_apoio(self,inimigo,n=None):
        n=n or self.ativo
        if not self.apoio_disponivel(n) or not inimigo.esta_vivo(): raise ValueError('Apoio indisponível.')
        d=COMPANHEIROS[n]; v=self.valor_apoio(n)
        if d['efeito']=='mana': real=min(v,self.p.mana_maxima-self.p.mana); attr='mana'; msg=f'+{real} MP'
        elif d['efeito']=='vida': real=min(v,self.p.vida_maxima-self.p.vida); attr='vida'; msg=f'+{real} HP'
        else: real=min(v,inimigo.vida); attr=None; msg=f'{real} de dano'
        if not real: raise ValueError('Recurso já está cheio.')
        if attr: setattr(self.p,attr,getattr(self.p,attr)+real)
        else: inimigo.receber_dano(real)
        self.pendente.setdefault('apoios_usados',[]).append(n)
        return f'{n} — {d["tecnica"]}: {msg}. Seu turno continua.'
    def iniciar_expedicao(self):
        self.vinculo_livre()
        if self.local in self.conquistas: raise ValueError('Masmorra já conquistada.')
        self.expedicao={'signo':self.local,'onda':1,'nivel':self.nivel}; self.diario.append('Expedição iniciada: '+MASMORRAS[self.local].nome)
    def abandonar_expedicao(self):
        if self.pendente or not self.expedicao: raise ValueError('Encerre o combate antes de abandonar.')
        self.diario.append('Expedição abandonada: '+MASMORRAS[self.local].nome); self.expedicao=None
    def iniciar_onda(self):
        if not self.expedicao or self.pendente or self.expedicao['signo']!=self.local: raise ValueError('Onda indisponível.')
        o=self.expedicao['onda']; nivel=self.expedicao['nivel']; s=self.local
        e=Personagem(inimigo_onda(s,o),CLASSES_ONDA[o-1]); i=list(MASMORRAS).index(s)
        if o==10: e.classe=('Guerreiro','Paladino','Mago','Ladino')[i%4]
        # Fichas inimigas próprias; as fórmulas e a ficha do jogador continuam intocadas.
        b=min(18,(nivel-1)//2); base=6+o//2+b; e.forca=base+(3 if o==10 else 0); e.defesa=base+(2 if o==10 else 0); e.agilidade=base+(2 if e.classe=='Mago' else 0); e.vitalidade=5+o//2+b+(7 if o==10 else 0)
        e.vida=e.vida_maxima=e.vitalidade*5; e.mana=e.mana_maxima=20+2*e.agilidade
        self.pendente={'tipo':'masmorra','signo':s,'onda':o,'antes':ficha(self.p),'itens':dict(self.inventario)}; return e
    def resultado_combate(self,vitoria):
        caso=self.pendente
        if not caso: raise ValueError('Nenhum confronto em curso.')
        usados=caso.get('apoios_usados',[])
        if caso['tipo']!='masmorra': super().resultado_combate(vitoria)
        else:
            self.pendente=None
            if not vitoria: self.p=restaurar(caso['antes']); self.inventario=dict(caso['itens']); return
            s,o=caso['signo'],caso['onda']; self.p.d20_preparado=self.p.d6_preparado=None
            novo=o>self.recordes[s]
            if novo:
                self.recordes[s]=o; self.ganhar_xp(8+o if o<10 else 65); self.ouro+=2 if o<10 else 25
                if o in (3,6,9): self.materiais[POR_SIGNO[s].material]+=1; self.inventario['Tônico rubro']+=1
            if o==10:
                self.conquistas.append(s); self.reputacao[s]+=3; self.inventario['Elixir da aurora']+=2; self.expedicao=None
                self.diario.append(f'Masmorra conquistada — {MASMORRAS[s].nome}: {MASMORRAS[s].revelacao}')
            else:
                self.expedicao['onda']+=1; self.p.vida=min(self.p.vida_maxima,self.p.vida+12); self.p.mana=min(self.p.mana_maxima,self.p.mana+10)
            # Avoid farming affinity by repeating waves after abandoning.
            if not novo: usados=[]
        if vitoria:
            for n in usados: self.alterar_afinidade(n,1 if caso['tipo']=='masmorra' else 3)
    def salvar(self,path=SAVE):
        path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
        data={k:v for k,v in vars(self).items() if k not in ('p','pendente')}; data['p']=self.pendente['antes'] if self.pendente else ficha(self.p)
        if self.pendente: data['inventario']=self.pendente.get('itens',self.inventario)
        data['versao']=4; tmp=path.with_suffix('.tmp'); tmp.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8'); tmp.replace(path)
    @classmethod
    def carregar(cls,path=SAVE):
        data=json.loads(Path(path).read_text(encoding='utf-8')); v=data.get('versao')
        if v in (1,2,3):
            old=Base.carregar(path); obj=cls(old.p.nome,old.p.classe,old.origem); obj.__dict__.update(vars(old)); obj.equipe=[old.ativo] if old.ativo else []; obj._sincronizar(); return obj
        if v!=4: raise ValueError('Salvamento incompatível.')
        data.pop('versao'); p=data.pop('p'); obj=cls(p['nome'],p['classe'],data['origem']); obj.__dict__.update(data); obj.p=restaurar(p); obj._sincronizar(); return obj
