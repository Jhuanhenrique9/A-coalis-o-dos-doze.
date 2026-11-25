"""Sprites originais procedurais em pixel art; Pillow só para regenerar."""
from PIL import Image, ImageDraw
from pathlib import Path
import random, math
from masmorras import MASMORRAS, inimigo_onda
from gerar_artes import PALETTES, mix
OUT=Path(__file__).with_name('artes')

def sprite(i,o,tema):
    r=random.Random(917*i+o*37); dark,mid,light=PALETTES[i]; boss=o==10
    im=Image.new('RGB',(96,96),dark); d=ImageDraw.Draw(im)
    for y in range(96): d.line((0,y,95,y),fill=mix(dark,mid,y/210))
    for _ in range(26):
        x,y=r.randrange(96),r.randrange(85); d.point((x,y),fill=mix(mid,light,.25))
    for x in (8,76):
        d.rectangle((x,8,x+10,80),fill=mix(dark,mid,.32)); d.rectangle((x-2,8,x+12,12),fill=mid)
    d.ellipse((17,76,79,89),fill=mix(dark,mid,.16)); d.ellipse((24,80,72,85),fill='#13151b')
    if boss:
        d.ellipse((13,9,83,79),outline=light,width=1); d.ellipse((17,13,79,75),outline=mid,width=1)
        for a in range(0,360,45):
            x=48+int(35*math.cos(math.radians(a))); y=44+int(35*math.sin(math.radians(a))); d.polygon([(x,y-3),(x+3,y),(x,y+3),(x-3,y)],fill=light)
    outline='#151520'; shadow=mix(dark,mid,.55); body=mix(mid,light,.20); hi=mix(mid,light,.65)
    cx=48; yy=27 if boss else 34; w=24 if boss else 16+(o%3)*2
    # Named creature morphology chosen from its name; otherwise district theme.
    name=inimigo_onda(list(MASMORRAS)[i],o).lower() if o else ''
    if any(x in name for x in ('aranha','escorpião','caranguejo','besouro','vespa','ferrão')): shape='insect'
    elif any(x in name for x in ('enguia','serpente','lagarto','tubarão','peixe','polvo','medusa')): shape='aquatic'
    elif any(x in name for x in ('rato','lobo','leão','javali','urso','cervo','cão','grifo','corvo','touro')): shape='beast'
    elif any(x in name for x in ('broto','raiz','flor','fungo','mandrágora','liana','ent ','esporo','musgo','rosa')): shape='plant'
    elif any(x in name for x in ('esfera','relógio','autômato','mola','mecânico','engrenagens','núcleo','vórtice','centelha','gota','nuvem','livro','mímico')): shape='machine'
    else: shape=tema if boss else ('armor' if o%3==1 else tema if o%3==2 else 'shadow')
    if shape=='insect':
        for j in range(3):
            y=47+j*7
            for sign in (-1,1): d.line((cx+sign*8,y,cx+sign*(26+j*2),y-8,cx+sign*(33+j),y+10),fill=outline,width=5); d.line((cx+sign*8,y,cx+sign*(26+j*2),y-8,cx+sign*(33+j),y+10),fill=body,width=2)
        d.ellipse((cx-w,yy+9,cx+w,77),fill=body,outline=outline,width=3); d.ellipse((35,yy,61,yy+26),fill=shadow,outline=outline,width=2)
        if boss or 'escorpião' in name: d.line((57,70,78,62,80,36,67,24),fill=outline,width=9); d.line((57,70,78,62,80,36,67,24),fill=hi,width=5); d.polygon([(65,18),(72,24),(62,32)],fill=light)
    elif shape=='aquatic':
        for j in range(4):
            x=28+j*12; d.line((x,58,x-9+(j%2)*18,70,x-5,81),fill=outline,width=7); d.line((x,58,x-9+(j%2)*18,70,x-5,81),fill=body,width=4)
        d.polygon([(cx,yy-8),(cx+w+4,yy+18),(cx+w,60),(cx,72),(cx-w,60),(cx-w-4,yy+18)],fill=body,outline=outline,width=2)
        for sign in (-1,1): d.polygon([(cx+sign*15,43),(cx+sign*34,25),(cx+sign*29,60)],fill=hi,outline=outline)
    elif shape=='beast':
        for x in (28,40,57,69): d.rectangle((x-4,59,x+4,80),fill=shadow,outline=outline,width=2); d.rectangle((x-5,76,x+5,81),fill=hi)
        d.ellipse((22,44,75,73),fill=body,outline=outline,width=3)
        d.polygon([(28,yy+20),(29,yy-8),(43,yy+3),(54,yy+3),(69,yy-8),(68,yy+20),(60,yy+35),(37,yy+35)],fill=body,outline=outline,width=2)
        d.polygon([(37,yy+24),(60,yy+24),(55,yy+35),(42,yy+35)],fill=hi,outline=outline)
    elif shape=='plant':
        for x in (27,38,55,67): d.line((48,59,x,76,x-5,83),fill=outline,width=8); d.line((48,59,x,76,x-5,83),fill=body,width=4)
        for a in range(0,360,60 if not boss else 45):
            x=48+int(w*math.cos(math.radians(a))); y=yy+18+int(w*math.sin(math.radians(a))); d.ellipse((x-10,y-12,x+10,y+12),fill=hi,outline=outline,width=2)
        d.ellipse((34,yy+4,62,yy+32),fill=shadow,outline=outline,width=2)
    elif shape=='machine':
        d.polygon([(48,yy-5),(48+w+7,yy+18),(48+w,65),(48,77),(48-w,65),(48-w-7,yy+18)],fill=body,outline=outline,width=3)
        for a in range(0,360,45):
            x=48+int((w+5)*math.cos(math.radians(a))); y=yy+22+int((w+5)*math.sin(math.radians(a))); d.rectangle((x-4,y-4,x+4,y+4),fill=hi,outline=outline)
        d.ellipse((34,yy+8,62,yy+36),fill=shadow,outline=outline,width=3); d.ellipse((42,yy+16,54,yy+28),fill=light)
    else:
        d.polygon([(cx-w,yy+22),(cx+w,yy+22),(cx+w+7,65),(cx+12,66),(cx+16,81),(cx-1,81),(cx,66),(cx-16,81),(cx-24,81),(cx-13,65),(cx-w-7,65)],fill=shadow,outline=outline,width=3)
        d.polygon([(cx-w,yy+23),(cx,yy+17),(cx+w,yy+23),(cx+13,61),(cx-13,61)],fill=body,outline=outline,width=2)
        d.polygon([(cx-14,yy+7),(cx-10,yy-5),(cx+10,yy-5),(cx+14,yy+7),(cx+10,yy+23),(cx-10,yy+23)],fill=hi,outline=outline,width=2)
        d.rectangle((cx-11,yy+9,cx+11,yy+14),fill=outline)
        if shape=='stone':
            for _ in range(7):
                x=r.randrange(36,60); y=r.randrange(yy+24,60); d.line((x,y,x+4,y+4,x+1,y+8),fill=shadow,width=1)
        if shape=='shadow': d.polygon([(cx-19,yy+5),(cx,yy-12),(cx+19,yy+5),(cx+13,yy+23),(cx-13,yy+23)],fill=shadow,outline=outline,width=2)
        d.line((73,35,73,78),fill=outline,width=6); d.line((73,35,73,78),fill=hi,width=3); d.rectangle((67,49,79,52),fill=light)
    if shape!='machine':
        for x in (42,53): d.rectangle((x-2,yy+12,x+2,yy+14),fill=light)
    if boss:
        # Heraldic boss sigils and equipment, distinctive by district.
        if i==0: d.line((17,17,17,80),fill=light,width=2); d.polygon([(17,17),(34,21),(17,31)],fill=hi)
        if i==2: d.line((17,47,79,47),fill=hi,width=1); d.ellipse((16,40,30,54),outline=light,width=2); d.ellipse((66,40,80,54),outline=light,width=2)
        if i==6: d.line((16,26,16,65),fill=light,width=2); d.line((6,33,26,33),fill=light,width=2); d.polygon([(6,33),(2,45),(10,45)],fill=hi); d.polygon([(26,33),(22,45),(30,45)],fill=hi)
        if i==8: d.arc((67,15,89,77),90,270,fill=light,width=2); d.line((78,15,78,77),fill=hi,width=1)
        if i==9: d.line((35,53,46,61,42,70,55,78),fill='#fca24d',width=2)
        if i==10: d.line((52,10,40,32,55,32,44,53),fill=light,width=3)
        if i==11: d.ellipse((9,13,23,27),fill=light); d.ellipse((14,10,25,23),fill=dark)
        d.polygon([(33,yy-4),(30,yy-16),(40,yy-10),(48,yy-20),(56,yy-10),(66,yy-16),(63,yy-4)],fill=light,outline=outline,width=1)
    # Wave-specific rune marks ensure each enemy has a separate portrait.
    for j in range(o%5+1): d.rectangle((5+j*4,90,7+j*4,92),fill=light)
    return im.resize((192,192),Image.Resampling.NEAREST)


