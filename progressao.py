from campanha import Campanha as Base, ficha, restaurar, SAVE
from mundo import POR_SIGNO
from expansao import ITENS, MERCADOS, EVENTOS, NPCS
from pathlib import Path
import json, random

class Campanha(Base):
    def __init__(self,nome,classe,origem):
        super().__init__(nome,classe,origem)
        self.nivel=1; self.xp=0; self.pontos=0; self.inventario={k:0 for k in ITENS}; self.inventario['Tônico rubro']=1; self.inventario['Ração de viagem']=1
        self.dia=1; self.compras={}; self.eventos={}; self.evento=None; self.relacoes={k:[] for k in NPCS}; self.perguntas={}
    @property
    def xp_meta(self): return 45+25*(self.nivel-1)
    def ganhar_xp(self,n):
        self.xp+=n
        while self.xp>=self.xp_meta:
            self.xp-=self.xp_meta; self.nivel+=1; self.pontos+=2
            self.diario.append(f'Progressão: nível {self.nivel}! +2 pontos de atributo.')
    def investir(self,atributo):
        self.livre()
        if atributo not in ('forca','defesa','agilidade','vitalidade') or not self.pontos: raise ValueError('Ponto de atributo indisponível.')
        p=self.p; setattr(p,atributo,getattr(p,atributo)+1); self.pontos-=1
        if atributo=='vitalidade': p.vida_maxima=p.vitalidade*5; p.vida+=5
        if atributo=='agilidade': p.mana_maxima=20+p.agilidade*2; p.mana+=2
    def iniciar(self,escolha):
        super().iniciar(escolha); self.ganhar_xp(15)
    def viajar(self,signo):
        novo=signo not in self.visitados; mudou=signo!=self.local
        if self.evento: raise ValueError('Decida o encontro atual antes de viajar.')
        super().viajar(signo)
        if mudou:
            self.dia+=1
            if novo: self.ganhar_xp(12)
            self.sortear_evento()
    def ler(self):
        novo=self.local not in self.lidos; super().ler()
        if novo: self.ganhar_xp(10)
    def coletar(self):
        msg=super().coletar(); self.ganhar_xp(8); return msg
    def _concluir_local(self,signo,modo):
        super()._concluir_local(signo,modo); self.ganhar_xp(40)
    def _concluir_final(self,modo):
        super()._concluir_final(modo); self.ganhar_xp(70)
    def fabricar(self,nome):
        super().fabricar(nome); self.ganhar_xp(12)
    def resolver(self,modo):
        if self.evento: raise ValueError('Decida o encontro primeiro.')
        e=super().resolver(modo)
        if e: self.pendente['itens']=dict(self.inventario); self.escalar(e)
        return e
    def encerrar(self,modo):
        if self.evento: raise ValueError('Decida o encontro primeiro.')
        e=super().encerrar(modo)
        if e: self.pendente['itens']=dict(self.inventario); self.escalar(e)
        return e
    def escalar(self,e):
        # Enemy adaptation is deliberately slower than player growth.
        bonus=min(10,(self.nivel-1)//2)
        for k in ('forca','defesa','agilidade','vitalidade'): setattr(e,k,getattr(e,k)+bonus)
        e.vida=e.vida_maxima=e.vitalidade*5; e.mana=e.mana_maxima=20+e.agilidade*2
    def resultado_combate(self,vitoria):
        if self.pendente and not vitoria: self.inventario=dict(self.pendente.get('itens',self.inventario))
        super().resultado_combate(vitoria)
    def descansar(self):
        super().descansar(); self.dia+=1
    def oferta(self,loja):
        if loja not in (0,1): raise ValueError('Mercado inválido.')
        d=POR_SIGNO[self.local]; nomes=list(ITENS)
        if loja==0: return {nomes[0]:7,nomes[3]:3,nomes[4]:5,d.material:4}
        # Unique special by district, with local discount.
        i=list(POR_SIGNO).index(self.local); especial=nomes[i%3]
        itens={nomes[1]:7,nomes[2]:12,nomes[3]:3,especial:ITENS[especial][2]-2,d.material:5}
        return itens
    def estoque(self,loja,nome): return max(0,3-self.compras.get(f'{self.dia}:{self.local}:{loja}:{nome}',0))
    def comprar(self,loja,nome):
        self.livre(); oferta=self.oferta(loja)
        if nome not in oferta or not self.estoque(loja,nome): raise ValueError('Produto esgotado ou indisponível.')
        preco=oferta[nome]
        if self.ouro<preco: raise ValueError('Moedas insuficientes.')
        self.ouro-=preco; key=f'{self.dia}:{self.local}:{loja}:{nome}'; self.compras[key]=self.compras.get(key,0)+1
        alvo=self.inventario if nome in ITENS else self.materiais; alvo[nome]+=1
    def usar_item(self,nome):
        if nome not in ITENS or self.inventario.get(nome,0)<1: raise ValueError('Item indisponível.')
        tipo,n,_,_=ITENS[nome]; p=self.p
        if tipo=='selo' or (self.pendente and nome=='Ração de viagem'): raise ValueError('Este item não pode ser usado aqui.')
        hp=min(n,p.vida_maxima-p.vida) if tipo in ('vida','ambos') else 0; mp=min(n,p.mana_maxima-p.mana) if tipo in ('mana','ambos') else 0
        if hp+mp==0: raise ValueError('Não há nada para recuperar.')
        self.inventario[nome]-=1; p.vida+=hp; p.mana+=mp; return f'{nome}: +{hp} HP, +{mp} MP.'
    def sortear_evento(self):
        op=[i for i in range(2) if f'{self.local}:{i}' not in self.eventos]
        if not self.evento and op and random.random()<.65: self.evento=[self.local,random.choice(op)]
    def decidir_evento(self,escolha):
        self.livre()
        if not self.evento or escolha not in (0,1,2): raise ValueError('Evento indisponível.')
        signo,i=self.evento; e=EVENTOS[signo][i]; efeito=e[3+2*escolha] if escolha<2 else {}
        custo=-min(0,efeito.get('ouro',0)); selo=efeito.get('selo')
        if selo and not self.inventario['Selo de passagem']: custo+=4
        if self.ouro<custo: raise ValueError('Moedas insuficientes; escolha outra opção.')
        if selo and self.inventario['Selo de passagem']: self.inventario['Selo de passagem']-=1
        self.ouro+=max(0,efeito.get('ouro',0))-custo; self.reputacao[signo]+=efeito.get('rep',0)
        self.materiais[POR_SIGNO[signo].material]+=efeito.get('material',0)
        if 'item' in efeito: self.inventario[efeito['item']]+=1
        self.p.vida=max(1,self.p.vida-efeito.get('dano',0)); self.ganhar_xp(efeito.get('xp',0)); self.eventos[f'{signo}:{i}']=escolha; self.evento=None
        self.diario.append(f'Encontro — {e[0]}: '+(e[2+2*escolha] if escolha<2 else 'Segui viagem.'))
    def npc_local(self,nome):
        loc=NPCS[nome][1]; return loc[min(len(self.relacoes[nome]),2)]
    def npc_disponivel(self,nome):
        etapa=len(self.relacoes[nome]); return etapa<3 and self.local==self.npc_local(nome) and (etapa==0 or (etapa==1 and len(self.resolvidos)>=2) or (etapa==2 and bool(self.alianca)))
    def npc_decidir(self,nome,escolha):
        self.livre()
        if escolha not in (0,1) or not self.npc_disponivel(nome): raise ValueError('Conversa indisponível.')
        etapa=len(self.relacoes[nome]); cena=NPCS[nome][2][etapa]; self.relacoes[nome].append(escolha); self.ganhar_xp(15); self.reputacao[self.local]+=1
        if etapa==1: self.inventario['Selo de passagem' if escolha==0 else 'Essência lunar']+=1
        if etapa==2: self.ouro+=5
        self.diario.append(f'{nome} — {cena[0]}: {cena[2+escolha]}')
    def epilogo(self):
        texto=super().epilogo()
        if texto:
            for nome,escolhas in self.relacoes.items():
                if len(escolhas)==3: texto+=f' {nome} leva adiante seu último compromisso: {NPCS[nome][2][2][2+escolhas[-1]]}'
        return texto
    def salvar(self,path=SAVE):
        path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
        data={k:v for k,v in vars(self).items() if k not in ('p','pendente')}; data['p']=self.pendente['antes'] if self.pendente else ficha(self.p)
        if self.pendente: data['inventario']=self.pendente.get('itens',self.inventario)
        data['versao']=2; tmp=path.with_suffix('.tmp'); tmp.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8'); tmp.replace(path)
    @classmethod
    def carregar(cls,path=SAVE):
        data=json.loads(Path(path).read_text(encoding='utf-8')); versao=data.pop('versao'); p=data.pop('p')
        if versao not in (1,2): raise ValueError('Salvamento incompatível.')
        obj=cls(p['nome'],p['classe'],data['origem']); obj.__dict__.update(data); obj.p=restaurar(p)
        if versao==1:
            obj.ganhar_xp((15 if obj.prologo else 0)+12*max(0,len(obj.visitados)-1)+10*len(obj.lidos)+8*sum(obj.coletados.values())+40*len(obj.resolvidos)+12*len(obj.armas)+(70 if obj.final else 0))
            obj.diario.append('Salvamento atualizado: experiência retroativa aplicada, atributos originais preservados.')
        return obj
