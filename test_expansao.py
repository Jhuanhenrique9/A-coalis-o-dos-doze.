import unittest,tempfile,json
from pathlib import Path
from unittest.mock import patch
from progressao import Campanha
from campanha import Campanha as Antiga,ficha
from mundo import DISTRITOS
from personagem import CLASSES_DISPONIVEIS
from expansao import EVENTOS,NPCS,MERCADOS,ITENS
class Expansao(unittest.TestCase):
 def novo(self):
  c=Campanha('Teste','Guerreiro','Áries'); c.iniciar('sigilo'); return c
 def test_rotas(self):
  with patch('progressao.random.random',return_value=1):
   for cl in CLASSES_DISPONIVEIS:
    for d in DISTRITOS:
     c=Campanha('Teste',cl,d.signo); c.iniciar('investigar'); f=ficha(c.p)
     for destino in DISTRITOS:
      c.viajar(destino.signo); c.ler(); c.coletar(); c.coletar(); c.resolver('classe' if cl==destino.classe_forte else 'acordo')
     self.assertEqual(f,ficha(c.p)); self.assertGreater(c.nivel,1); self.assertEqual(c.pontos,2*(c.nivel-1)); c.escolher_alianca('Liga dos Doze'); c.encerrar('acordo'); self.assertTrue(c.epilogo())
 def test_atributos(self):
  c=self.novo(); c.ganhar_xp(100); self.assertEqual(c.nivel,3); c.investir('vitalidade'); c.investir('agilidade'); self.assertEqual(c.p.vida_maxima,c.p.vitalidade*5); self.assertEqual(c.p.mana_maxima,20+2*c.p.agilidade)
 def test_itens_checkpoint(self):
  c=self.novo(); c.comprar(0,'Tônico rubro'); n=c.inventario['Tônico rubro']; c.resolver('combate'); c.p.vida-=20; c.usar_item('Tônico rubro'); self.assertEqual(c.inventario['Tônico rubro'],n-1)
  with tempfile.TemporaryDirectory() as d:
   path=Path(d)/'save'; c.salvar(path); r=Campanha.carregar(path); self.assertEqual(r.inventario['Tônico rubro'],n)
  c.resultado_combate(False); self.assertEqual(c.inventario['Tônico rubro'],n)
  c.resolver('combate'); c.p.vida-=20; c.usar_item('Tônico rubro'); c.resultado_combate(True); self.assertEqual(c.inventario['Tônico rubro'],n-1)
 def test_eventos(self):
  for d,evs in EVENTOS.items():
   for i in range(len(evs)):
    for escolha in range(3):
     c=self.novo(); c.local=d; c.evento=[d,i]; c.ouro=100; c.decidir_evento(escolha); self.assertEqual(c.eventos[f'{d}:{i}'],escolha); self.assertIsNone(c.evento)
 def test_mercados(self):
  c=self.novo(); c.ouro=9999
  for d in MERCADOS:
   c.local=d
   for loja in (0,1):
    for nome in c.oferta(loja):
     for i in range(3): c.comprar(loja,nome)
     with self.assertRaises(ValueError): c.comprar(loja,nome)
   c.descansar(); self.assertEqual(c.estoque(0,'Tônico rubro'),3)
 def test_npcs_e_save(self):
  c=self.novo(); c.resolvidos={'Áries':'acordo','Touro':'acordo'}; c.alianca='Liga dos Doze'
  for n in NPCS:
   for i in range(3): c.local=c.npc_local(n); c.npc_decidir(n,i%2)
  with tempfile.TemporaryDirectory() as d:
   path=Path(d)/'save'; c.salvar(path); self.assertEqual(Campanha.carregar(path).relacoes,c.relacoes)
   old=Antiga('Teste','Ladino','Peixes'); old.iniciar('sigilo'); old.salvar(path); new=Campanha.carregar(path); self.assertEqual(ficha(old.p),ficha(new.p)); self.assertEqual(new.xp,15)
if __name__=='__main__': unittest.main()
