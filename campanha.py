"""Motor de campanha. A ficha e as ações de combate pertencem ao módulo original."""
import json
from pathlib import Path
from personagem import Personagem, CLASSES_DISPONIVEIS
from mundo import POR_SIGNO, RECEITAS

SAVE = Path.home() / '.the_battle' / 'campanha.json'
FICHA = ('nome','classe','forca','defesa','agilidade','vitalidade','vida_maxima','vida','mana_maxima','mana','d20_preparado','d6_preparado')

def ficha(p):
    return {k:getattr(p,k) for k in FICHA}

def restaurar(d):
    p=Personagem(d['nome'],d['classe'])
    for k in FICHA: setattr(p,k,d[k])
    return p

class Campanha:
    def __init__(self,nome,classe,origem):
        if origem not in POR_SIGNO or classe not in CLASSES_DISPONIVEIS: raise ValueError('Origem ou classe inválida.')
        self.p=Personagem(nome,classe)
        self.origem=self.local=origem
        self.ouro=24
        self.materiais={k:0 for k in ('Ferro','Madeira','Couro','Cristal')}
        self.visitados=[origem]; self.lidos=[]; self.coletados={}; self.resolvidos={}; self.reputacao={k:0 for k in POR_SIGNO}
        self.armas=[]; self.equipada=None
        self.prologo=None; self.alianca=None; self.final=None
        self.diario=[]; self.pendente=None
    def iniciar(self,escolha):
        if self.prologo: raise ValueError('Prólogo já concluído.')
        if escolha not in ('testemunhar','sigilo','investigar'): raise ValueError('Escolha inválida.')
        self.prologo=escolha
        if escolha=='testemunhar': self.reputacao[self.origem]+=1
        if escolha=='sigilo': self.ouro+=4
        if escolha=='investigar': self.materiais['Cristal']+=1
        self.diario.append('Prólogo: '+{'testemunhar':'Assinei a denúncia pública de Ione.','sigilo':'Protegi a identidade de Ione.','investigar':'Guardei o fragmento do astrolábio.'}[escolha])
    def livre(self):
        if self.pendente: raise ValueError('Resolva o confronto primeiro.')
        if not self.prologo: raise ValueError('Conclua o prólogo.')
    def viajar(self,signo):
        self.livre()
        if signo not in POR_SIGNO: raise ValueError('Distrito inválido.')
        self.local=signo
        if signo not in self.visitados: self.visitados.append(signo)
    def ler(self):
        self.livre()
        if self.local not in self.lidos:
            self.lidos.append(self.local); self.diario.append('Arquivo consultado: '+POR_SIGNO[self.local].arquivo)
    def coletar(self):
        self.livre(); d=POR_SIGNO[self.local]
        n=self.coletados.get(self.local,0)
        if n>=2: raise ValueError('As duas encomendas desta oficina já foram concluídas.')
        self.coletados[self.local]=n+1; self.materiais[d.material]+=2; self.ouro+=3
        return f'Encomenda concluída: +2 {d.material}, +3 moedas. ({n+1}/2)'
    def custo_acordo(self):
        d=POR_SIGNO[self.local]
        return 9 if self.p.classe==d.classe_fraca else 5
    def resolver(self,modo):
        self.livre(); d=POR_SIGNO[self.local]
        if self.local in self.resolvidos: raise ValueError('Caso já resolvido.')
        if modo=='combate':
            self.pendente={'tipo':'local','signo':self.local,'antes':ficha(self.p)}
            return Personagem(d.inimigo,d.classe_inimigo)
        if modo=='classe':
            if self.p.classe!=d.classe_forte: raise ValueError('Sua classe não tem acesso a este atalho.')
        elif modo=='acordo':
            custo=self.custo_acordo()
            if self.ouro<custo: raise ValueError('Moedas insuficientes. Trabalhe na oficina ou escolha outra abordagem.')
            self.ouro-=custo
        else: raise ValueError('Abordagem inválida.')
        self._concluir_local(self.local,modo)
    def _concluir_local(self,signo,modo):
        d=POR_SIGNO[signo]; self.resolvidos[signo]=modo
        self.reputacao[signo]+=2 if modo=='classe' else 1
        self.ouro+=7 if modo=='combate' else 4
        self.materiais[d.material]+=1
        self.diario.append(f'{d.nome}: {d.prova} ({modo}). {d.retorno}')
    def categorias(self):
        return {POR_SIGNO[k].categoria for k in self.resolvidos}
    def audiencia_liberada(self):
        return self.categorias()=={'ordens','suprimentos','testemunhos'}
    def apoio(self):
        return sum(1 for m in self.resolvidos.values() if m!='combate')
    def escolher_alianca(self,alianca):
        self.livre()
        if not self.audiencia_liberada() or self.alianca: raise ValueError('Audiência indisponível.')
        if alianca not in ('Liga dos Doze','Pacto dos Faróis','Câmara do Meridiano'): raise ValueError('Aliança inválida.')
        self.alianca=alianca; self.diario.append('Audiência: declarei apoio a '+alianca+'.')
    def final_pacifico_liberado(self):
        return self.apoio()>=3 and len(self.resolvidos)>=4
    def encerrar(self,modo):
        self.livre()
        if not self.alianca or self.final: raise ValueError('Desfecho indisponível.')
        if modo=='acordo':
            if not self.final_pacifico_liberado(): raise ValueError('Obtenha 4 provas e 3 resoluções não violentas.')
            self._concluir_final(modo)
        elif modo=='combate':
            self.pendente={'tipo':'final','antes':ficha(self.p)}
            return Personagem('Regente Cassian','Mago')
        else: raise ValueError('Desfecho inválido.')
    def _concluir_final(self,modo):
        self.final=modo; self.diario.append(f'Conjunção: {modo}; {self.alianca} assume a reconstrução.')
    def epilogo(self):
        if not self.final: return ''
        base={'Liga dos Doze':'O controle das torres passa às assembleias. Nenhum distrito pode suspender água ou grãos sem votação; as primeiras negociações duram semanas.', 'Pacto dos Faróis':'A rede de serviços assume a manutenção sob fiscalização pública. Os contratos se tornam acessíveis, embora os antigos nobres contestem a perda de influência.', 'Câmara do Meridiano':'A administração central sobrevive sob novas auditorias e limites de mandato. As reparações avançam rápido, mas os bairros temem a volta dos decretos secretos.'}[self.alianca]
        return ('Cassian entrega a chave quando seus operadores recusam a ordem de ativação. ' if self.final=='acordo' else 'Derrotado, Cassian entrega a chave; os técnicos desligam o astrolábio. ')+base+f' As ruas voltam a ficar abertas. O arquivo reúne agora {len(self.resolvidos)} casos resolvidos.'
    def resultado_combate(self,vitoria):
        if not self.pendente: raise ValueError('Nenhum confronto em curso.')
        caso=self.pendente; self.pendente=None
        if not vitoria:
            self.p=restaurar(caso['antes']); return
        self.p.d20_preparado=self.p.d6_preparado=None
        if caso['tipo']=='local': self._concluir_local(caso['signo'],'combate')
        else: self._concluir_final('combate')
    def descansar(self):
        self.livre()
        if self.ouro<3: raise ValueError('O descanso custa 3 moedas.')
        self.ouro-=3; self.p.vida=self.p.vida_maxima; self.p.mana=self.p.mana_maxima
    def fabricar(self,nome):
        self.livre()
        if nome not in RECEITAS or nome in self.armas: raise ValueError('Receita inválida ou arma já fabricada.')
        req=RECEITAS[nome][0]
        if any(self.materiais[k]<v for k,v in req.items()): raise ValueError('Materiais insuficientes.')
        for k,v in req.items(): self.materiais[k]-=v
        self.armas.append(nome); self.equipada=nome
    def equipar(self,nome):
        self.livre()
        if nome is not None and nome not in self.armas: raise ValueError('Arma não fabricada.')
        self.equipada=nome
    def salvar(self,path=SAVE):
        path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
        data={k:v for k,v in vars(self).items() if k not in ('p','pendente')}
        data['p']=self.pendente['antes'] if self.pendente else ficha(self.p)
        data['versao']=1
        tmp=path.with_suffix('.tmp'); tmp.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8'); tmp.replace(path)
    @classmethod
    def carregar(cls,path=SAVE):
        data=json.loads(Path(path).read_text(encoding='utf-8'))
        if data.pop('versao')!=1: raise ValueError('Versão de salvamento incompatível.')
        p=data.pop('p'); obj=cls(p['nome'],p['classe'],data['origem'])
        if set(data)!=set(vars(obj))-{'p','pendente'}: raise ValueError('Salvamento incompleto.')
        obj.__dict__.update(data); obj.p=restaurar(p); return obj
