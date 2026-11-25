import unittest, tempfile
from pathlib import Path
from campanha import Campanha, ficha
from mundo import DISTRITOS, RECEITAS
from personagem import CLASSES_DISPONIVEIS

class CampanhaTests(unittest.TestCase):
    def novo(self,classe='Guerreiro',origem='Áries'):
        c=Campanha('Teste',classe,origem); c.iniciar('investigar'); return c
    def test_todas_classes_origens_e_distritos(self):
        for classe in CLASSES_DISPONIVEIS:
            for origem in DISTRITOS:
                c=self.novo(classe,origem.signo); inicial=ficha(c.p)
                for d in DISTRITOS:
                    c.viajar(d.signo); c.ler(); c.coletar(); c.coletar()
                    with self.assertRaises(ValueError): c.coletar()
                    c.resolver('classe' if classe==d.classe_forte else 'acordo')
                    with self.assertRaises(ValueError): c.resolver('acordo')
                self.assertEqual(len(c.resolvidos),12); self.assertEqual(len(c.lidos),12); self.assertEqual(ficha(c.p),inicial)
                for arma in RECEITAS: c.fabricar(arma)
                self.assertEqual(ficha(c.p),inicial); self.assertEqual(len(c.armas),4)
                self.assertTrue(c.audiencia_liberada()); c.escolher_alianca('Pacto dos Faróis'); c.encerrar('acordo'); self.assertTrue(c.epilogo())
    def test_combate_derrota_vitoria_save(self):
        c=self.novo(); inicial=ficha(c.p); e=c.resolver('combate'); self.assertTrue(e.esta_vivo()); c.p.receber_dano(999)
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'save.json'; c.salvar(path); r=Campanha.carregar(path); self.assertEqual(ficha(r.p),inicial); self.assertFalse(r.pendente)
            c.resultado_combate(False); self.assertEqual(ficha(c.p),inicial); self.assertFalse(c.resolvidos)
            e=c.resolver('combate'); e.receber_dano(999); c.resultado_combate(True); self.assertEqual(c.resolvidos['Áries'],'combate'); c.salvar(path); r=Campanha.carregar(path); self.assertEqual(r.resolvidos,c.resolvidos)
    def test_final_e_restricoes(self):
        c=self.novo(); self.assertFalse(c.audiencia_liberada())
        with self.assertRaises(ValueError): c.escolher_alianca('Liga dos Doze')
        for s in ('Áries','Touro','Câncer'):
            c.viajar(s); c.resolver('acordo')
        c.escolher_alianca('Liga dos Doze')
        with self.assertRaises(ValueError): c.encerrar('acordo')
        e=c.encerrar('combate'); self.assertEqual(e.nome,'Regente Cassian'); c.resultado_combate(False); self.assertFalse(c.final)
        c.encerrar('combate'); c.resultado_combate(True); self.assertEqual(c.final,'combate'); c.viajar('Peixes')
    def test_custos_e_atalhos(self):
        c=self.novo('Ladino'); self.assertEqual(c.custo_acordo(),9)
        with self.assertRaises(ValueError): c.resolver('classe')
        c.viajar('Gêmeos'); c.resolver('classe'); self.assertEqual(c.reputacao['Gêmeos'],2)
        with self.assertRaises(ValueError): c.fabricar('Martelo de basalto')
        c.p.receber_dano(10); c.descansar(); self.assertEqual(c.p.vida,c.p.vida_maxima)
if __name__=='__main__': unittest.main()
