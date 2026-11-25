import tempfile, unittest, wave
from pathlib import Path
from unittest.mock import patch
from reliquias import Campanha, CATALOGO, POR_DISTRITO, chance_raro
from equipe import Campanha as V4
from campanha import ficha
from masmorras import MASMORRAS
from audio import TRILHAS, contexto, BASE, Audio

class V5Tests(unittest.TestCase):
    def novo(self,s='Áries'):
        c=Campanha('Teste','Guerreiro',s); c.iniciar('sigilo'); return c
    def test_catalogo_probabilidades(self):
        self.assertEqual(len(CATALOGO),24); self.assertEqual(set(POR_DISTRITO),set(MASMORRAS))
        self.assertEqual([chance_raro(i) for i in range(1,11)],[8,8,8,12,12,12,18,18,18,35])
        for o in range(1,11):
            c=self.novo(); c.iniciar_expedicao(); c.expedicao['onda']=o; c.iniciar_onda()
            with patch('reliquias.random.random',return_value=(chance_raro(o)+.01)/100): c.resultado_combate(True)
            self.assertEqual(c.equipamentos,[])
    def test_drop_independente_e_duplicatas(self):
        for s in MASMORRAS:
            c=self.novo(s); r,a=POR_DISTRITO[s]; c.iniciar_expedicao(); c.expedicao['onda']=10; c.iniciar_onda()
            with patch('reliquias.random.random',side_effect=[.4,.14]): c.resultado_combate(True)
            self.assertEqual(c.equipamentos,[a]); self.assertEqual(c.vitorias_chefe[s],1)
            c.iniciar_expedicao(); c.expedicao['onda']=10; c.iniciar_onda()
            with patch('reliquias.random.random',side_effect=[.34,.14]): c.resultado_combate(True)
            self.assertEqual(c.equipamentos,[a,r]); self.assertEqual(c.vitorias_chefe[s],2)
    def test_revanche_sem_duplicar_recompensas(self):
        c=self.novo(); s=c.local
        with patch('reliquias.random.random',return_value=0):
            c.iniciar_expedicao()
            for _ in range(10): c.iniciar_onda(); c.resultado_combate(True)
            old=(c.ouro,c.xp,c.nivel,c.reputacao.copy(),c.inventario.copy(),c.afinidade.copy())
            c.iniciar_expedicao()
            for _ in range(10): c.iniciar_onda(); c.resultado_combate(True)
        self.assertEqual(old,(c.ouro,c.xp,c.nivel,c.reputacao,c.inventario,c.afinidade)); self.assertEqual(c.conquistas,[s]); self.assertEqual(len(c.equipamentos),2); self.assertEqual(len(c.historico_drops),20)
    def test_equipar_e_efeitos(self):
        c=self.novo(); r,a=POR_DISTRITO[c.local]; inicial=ficha(c.p)
        with self.assertRaises(ValueError): c.equipar_reliquia(r,'equip_raro')
        c.equipamentos=[r,a]; c.equipar_reliquia(r,'equip_raro'); c.equipar_reliquia(a,'equip_artefato'); self.assertEqual(inicial,ficha(c.p))
        c.iniciar_expedicao(); e=c.iniciar_onda(); vida=e.vida; c.usar_reliquia(r,e); self.assertEqual(e.vida,max(0,vida-7)); self.assertFalse(c.reliquia_disponivel(r))
        with self.assertRaises(ValueError): c.usar_reliquia(r,e)
        c.resultado_combate(False); self.assertEqual(c.equipamentos,[r,a]); self.assertEqual(ficha(c.p),inicial); self.assertEqual(c.historico_drops,[])
    def test_migracao_salvamento(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'save.json'; c=V4('Antigo','Mago','Peixes'); c.iniciar('sigilo'); c.salvar(path); v=Campanha.carregar(path); self.assertEqual(ficha(v.p),ficha(c.p)); self.assertEqual(v.equipamentos,[])
            v.iniciar_expedicao(); e=v.iniciar_onda()
            with patch('reliquias.random.random',return_value=0): v.resultado_combate(True)
            r,_=POR_DISTRITO[v.local]; v.equipar_reliquia(r,'equip_raro'); v.salvar(path); novo=Campanha.carregar(path); self.assertEqual(novo.equip_raro,r); self.assertEqual(novo.expedicao['onda'],2); self.assertEqual(novo.historico_drops,v.historico_drops)
    def test_audio_contexto_e_arquivos(self):
        self.assertEqual(contexto('Travessia — x'),'viagem'); self.assertEqual(contexto('Masmorra — y'),'masmorra'); self.assertEqual(contexto('Conversa — Mira'),'dialogo'); self.assertEqual(contexto('Loja',('Loja',)),'mercado'); self.assertEqual(contexto('Peixes / Ilhas'),'exploracao')
        for k in TRILHAS:
            with wave.open(str(BASE/(k+'.wav'))) as f: self.assertGreater(f.getnframes(),10000); self.assertEqual(f.getframerate(),16000)
    def test_audio_sem_dispositivo(self):
        a=Audio(); a.mixer=None; a.win=None; a.mudo=False; a.tocar('menu'); self.assertEqual(a.atual,'menu'); self.assertIsNone(a.tocando); a.parar()
if __name__=='__main__': unittest.main()
