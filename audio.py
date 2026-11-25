"""Trilha adaptativa; arquivos externos opcionais, fallback original local."""
from pathlib import Path
import os, json
from urllib.parse import quote

# contexto: título, ISRC, nome do arquivo externo esperado
TRILHAS={
 'menu':('Angevin','USUAN1200110'),
 'exploracao':('The Path of the Goblin King','USUAN1100873'),
 'viagem':('Angevin B','USUAN1200111'),
 'mercado':('Village Consort','USUAN1700007'),
 'dialogo':('Sneaky Snitch','USUAN1100772'),
 'masmorra':('Darkest Child','USUAN1100783'),
 'combate':('Clash Defiant','USUAN1600003'),
 'chefe':('Mighty and Meek','USUAN1100500'),
 'vitoria':('Fanfare for Space','USUAN1300026'),
}
BASE=Path(__file__).resolve().parent/'musicas'
EXTERNAS=Path.home()/'.the_battle'/'musicas'
CONFIG=Path.home()/'.the_battle'/'audio.json'
def fonte(k): return 'https://incompetech.com/music/royalty-free/index.html?Search=Search&isrc='+TRILHAS[k][1]
def url_mp3(k): return 'https://incompetech.com/music/royalty-free/mp3-royaltyfree/'+quote(TRILHAS[k][0])+'.mp3'

def contexto(title,mercados=(),local=''):
    if title.startswith('Masmorra'): return 'masmorra'
    if title.startswith('Travessia'): return 'viagem'
    if title in mercados: return 'mercado'
    if title.startswith(('Conversa','Prólogo','Conselho','Encontro')) or title==local: return 'dialogo'
    return 'exploracao'

class Audio:
    def __init__(self):
        self.mixer=None; self.win=None; self.atual=None; self.tocando=None; self.mudo=False; self.volume=.45; self.erro=''; self.suporte='sem dispositivo'
        try:
            d=json.loads(CONFIG.read_text(encoding='utf-8')); self.mudo=bool(d.get('mudo',False)); self.volume=max(0,min(1,float(d.get('volume',.45))))
        except (OSError,ValueError,TypeError): pass
        try:
            os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT','1')
            from pygame import mixer
            mixer.init(); self.mixer=mixer; self.suporte='pygame'; mixer.music.set_volume(self.volume)
        except Exception as e:
            self.erro=str(e)
            if os.name=='nt':
                try:
                    import winsound
                    self.win=winsound; self.suporte='Windows WAV'
                except ImportError: pass
    def salvar(self):
        try: CONFIG.parent.mkdir(parents=True,exist_ok=True); CONFIG.write_text(json.dumps({'mudo':self.mudo,'volume':self.volume}),encoding='utf-8')
        except OSError: pass
    def parar(self):
        try:
            if self.mixer: self.mixer.music.stop()
            if self.win: self.win.PlaySound(None,0)
        except Exception: pass
        self.tocando=None
    def tocar(self,k,forcar=False):
        if k not in TRILHAS: return
        if self.atual==k and not forcar: return
        self.atual=k; self.parar()
        if self.mudo: return
        caminhos=[EXTERNAS/(k+'.mp3'),BASE/(k+'.mp3'),BASE/(k+'.wav')]
        if self.mixer:
            for p in caminhos:
                if not p.is_file(): continue
                try:
                    self.mixer.music.load(str(p)); self.mixer.music.set_volume(self.volume); self.mixer.music.play(-1); self.tocando=p; return
                except Exception as e: self.erro=str(e)
        elif self.win:
            p=BASE/(k+'.wav')
            try:
                self.win.PlaySound(str(p),self.win.SND_FILENAME|self.win.SND_ASYNC|self.win.SND_LOOP|self.win.SND_NODEFAULT); self.tocando=p
            except Exception as e: self.erro=str(e)
    def alternar(self):
        self.mudo=not self.mudo; self.salvar()
        if self.mudo: self.parar()
        elif self.atual: self.tocar(self.atual,True)
    def ajustar(self,v):
        self.volume=max(0,min(1,float(v)/100)); self.salvar()
        if self.mixer: self.mixer.music.set_volume(self.volume)
    def status(self):
        if self.mudo: return 'Música desativada'
        if not self.tocando: return 'Áudio indisponível — instale pygame ou verifique o dispositivo.'
        if self.tocando.suffix=='.mp3': return TRILHAS[self.atual][0]+' — Kevin MacLeod (CC BY 4.0)'
        return 'Trilha provisória original — '+self.atual
