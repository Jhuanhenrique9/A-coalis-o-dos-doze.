"""V3: companhia, afinidade e missões. Sem alterações no Personagem original."""
from pathlib import Path
import json
from progressao import Campanha as Base, SAVE, ficha, restaurar
from personagem import Personagem
from expansao import NPCS
from mundo import POR_SIGNO

# Cada etapa: distrito, local, título, cena, escolhas (texto, afinidade, consequência).
# A terceira opção da etapa intermediária, quando presente, inicia confronto.
COMPANHEIROS = {
 'Ione': dict(papel='Apoio arcano', tecnica='Memória do astrolábio', efeito='mana', valores=(12,20), historia='A arquivista foi aprendiz de um copista que desapareceu durante a Guerra das Cinzas. Ela teme que preservar a verdade custe a vida de quem a conta.', preferencia='Protege fontes e favorece divulgação responsável.', ganhos=(20,15, 18,12, 17,18), titulo='O nome que não consta', inimigo=('Custódio do arquivo','Mago'), inicio_luta='O custódio tenta destruir as páginas e lança uma runa contra vocês. Ione protege o livro enquanto você o enfrenta.', etapas=[
 ('Peixes','Casa dos Copistas','A carta sem remetente','Ione encontra uma carta do seu antigo mestre, Orven. Ele registrou famílias deslocadas durante a guerra, mas seu nome foi apagado dos créditos. A filha de uma testemunha pede que seu endereço não seja divulgado.', [('Preservar a carta com os dados pessoais lacrados.',12,'Ione aceita separar a identidade das provas. A filha entrega a chave de um depósito em Gêmeos.'),('Registrar a carta integralmente sob custódia judicial.',4,'Ione teme a exposição, mas a custódia oferece proteção. A chave do depósito é registrada no processo.')]),
 ('Gêmeos','Depósito dos Relógios','As páginas confiscadas','O custódio admite receber ordens para destruir os livros de Orven. Diz que sua família perderá a moradia se desobedecer. Os livros provam que os cadastros de refugiados foram usados para esconder remessas ao observatório.', [('Oferecer proteção ao custódio e copiar os livros.',15,'O homem entrega as cópias e aceita depor sob proteção.'),('Solicitar uma apreensão formal aos cartógrafos.',7,'O depósito é lacrado e os cartógrafos autenticam os livros.'),('Impedir a destruição dos livros pela força.',3,'O custódio é desarmado. Ione recolhe as páginas e chama os cartógrafos.')]),
 ('Libra','Sala dos Registros','A autoria devolvida','Maelis oferece uma audiência. Orven poderá ser reconhecido, mas divulgar os nomes de todas as famílias colocaria algumas delas em risco. Ione pede sua opinião antes de apresentar as cópias.', [('Publicar a autoria e proteger as identidades.',20,'Orven é reconhecido. Ione funda um arquivo de acesso público com proteção de fontes.'),('Entregar os registros completos a um tribunal independente.',10,'O tribunal preserva os registros originais e autoriza acesso mediante justificativa.')])]),
 'Raska': dict(papel='Vanguarda', tecnica='Investida da Vigília', efeito='dano', valores=(9,15), historia='A capitã carrega uma lista de recrutas que não regressaram de uma escolta. Seu antigo comandante assinou a ordem e ela ainda se culpa por tê-la obedecido.', preferencia='Prioriza civis, responsabilidade individual e proteção dos recrutas.', ganhos=(20,15, 20,10, 17,17), titulo='O peso do juramento', inimigo=('Sargento da escolta','Guerreiro'), inicio_luta='O sargento recusa a ordem de parada e avança contra uma recruta. Raska conduz os civis para trás da barricada enquanto você o enfrenta.', etapas=[
 ('Áries','Quartel da Brasa','Os nomes na muralha','Uma recruta entrega a Raska uma lista de desaparecidos. Entre eles está seu irmão. A capitã reconhece a assinatura de seu mentor, comandante Harun, e confessa ter autenticado parte das ordens sem verificar os destinos.', [('Ouvir os familiares antes de acusar Harun.',14,'Raska admite sua parcela de responsabilidade diante das famílias.'),('Notificar imediatamente o comando e pedir investigação.',5,'Raska aceita a investigação, embora tema represálias antes de reunir provas.')]),
 ('Sagitário','Posto da Estrada Velha','A escolta esquecida','A lista leva a uma estação de caravanas. Um sargento mantém antigos recrutas trabalhando sob ameaça de prisão por deserção. Há uma passagem lateral que os guias conhecem.', [('Negociar a saída dos recrutas com os guias.',15,'Os recrutas saem com testemunhas e o sargento perde o controle da escolta.'),('Apresentar os registros e convocar uma patrulha neutra.',9,'A patrulha autentica os registros e conduz o sargento ao quartel.'),('Proteger os recrutas do sargento armado.',12,'A escolta é desarmada e os recrutas são levados à hospedaria.')]),
 ('Leão','Pátio das Medalhas','Uma capitã diante do conselho','Harun admite ter cedido a pressões de financiadores para não perder a unidade. A medalha de Raska depende do silêncio dela; os recrutas exigem uma resposta.', [('Testemunhar com Raska, incluindo os erros dela.',20,'Raska devolve a medalha e participa de uma reforma de recrutamento.'),('Defender uma investigação externa, sem antecipar sentença.',12,'Uma comissão independente recebe os depoimentos; Raska aceita ser investigada.')])]),
 'Vesper': dict(papel='Infiltração', tecnica='Corte do Véu', efeito='dano', valores=(8,14), historia='Vesper cresceu entre mensageiros do mercado subterrâneo. Seu irmão adotivo, Lio, assumiu uma dívida para impedir que a família fosse expulsa das galerias.', preferencia='Valoriza anonimato, autonomia e proteção dos mensageiros.', ganhos=(20,15, 20,8, 18,12), titulo='Dívidas sob as lanternas', inimigo=('Cobrador das Lanternas','Ladino'), inicio_luta='O cobrador tenta levar Lio antes que o contrato seja examinado. Vesper corta a corda da passagem e você bloqueia o avanço do cobrador.', etapas=[
 ('Escorpião','Cozinha das Lanternas','A dívida de Lio','Vesper revela que Lio transportou caixas para pagar uma dívida adulterada. Um recibo mostra que o credor aumentou os juros sem testemunhas. Lio teme que seu endereço seja revelado.', [('Proteger Lio e procurar o contrato original.',14,'Vesper confia a você a localização de um antigo armazém em Câncer.'),('Registrar uma queixa nominal com proteção do magistrado.',3,'Vesper aceita a proteção, mas pede que os dados da família permaneçam fechados.')]),
 ('Câncer','Armazém da Maré Baixa','O livro das dívidas','O cobrador guarda o contrato e os comprovantes de transporte ao observatório. Ele oferece anular a dívida de Lio se os demais nomes permanecerem presos aos contratos.', [('Recusar o trato e copiar todos os contratos com testemunhas.',15,'Os barqueiros autenticam as cópias; a dívida de todas as famílias poderá ser contestada.'),('Negociar a suspensão de todas as cobranças até auditoria.',10,'O cobrador aceita a suspensão para evitar uma denúncia imediata.'),('Impedir que o cobrador leve Lio à força.',8,'O cobrador recua e os barqueiros guardam os contratos como prova.')]),
 ('Gêmeos','Correio das Sete Chaves','A rede tem um nome','Os mensageiros querem criar uma associação, mas alguns dependem do anonimato para escapar dos credores. Vesper não quer substituir uma rede de coerção por outra.', [('Criar uma associação com identidades protegidas.',20,'Vesper ajuda a fundar uma rede de mensageiros com direito a recusar encomendas.'),('Criar uma cooperativa auditada com representação eleita.',13,'Os mensageiros aprovam regras comuns de remuneração e proteção dos associados.')])]),
 'Maelis': dict(papel='Proteção e cura', tecnica='Luz do Equilíbrio', efeito='vida', valores=(14,23), historia='Maelis condenou um barqueiro com base em um decreto emergencial no início de sua carreira. A prova que o incriminava pode ter sido produzida pelo mesmo cartório que agora protege Cassian.', preferencia='Busca revisão pública, direito de defesa e independência institucional.', ganhos=(20,15, 20,12, 20,18), titulo='A sentença que permanece', inimigo=('Executor do cartório','Paladino'), inicio_luta='O executor tenta arrancar o livro da sentença das mãos da testemunha. Maelis a escolta para uma saída segura enquanto você impede a apreensão.', etapas=[
 ('Libra','Arquivo dos Recursos','O recurso esquecido','Maelis encontra uma petição de Dario, barqueiro condenado há anos. A folha foi arquivada sem resposta. Ela reconhece sua própria assinatura na sentença e procura a família.', [('Pedir a reabertura e reconhecer o erro em público.',15,'Maelis registra sua responsabilidade e solicita um juiz independente.'),('Reabrir o processo em sigilo para proteger a família.',8,'A juíza pede revisão reservada e proteção para os envolvidos.')]),
 ('Virgem','Casa de Convalescença','A testemunha viva','Eline apresenta uma testemunha da antiga apreensão. Um executor pretende confiscar o livro médico que confirma que Dario estava internado na data do crime.', [('Proteger a testemunha e autenticar uma cópia com Eline.',15,'O livro é copiado sem divulgar outros pacientes.'),('Pedir uma ordem de preservação a um magistrado neutro.',11,'O livro fica sob custódia independente; a testemunha é ouvida.'),('Impedir a apreensão forçada do livro.',7,'O executor é desarmado e o livro segue para custódia neutra.')]),
 ('Libra','Tribunal dos Recursos','Uma lei que pode falhar','O novo julgamento absolve Dario. Maelis precisa decidir se renuncia ou usa sua posição para abrir a revisão de outras sentenças emergenciais.', [('Apoiar revisão independente de todos os casos similares.',20,'Maelis cria uma comissão de revisão e se afasta dos próprios processos.'),('Apoiar a renúncia seguida de assistência jurídica pública.',13,'Maelis deixa a cadeira e passa a auxiliar famílias nos pedidos de revisão.')])]),
}


