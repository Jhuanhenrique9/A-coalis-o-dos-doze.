import unittest, tempfile
from pathlib import Path
from unittest.mock import patch
from itertools import combinations
from equipe import Campanha, COMPANHEIROS, PARES, chave
from companheiros import Campanha as V3
from campanha import ficha
from masmorras import MASMORRAS, PADROES_CHEFE, acao_chefe
from personagem import CLASSES_DISPONIVEIS

class V4Tests(unittest.TestCase):
    def novo(self,classe='Guerreiro',s='Áries'):
        c=Campanha('Teste',classe,s); c.iniciar('sigilo'); return c
    def recrutar_todos(self,c):
        for n in COMPANHEIROS:
            c.viajar(c.npc_local(n)); c.npc_decidir(n,0); c.recrutar(n)
    @patch('progressao.random.random',return_value=1)
    def test_equipes(self,_):
        c=self.novo(); self.recrutar_todos(c); self.assertEqual(len(c.equipe),3); self.assertEqual(len(c.recrutados),4)
        with self.assertRaises(ValueError): c.selecionar('Maelis')
        c.selecionar('Ione'); c.selecionar('Maelis'); self.assertEqual(c.equipe,['Raska','Vesper','Maelis']); self.assertEqual(len(c.pares_ativos()),3)
        for n in list(c.equipe): c.selecionar(n)
        for grupo in combinations(COMPANHEIROS,3):
            for n in grupo: c.selecionar(n)
            self.assertEqual(set(c.equipe),set(grupo)); self.assertEqual(len(c.pares_ativos()),3)
            for n in grupo: c.selecionar(n)
    @patch('progressao.random.random',return_value=1)
    def test_dialogos(self,_):
        for k in PARES:
            for op in range(3):
                c=self.novo(); self.recrutar_todos(c)
                for n in list(c.equipe): c.selecionar(n)
                a,b=k.split('|'); c.selecionar(a); c.selecionar(b); old=c.vinculos_grupo[k]; inicial=ficha(c.p)
                c.decidir_grupo(k,op); self.assertEqual(c.vinculos_grupo[k],old+(25,-15,-15)[op]); self.assertFalse(c.cena_disponivel(k)); c.recordes['Áries']=1
                self.assertTrue(c.cena_disponivel(k)); c.decidir_grupo(k,0); self.assertFalse(c.cena_disponivel(k)); self.assertEqual(ficha(c.p),inicial)
                with self.assertRaises(ValueError): c.decidir_grupo(k,0)
    @patch('progressao.random.random',return_value=1)
    def test_tres_apoios_e_missao(self,_):
        c=self.novo(); self.recrutar_todos(c); c.viajar('Áries'); e=c.resolver('combate'); c.p.vida-=30; c.p.mana-=30; old=dict(c.afinidade)
        for n in c.equipe: c.usar_apoio(e,n); self.assertFalse(c.apoio_disponivel(n))
        with self.assertRaises(ValueError): c.usar_apoio(e,'Maelis')
        c.resultado_combate(True)
        for n in c.equipe: self.assertEqual(c.afinidade[n],old[n]+3)
        c.viajar(c.etapa_missao('Vesper')[0]); self.assertTrue(c.missao_disponivel('Vesper')); c.decidir_missao('Vesper',0); self.assertEqual(c.missoes['Vesper'],[0])
        c.conversa_pessoal('Vesper',0)
    def test_120_ondas_todas_classes(self):
        for cl in CLASSES_DISPONIVEIS:
            for s,m in MASMORRAS.items():
                c=self.novo(cl,s); inicial=ficha(c.p); c.iniciar_expedicao(); names=[]
                for o in range(1,11):
                    e=c.iniciar_onda(); names.append(e.nome); self.assertEqual(c.pendente['onda'],o); self.assertTrue(e.esta_vivo()); c.resultado_combate(True); self.assertEqual(c.recordes[s],o)
                self.assertEqual(len(set(names)),10); self.assertEqual(names[-1],m.chefe); self.assertEqual(c.conquistas,[s]); self.assertIsNone(c.expedicao); self.assertEqual(c.reputacao[s],3); self.assertEqual(c.ouro,24+4+18+25)
                self.assertEqual(ficha(c.p),inicial)
                with self.assertRaises(ValueError): c.iniciar_expedicao()
    def test_checkpoint_recompensas(self):
        c=self.novo(); c.iniciar_expedicao(); c.iniciar_onda(); c.resultado_combate(True); old=(c.ouro,c.xp,c.nivel); c.iniciar_onda(); antes=ficha(c.p); c.p.vida-=30; c.usar_item('Tônico rubro'); c.resultado_combate(False)
        self.assertEqual(ficha(c.p),antes); self.assertEqual(c.inventario['Tônico rubro'],1); self.assertEqual(c.expedicao['onda'],2)
        with self.assertRaises(ValueError): c.viajar('Touro')
        c.abandonar_expedicao(); c.iniciar_expedicao(); c.iniciar_onda(); c.resultado_combate(True); self.assertEqual((c.ouro,c.xp,c.nivel),old)
    def test_salvar_e_migrar(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'s.json'; old=V3('Old','Mago','Peixes'); old.iniciar('sigilo'); old.npc_decidir('Ione',0); old.recrutar('Ione'); old.salvar(p)
            c=Campanha.carregar(p); self.assertEqual(c.equipe,['Ione']); self.assertEqual(ficha(old.p),ficha(c.p)); c.iniciar_expedicao(); c.iniciar_onda(); c.resultado_combate(True); c.iniciar_onda(); antes=ficha(c.p); c.p.vida-=20; c.salvar(p); novo=Campanha.carregar(p)
            self.assertEqual(novo.expedicao['onda'],2); self.assertEqual(novo.recordes['Peixes'],1); self.assertEqual(ficha(novo.p),antes); self.assertIsNone(novo.pendente); self.assertEqual(novo.equipe,['Ione'])
    def test_artes_e_padroes(self):
        pasta=Path(__file__).with_name('artes'); self.assertEqual(set(PADROES_CHEFE),set(MASMORRAS))
        for i,s in enumerate(MASMORRAS):
            for o in range(1,11): self.assertTrue((pasta/f'enemy_{i}_{o}.png').is_file())
            for t in range(1,7): self.assertIn(acao_chefe(s,t)[1],('Golpe Poderoso','Bola de Fogo','Ataque Rápido'))
if __name__=='__main__': unittest.main()