def sala(i,tema):
    rng=random.Random(951+i); dark,mid,light=PALETTES[i]; im=Image.new('RGB',(300,108),dark); d=ImageDraw.Draw(im)
    for y in range(108): d.line((0,y,299,y),fill=mix(dark,mid,y/210))
    # Vaulted passage, vanishing point and layered stonework.
    d.polygon([(0,0),(104,24),(104,80),(0,108)],fill=mix(dark,mid,.26)); d.polygon([(299,0),(196,24),(196,80),(299,108)],fill=mix(dark,mid,.26))
    d.polygon([(0,108),(104,80),(196,80),(299,108)],fill=mix(dark,mid,.45)); d.polygon([(0,0),(104,24),(196,24),(299,0)],fill=mix(dark,mid,.1))
    for k,(x,y) in enumerate(((9,4),(44,12),(79,20),(107,26))):
        w=300-2*x; h=100-2*y; d.arc((x,y,300-x,y+int(h*.8)),180,360,fill=mid,width=3); d.line((x,y+h//3,x,108-y),fill=mid,width=3); d.line((300-x,y+h//3,300-x,108-y),fill=mid,width=3)
    d.rectangle((128,46,172,80),fill='#14161d'); d.arc((128,29,172,63),180,360,fill=light,width=2)
    d.line((150,34,150,80),fill=mid,width=2)
    for y in (83,90,101): d.line((max(0,100-(y-80)*3),y,min(299,200+(y-80)*3),y),fill=mix(dark,light,.32))
    for x in (20,62,238,279):
        d.rectangle((x-1,33,x+1,60),fill=mid); d.polygon([(x-4,41),(x,28),(x+4,41),(x,46)],fill=light)
    for _ in range(30):
        x,y=rng.randrange(300),rng.randrange(18,106)
        if tema=='plant': d.line((x,y,x+3,y-5,x+6,y-4),fill=mid,width=2)
        elif tema=='aquatic': d.line((x,y,x+6,y),fill=mix(mid,light,.3))
        elif tema=='machine': d.rectangle((x,y,x+2,y+2),fill=mid)
        else: d.point((x,y),fill=mid)
    if tema=='stone':
        for x in (7,292): d.polygon([(x-6,104),(x,61),(x+10,104)],fill=mid,outline=light)
    im=im.resize((600,216),Image.Resampling.NEAREST); name=f'dungeon_{i}'; im.save(OUT/(name+'.png'))
    for j,alpha in enumerate((.32,.67)): Image.blend(Image.new('RGB',im.size,'#2a211b'),im,alpha).save(OUT/(name+f'_fade{j}.png'))

def main():
    for i,(s,m) in enumerate(MASMORRAS.items()):
        sala(i,m.tema)
        for o in range(1,11): sprite(i,o,m.tema).save(OUT/f'enemy_{i}_{o}.png')
        sprite(i,0,'armor').save(OUT/f'enemy_local_{i}.png')
    for i in range(4): sprite(i*3,0,'shadow').save(OUT/f'enemy_personal_{i}.png')
    sprite(10,0,'machine').save(OUT/'enemy_final.png')
if __name__=='__main__': main()
