import unittest, tempfile
from pathlib import Path
from unittest.mock import patch
from companheiros import Campanha, COMPANHEIROS
from progressao import Campanha as V2
from campanha import Campanha as V1, ficha
from personagem import CLASSES_DISPONIVEIS
from expansao import NPCS

class CompanhiaTests(unittest.TestCase):
    def novo(self,classe='Guerreiro'):
        c=Campanha('Teste',classe,'Áries'); c.iniciar('sigilo'); return c
    def recrutar(self,c,n,escolha=0):
        c.viajar(c.npc_local(n)); c.npc_decidir(n,escolha); c.recrutar(n); c.selecionar(n)
    @patch('progressao.random.random',return_value=1)
    def test_recrutar_todas_classes_e_rotas(self,_):
        for cl in CLASSES_DISPONIVEIS:
            for n in COMPANHEIROS:
                for primeira in (0,1):
                    c=self.novo(cl); inicial=ficha(c.p); self.recrutar(c,n,primeira)
                    self.assertEqual(c.ativo,n); self.assertGreaterEqual(c.afinidade[n],15)
                    for escolha in (0,1,0):
                        e=c.etapa_missao(n); c.viajar(e[0]); c.decidir_missao(n,escolha)
                    self.assertEqual(len(c.missoes[n]),3); self.assertIsNone(c.etapa_missao(n)); self.assertEqual(ficha(c.p),inicial)
                    with self.assertRaises(ValueError): c.decidir_missao(n,0)
    @patch('progressao.random.random',return_value=1)
    def test_todas_escolhas_pessoais(self,_):
        for n,d in COMPANHEIROS.items():
            for a in (0,1):
                for b in (0,1,2):
                    for z in (0,1):
                        c=self.novo(); self.recrutar(c,n)
                        for choice in (a,b,z):
                            c.viajar(c.etapa_missao(n)[0]); e=c.decidir_missao(n,choice)
                            if e: c.resultado_combate(True)
                        self.assertEqual(c.missoes[n],[a,b,z]); self.assertFalse(c.final); self.assertEqual(c.inventario['Elixir da aurora'],1)
                        self.assertLessEqual(c.afinidade[n],100)
    @patch('progressao.random.random',return_value=1)
    def test_apoios_checkpoint(self,_):
        for n,d in COMPANHEIROS.items():
            c=self.novo(); self.recrutar(c,n); c.viajar(c.etapa_missao(n)[0]); c.decidir_missao(n,0); c.viajar(c.etapa_missao(n)[0]); antes=ficha(c.p); rel=c.afinidade[n]; items=dict(c.inventario)
            e=c.decidir_missao(n,2); self.assertTrue(c.apoio_disponivel()); c.p.vida-=30; c.p.mana-=25; old=e.vida; c.usar_apoio(e)
            if d['efeito']=='dano': self.assertEqual(old-e.vida,d['valores'][0])
            if d['efeito']=='vida': self.assertEqual(c.p.vida,antes['vida']-30+d['valores'][0])
            if d['efeito']=='mana': self.assertEqual(c.p.mana,antes['mana']-25+d['valores'][0])
            with self.assertRaises(ValueError): c.usar_apoio(e)
            with self.assertRaises(ValueError): c.selecionar(None)
            c.usar_item('Tônico rubro') if c.p.vida< c.p.vida_maxima else None
            with tempfile.TemporaryDirectory() as tmp:
                path=Path(tmp)/'save.json'; c.salvar(path); r=Campanha.carregar(path); self.assertEqual(ficha(r.p),antes); self.assertEqual(r.inventario,items); self.assertEqual(r.missoes[n],[0]); self.assertIsNone(r.pendente); self.assertEqual(r.afinidade[n],rel)
            c.resultado_combate(False); self.assertEqual(ficha(c.p),antes); self.assertEqual(c.inventario,items); self.assertEqual(c.missoes[n],[0]); self.assertEqual(c.afinidade[n],rel)
            e=c.decidir_missao(n,2); c.p.vida-=30; c.p.mana-=25; c.usar_apoio(e); c.resultado_combate(True); self.assertEqual(len(c.missoes[n]),2); self.assertFalse(c.final); self.assertEqual(c.afinidade[n],min(100,rel+d['etapas'][1][4][2][1]+3))
    @patch('progressao.random.random',return_value=1)
    def test_reserva_conversas_e_afinidade(self,_):
        c=self.novo(); self.recrutar(c,'Ione'); self.recrutar(c,'Raska'); self.assertEqual(c.recrutados,['Ione','Raska']); self.assertEqual(c.ativo,'Raska'); c.selecionar('Ione'); old=c.afinidade['Ione']; c.conversa_pessoal('Ione',1); self.assertEqual(c.afinidade['Ione'],old-5)
        with self.assertRaises(ValueError): c.conversa_pessoal('Ione',0)
        c.resolvidos={'Áries':'acordo','Touro':'acordo'}; self.assertTrue(c.npc_disponivel('Ione')); c.npc_decidir('Ione',0); c.selecionar(None); self.assertIsNone(c.ativo)
        with self.assertRaises(ValueError): c.selecionar('Vesper')
        with self.assertRaises(ValueError): c.recrutar('Ione')
        c.alterar_afinidade('Ione',1000); self.assertEqual(c.grau('Ione'),'Lealdade'); c.alterar_afinidade('Ione',-1000); self.assertEqual(c.grau('Ione'),'Distante')
    @patch('progressao.random.random',return_value=1)
    def test_migracao_e_epilogo(self,_):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'save.json'; old=V2('Teste','Ladino','Peixes'); old.iniciar('sigilo'); old.npc_decidir('Ione',1); old.salvar(path)
            c=Campanha.carregar(path); self.assertEqual(ficha(c.p),ficha(old.p)); self.assertEqual(c.xp,old.xp); self.assertEqual(c.afinidade['Ione'],15); c.recrutar('Ione'); self.assertEqual(c.ativo,'Ione')
            for i in (0,0,0): c.viajar(c.etapa_missao('Ione')[0]); c.decidir_missao('Ione',i)
            c.alianca='Liga dos Doze'; c.final='acordo'; self.assertIn('Orven é reconhecido',c.epilogo()); c.salvar(path); novo=Campanha.carregar(path); self.assertEqual(novo.missoes,c.missoes); self.assertEqual(novo.afinidade,c.afinidade); self.assertEqual(novo.ativo,'Ione')
            old1=V1('Teste','Mago','Peixes'); old1.iniciar('sigilo'); old1.salvar(path); c=Campanha.carregar(path); self.assertEqual(c.xp,15); self.assertEqual(ficha(c.p),ficha(old1.p)); self.assertFalse(c.recrutados)
if __name__=='__main__': unittest.main()