# Uma conversa de viagem distinta para cada pessoa, disponível uma única vez.
CONVERSAS = {
 'Ione': ('Ione dobra uma carta tantas vezes que o papel começa a rasgar. “Sempre me disseram que um arquivo não pertence a quem escreve. Mas, se eu desaparecer, quem protegerá os nomes?”', ('Dizer que proteger a fonte também é parte de preservar a verdade.', 'Dizer que a verdade importa mais do que a segurança de quem a conta.'), ('Ione guarda a carta com cuidado. “É bom não carregar isso sozinha.”', 'Ione fecha o caderno. “Então precisarei proteger minhas fontes sem sua ajuda.”')),
 'Raska': ('Raska limpa uma insígnia antiga perto da fogueira. “A primeira vez que desobedeci a uma ordem, salvei uma criança. A primeira vez que obedeci sem pensar, perdi um amigo.”', ('Reconhecer que coragem também é questionar uma ordem injusta.', 'Dizer que um soldado deve obedecer, independentemente das consequências.'), ('Raska assente. “É isso que quero ensinar aos próximos recrutas.”', 'Raska guarda a insígnia. “Já ouvi essas palavras antes. Não quero repeti-las.”')),
 'Vesper': ('Vesper deixa duas canecas sobre a mesa e observa a porta. “Lio me ensinou a reconhecer quem seguia nossos passos. Às vezes ainda conto as saídas antes de conseguir dormir.”', ('Oferecer companhia sem exigir que revele mais nada.', 'Insistir para que conte os esconderijos da sua rede.'), ('Vesper relaxa os ombros. “Uma pergunta a menos vale mais que uma promessa.”', 'Vesper se afasta da mesa. “Há nomes que não são meus para entregar.”')),
 'Maelis': ('Maelis relê uma sentença antiga à luz de uma lamparina. “Um selo não torna uma decisão justa. Aprendi isso tarde. Você acha que alguém como eu merece continuar julgando?”', ('Dizer que reconhecer erros exige responsabilidade e revisão independente.', 'Dizer que a autoridade do cargo basta para justificar suas decisões.'), ('Maelis fecha o documento. “Uma lei que não pode ser revista é apenas uma ordem.”', 'Maelis suspira. “Foi justamente assim que o tribunal deixou de ouvir os acusados.”')),
}

