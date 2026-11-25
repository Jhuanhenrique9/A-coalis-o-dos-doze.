"""V5: saque independente de atributos, expedições de revanche e equipamento."""
import json, random
from pathlib import Path
from dataclasses import dataclass
from equipe import Campanha as V4, SAVE, ficha, restaurar
from masmorras import MASMORRAS

@dataclass(frozen=True)
class Equipamento:
    nome: str
    signo: str
    raridade: str
    efeitos: tuple
    lore: str
    @property
    def descricao(self):
        return ' · '.join({'vida':f'Até +{v} HP','mana':f'Até +{v} MP','dano':f'{v} de dano direto'}[k] for k,v in self.efeitos)+' — uma vez por luta, sem consumir turno.'

# Um equipamento raro e um artefato lendário para cada distrito.
_DADOS=(
('Braçadeiras da Vigília',(('dano',7),),'Selo do Marechal Oco',(('dano',18),),'A ordem original da guarnição está gravada sob o selo.'),
('Cinto dos Semeadores',(('vida',10),),'Coração da Raiz de Inverno',(('vida',25),),'Conserva o calor do primeiro moinho do distrito.'),
('Luva de Engrenagens',(('mana',9),),'Pêndulo dos Dois Ponteiros',(('mana',18),('dano',7)),'Seus ponteiros repetem a hora da mensagem adulterada.'),
('Manto de Nácar',(('vida',7),('mana',5)),'Pérola da Maré Cativa',(('vida',15),('mana',15)),'Uma corrente de água limpa permanece dentro da pérola.'),
('Manopla do Arauto',(('dano',9),),'Diadema de Bronze',(('dano',15),('vida',8)),'A inscrição obriga o regente a servir aos cidadãos.'),
('Capa de Alva',(('vida',12),),'Rosa da Vigília',(('vida',28),),'A flor não murcha mesmo sob a poeira da guerra.'),
('Broche do Magistrado',(('vida',8),('mana',4)),'Prato da Balança Cega',(('vida',16),('dano',9)),'Os nomes esquecidos aparecem na superfície polida.'),
('Botas do Véu',(('dano',8),),'Ferrão de Vidro',(('dano',22),),'A luz da lanterna negra se reflete no cristal.'),
('Aljava de Freixo',(('dano',6),('mana',4)),'Bússola Sem Norte',(('dano',14),('mana',10)),'Aponta para a estrada que salvou a última caravana.'),
('Peitoral de Basalto',(('vida',14),),'Núcleo da Fornalha',(('vida',20),('dano',8)),'O metal retém a última advertência dos mineiros.'),
('Anel da Condensação',(('mana',12),),'Prisma da Tempestade',(('mana',25),),'Um relâmpago minúsculo percorre as faces do prisma.'),
('Amuleto do Barqueiro',(('vida',6),('mana',6)),'Concha dos Sonhos Náufragos',(('vida',18),('mana',12)),'As vozes dos viajantes finalmente descansam.'),
)
CATALOGO={}; POR_DISTRITO={}
for i,(s,(r,re,a,ae,lore)) in enumerate(zip(MASMORRAS,_DADOS)):
    rk=f'r{i}'; ak=f'a{i}'; POR_DISTRITO[s]=(rk,ak)
    CATALOGO[rk]=Equipamento(r,s,'Raro',re,'Equipamento recuperado de '+MASMORRAS[s].nome+'.')
    CATALOGO[ak]=Equipamento(a,s,'Lendário',ae,lore)

def chance_raro(onda):
    if onda not in range(1,11): raise ValueError('Onda inválida.')
    return 8 if onda<=3 else 12 if onda<=6 else 18 if onda<=9 else 35
CHANCE_ARTEFATO=15

