"""Instalação explícita de faixas gratuitas oficiais. Sem download durante a campanha."""
import urllib.request, concurrent.futures
from audio import TRILHAS, EXTERNAS, url_mp3, fonte

def baixar(k):
    p=EXTERNAS/(k+'.mp3'); tmp=p.with_suffix('.part')
    if p.is_file() and p.stat().st_size>4096: return f'{k}: já instalado'
    try:
        req=urllib.request.Request(url_mp3(k),headers={'User-Agent':'Mozilla/5.0'})
        with urllib.request.urlopen(req,timeout=30) as r:
            data=r.read(40*1024*1024+1)
        if len(data)>40*1024*1024 or len(data)<4096 or not (data.startswith(b'ID3') or (data[0]==255 and data[1]&224==224)): raise ValueError('Resposta não é MP3 válido')
        tmp.write_bytes(data); tmp.replace(p); return f'{k}: OK — {TRILHAS[k][0]}'
    except Exception as e:
        tmp.unlink(missing_ok=True); return f'{k}: falhou ({e}). Baixe em {fonte(k)} e salve como {p}'

if __name__=='__main__':
    EXTERNAS.mkdir(parents=True,exist_ok=True)
    print('Kevin MacLeod — CC BY 4.0 — https://creativecommons.org/licenses/by/4.0/')
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        for msg in pool.map(baixar,TRILHAS): print(msg)
    print('Reabra o jogo. Se faltar alguma faixa, a música provisória será usada.')
