"""Nove pequenas trilhas originais de reserva, sintetizadas sem amostras de terceiros."""
import math, wave, array
from pathlib import Path
from audio import TRILHAS
# Cada tema: andamento, escala, progressão de baixo e melodia (graus).
THEMES=[(76,[0,2,3,5,7,8,10],[0,5,3,4],[0,2,4,6,5,4,2,1]),(98,[0,2,4,5,7,9,11],[0,4,5,3],[0,2,4,2,5,4,3,1]),(112,[0,2,3,5,7,9,10],[0,3,6,4],[0,4,3,2,4,6,5,3]),(120,[0,2,4,5,7,9,11],[0,3,4,0],[0,2,4,5,4,2,1,2]),(83,[0,2,3,5,7,8,11],[0,1,5,4],[4,3,2,6,5,2,1,0]),(64,[0,1,3,5,6,8,10],[0,1,4,0],[0,1,4,3,1,5,3,1]),(142,[0,2,3,5,7,8,10],[0,5,6,4],[0,0,4,2,6,4,3,1]),(156,[0,1,3,5,7,8,11],[0,1,5,4],[0,4,6,5,4,1,3,6]),(106,[0,2,4,5,7,9,11],[0,3,4,0],[0,2,4,6,7,6,4,0])]
RATE=16000

def gerar():
    pasta=Path(__file__).with_name('musicas'); pasta.mkdir(exist_ok=True)
    for idx,(k,(bpm,scale,roots,mel)) in enumerate(zip(TRILHAS,THEMES)):
        beat=60/bpm; size=round(RATE*beat*32); data=[0.0]*size
        def nota(pos,grau,octava,dur,amp,timbre):
            midi=48+idx%4+scale[grau%7]+12*(grau//7+octava); freq=440*2**((midi-69)/12); start=round(pos*beat*RATE); length=round(dur*beat*RATE)
            for j in range(length):
                t=j/RATE; fase=2*math.pi*freq*t; env=min(1,t/.022,max(0,(length-j)/(RATE*.10)))
                if timbre=='plucked': env*=math.exp(-t*3); s=math.sin(fase)+.28*math.sin(fase*2)+.12*math.sin(fase*3)
                else: s=math.sin(fase)+.16*math.sin(fase*2)+.09*math.sin(fase*3)
                data[(start+j)%size]+=s*amp*env
        for bar in range(8):
            root=roots[bar%4]; pos=bar*4
            for offset in (0,2): nota(pos+offset,root,-1,1.8,.085,'soft')
            for j in range(4):
                nota(pos+j,root+[0,2,4,2][j],0,.84,.06,'plucked')
                n=mel[(bar*4+j)%len(mel)]; nota(pos+j+(0.5 if idx in (3,6,7) else 0),n,1,.45 if idx in (3,6,7) else .85,.08,'plucked')
            if idx in (6,7):
                for j in range(4): nota(pos+j,root,-2,.22,.12,'plucked')
        samples=array.array('h',(int(max(-1,min(1,x))*30000) for x in data))
        with wave.open(str(pasta/(k+'.wav')),'wb') as f: f.setnchannels(1); f.setsampwidth(2); f.setframerate(RATE); f.writeframes(samples.tobytes())
if __name__=='__main__': gerar()