class Campanha(V4):
    def __init__(self,nome,classe,origem):
        super().__init__(nome,classe,origem)
        self.equipamentos=[]; self.equip_raro=None; self.equip_artefato=None
        self.historico_drops=[]; self.vitorias_chefe={s:0 for s in MASMORRAS}; self.ultimo_saque=[]
    def iniciar_expedicao(self):
        if self.local not in self.conquistas: return super().iniciar_expedicao()
        self.vinculo_livre(); self.expedicao={'signo':self.local,'onda':1,'nivel':self.nivel,'revanche':True}
        self.diario.append('Revanche iniciada: '+MASMORRAS[self.local].nome)
    def equipar_reliquia(self,id,slot):
        if self.pendente or not self.prologo or self.evento: raise ValueError('Equipamento indisponível neste momento.')
        if slot not in ('equip_raro','equip_artefato'): raise ValueError('Espaço inválido.')
        if id is not None and (id not in self.equipamentos or id not in CATALOGO or (CATALOGO[id].raridade=='Raro')!=(slot=='equip_raro')): raise ValueError('Equipamento não adquirido ou espaço incorreto.')
        setattr(self,slot,id)
    def reliquias_ativas(self): return [i for i in (self.equip_raro,self.equip_artefato) if i in CATALOGO]
    def reliquia_disponivel(self,i):
        return bool(self.pendente and i in self.reliquias_ativas() and i not in self.pendente.get('reliquias_usadas',[]) and self.p.esta_vivo())
    def usar_reliquia(self,i,e):
        if not self.reliquia_disponivel(i) or not e.esta_vivo(): raise ValueError('Relíquia indisponível.')
        efeitos=[]
        for k,v in CATALOGO[i].efeitos:
            if k=='dano': real=min(v,e.vida); e.receber_dano(real); efeitos.append(f'{real} de dano')
            else:
                maximo=getattr(self.p,k+'_maxima'); atual=getattr(self.p,k); real=min(v,maximo-atual); setattr(self.p,k,atual+real); efeitos.append(f'+{real} '+('HP' if k=='vida' else 'MP'))
        if not any(not x.startswith('+0 ') for x in efeitos): raise ValueError('Recursos já estão cheios.')
        self.pendente.setdefault('reliquias_usadas',[]).append(i)
        return CATALOGO[i].nome+': '+', '.join(efeitos)+'. Seu turno continua.'
    def _sortear_saque(self,s,o):
        r,a=POR_DISTRITO[s]; resultados=[]
        if random.random()*100<chance_raro(o): resultados.append(r)
        if o==10 and random.random()*100<CHANCE_ARTEFATO: resultados.append(a)
        for i in resultados:
            if i in self.equipamentos: self.ultimo_saque.append(CATALOGO[i].nome+' — duplicado, já na coleção.')
            else:
                self.equipamentos.append(i); self.ultimo_saque.append(f'{CATALOGO[i].raridade}: {CATALOGO[i].nome}')
        if not resultados: self.ultimo_saque.append('Nenhum equipamento desta vez.')
        self.historico_drops.append({'signo':s,'onda':o,'itens':resultados})
        self.diario.append(f'Saque {s}, onda {o}: '+ ' / '.join(self.ultimo_saque))
    def resultado_combate(self,vitoria):
        caso=self.pendente; self.ultimo_saque=[]
        if not caso or caso['tipo']!='masmorra' or not vitoria: return super().resultado_combate(vitoria)
        s,o=caso['signo'],caso['onda']
        # A revanche não repete a conquista, XP, moedas, reputação, afinidade ou consumíveis.
        if o==10 and s in self.conquistas:
            self.pendente=None; self.p.d20_preparado=self.p.d6_preparado=None; self.expedicao=None
            self.diario.append('Chefe derrotado novamente: '+MASMORRAS[s].chefe)
        else: super().resultado_combate(True)
        if o==10: self.vitorias_chefe[s]+=1
        self._sortear_saque(s,o)
    def salvar(self,path=SAVE):
        path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
        data={k:v for k,v in vars(self).items() if k not in ('p','pendente')}; data['p']=self.pendente['antes'] if self.pendente else ficha(self.p)
        if self.pendente: data['inventario']=self.pendente.get('itens',self.inventario)
        data['versao']=5; tmp=path.with_suffix('.tmp'); tmp.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8'); tmp.replace(path)
    @classmethod
    def carregar(cls,path=SAVE):
        data=json.loads(Path(path).read_text(encoding='utf-8'))
        if data.get('versao') in (1,2,3,4):
            old=V4.carregar(path); obj=cls(old.p.nome,old.p.classe,old.origem); obj.__dict__.update(vars(old)); obj.vitorias_chefe.update({s:1 for s in old.conquistas}); return obj
        if data.pop('versao',None)!=5: raise ValueError('Salvamento incompatível.')
        p=data.pop('p'); obj=cls(p['nome'],p['classe'],data['origem']); obj.__dict__.update(data); obj.p=restaurar(p); obj._sincronizar(); return obj