class Campanha(Base):
    def __init__(self,nome,classe,origem):
        super().__init__(nome,classe,origem)
        self.afinidade={n:0 for n in COMPANHEIROS}
        self.recrutados=[]; self.ativo=None
        self.missoes={n:[] for n in COMPANHEIROS}
        self.conversas_pessoais={n:None for n in COMPANHEIROS}
    def vinculo_livre(self):
        self.livre()
        if self.evento: raise ValueError('Decida o encontro atual antes de cuidar da companhia.')
    def alterar_afinidade(self,n,delta):
        self.afinidade[n]=max(0,min(100,self.afinidade[n]+delta))
    def grau(self,n):
        a=self.afinidade[n]
        return 'Lealdade' if a>=70 else 'Confiança' if a>=40 else 'Respeito' if a>=15 else 'Distante'
    def npc_local(self,nome):
        return self.local if self.ativo==nome else super().npc_local(nome)
    def npc_decidir(self,nome,escolha):
        self.vinculo_livre(); etapa=len(self.relacoes[nome]); super().npc_decidir(nome,escolha)
        self.alterar_afinidade(nome,COMPANHEIROS[nome]['ganhos'][etapa*2+escolha])
    def local_recrutamento(self,n):
        return NPCS[n][1][max(0,len(self.relacoes[n])-1)]
    def pode_recrutar(self,n):
        return n in COMPANHEIROS and n not in self.recrutados and bool(self.relacoes[n]) and self.afinidade[n]>=15 and self.local in (self.local_recrutamento(n),self.npc_local(n))
    def recrutar(self,n):
        self.vinculo_livre()
        if not self.pode_recrutar(n): raise ValueError('Converse primeiro, alcance 15 de afinidade e encontre o NPC no distrito indicado.')
        self.recrutados.append(n)
        if self.ativo is None: self.ativo=n
        self.diario.append(f'Companhia: {n} aceitou viajar comigo. {COMPANHEIROS[n]["titulo"]} disponível.')
    def selecionar(self,n):
        self.vinculo_livre()
        if n is not None and n not in self.recrutados: raise ValueError('Companheiro ainda não recrutado.')
        self.ativo=n
    def conversa_pessoal(self,n,escolha):
        self.vinculo_livre()
        if n!=self.ativo or n is None or self.conversas_pessoais[n] is not None or escolha not in (0,1): raise ValueError('Conversa indisponível.')
        self.conversas_pessoais[n]=escolha
        self.alterar_afinidade(n,8 if escolha==0 else -5)
        self.diario.append(f'{n} — conversa de viagem: {CONVERSAS[n][1][escolha]} {CONVERSAS[n][2][escolha]}')
        return CONVERSAS[n][2][escolha]
    def etapa_missao(self,n):
        i=len(self.missoes[n]); return COMPANHEIROS[n]['etapas'][i] if i<3 else None
    def missao_disponivel(self,n):
        e=self.etapa_missao(n)
        return bool(e and n==self.ativo and self.local==e[0] and not self.pendente and not self.evento and self.prologo)
    def decidir_missao(self,n,escolha):
        self.vinculo_livre()
        if n not in COMPANHEIROS or not self.missao_disponivel(n): raise ValueError('Ative o companheiro e visite o local da missão.')
        e=self.etapa_missao(n)
        if escolha not in range(len(e[4])): raise ValueError('Escolha inválida.')
        if escolha==2:
            self.pendente={'tipo':'pessoal','nome':n,'etapa':len(self.missoes[n]),'escolha':escolha,'antes':ficha(self.p),'itens':dict(self.inventario)}
            inimigo=Personagem(*COMPANHEIROS[n]['inimigo']); self.escalar(inimigo); return inimigo
        self._concluir_missao(n,escolha)
    def _concluir_missao(self,n,escolha):
        e=self.etapa_missao(n); texto,delta,resultado=e[4][escolha]; self.missoes[n].append(escolha)
        self.alterar_afinidade(n,delta); self.ganhar_xp(20); self.reputacao[e[0]]+=1
        self.diario.append(f'{n} — {e[2]}: {texto} {resultado}')
        if len(self.missoes[n])==3:
            self.ouro+=12; self.ganhar_xp(35); self.inventario['Elixir da aurora']+=1
            self.diario.append(f'Missão pessoal concluída: {COMPANHEIROS[n]["titulo"]}. +12 moedas, +35 XP e elixir.')
        return resultado
    def apoio_disponivel(self):
        return bool(self.pendente and self.ativo and self.ativo in self.recrutados and not self.pendente.get('apoio_usado') and self.p.esta_vivo())
    def descricao_apoio(self,n):
        d=COMPANHEIROS[n]; valor=d['valores'][int(self.afinidade[n]>=70)]
        return f'{d["tecnica"]}: '+{'mana':f'recupera até {valor} MP','vida':f'recupera até {valor} HP','dano':f'causa {valor} de dano ao inimigo'}[d['efeito']]
    def usar_apoio(self,inimigo):
        if not self.apoio_disponivel() or not inimigo.esta_vivo(): raise ValueError('Apoio indisponível.')
        n=self.ativo; d=COMPANHEIROS[n]; valor=d['valores'][int(self.afinidade[n]>=70)]
        if d['efeito']=='mana':
            real=min(valor,self.p.mana_maxima-self.p.mana)
            if not real: raise ValueError('Mana já está cheia.')
            self.p.mana+=real; msg=f'+{real} MP'
        elif d['efeito']=='vida':
            real=min(valor,self.p.vida_maxima-self.p.vida)
            if not real: raise ValueError('Vida já está cheia.')
            self.p.vida+=real; msg=f'+{real} HP'
        else:
            real=min(valor,inimigo.vida); inimigo.receber_dano(real); msg=f'{real} de dano'
        self.pendente['apoio_usado']=True
        return f'{n} — {d["tecnica"]}: {msg}. Apoio utilizado; seu turno continua.'
    def resultado_combate(self,vitoria):
        caso=self.pendente
        if not caso: raise ValueError('Nenhum confronto em curso.')
        if caso['tipo']=='pessoal':
            self.pendente=None
            if not vitoria:
                self.p=restaurar(caso['antes']); self.inventario=dict(caso['itens']); return
            self.p.d20_preparado=self.p.d6_preparado=None
            self._concluir_missao(caso['nome'],caso['escolha'])
        else: super().resultado_combate(vitoria)
        if vitoria and caso.get('apoio_usado') and self.ativo:
            self.alterar_afinidade(self.ativo,3)
            self.diario.append(f'{self.ativo}: vencemos juntos. +3 afinidade.')
    def epilogo(self):
        texto=super().epilogo()
        if texto:
            for n,escolhas in self.missoes.items():
                if len(escolhas)==3: texto+=' '+COMPANHEIROS[n]['etapas'][2][4][escolhas[2]][2]
        return texto
    def salvar(self,path=SAVE):
        path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
        data={k:v for k,v in vars(self).items() if k not in ('p','pendente')}
        data['p']=self.pendente['antes'] if self.pendente else ficha(self.p)
        if self.pendente: data['inventario']=self.pendente.get('itens',self.inventario)
        data['versao']=3; tmp=path.with_suffix('.tmp'); tmp.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8'); tmp.replace(path)
    @classmethod
    def carregar(cls,path=SAVE):
        data=json.loads(Path(path).read_text(encoding='utf-8')); versao=data.get('versao')
        if versao in (1,2):
            obj=super().carregar(path)
            for n,escolhas in obj.relacoes.items():
                obj.afinidade[n]=sum(COMPANHEIROS[n]['ganhos'][i*2+v] for i,v in enumerate(escolhas))
            obj.diario.append('V3: afinidade calculada a partir das conversas anteriores. Recrute seus aliados no painel de companhia.')
            return obj
        if versao!=3: raise ValueError('Salvamento incompatível.')
        data.pop('versao'); p=data.pop('p'); obj=cls(p['nome'],p['classe'],data['origem'])
        if set(data)!=set(vars(obj))-{'p','pendente'}: raise ValueError('Salvamento incompleto.')
        obj.__dict__.update(data); obj.p=restaurar(p); return obj
