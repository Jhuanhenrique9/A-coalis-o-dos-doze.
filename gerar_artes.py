"""Gera ilustrações originais em pixel art. Pillow é necessário apenas para regenerar."""
from PIL import Image, ImageDraw
from pathlib import Path
import random, math
from mundo import DISTRITOS
OUT=Path(__file__).with_name('artes'); OUT.mkdir(exist_ok=True)
PALETTES=[('#192338','#a34a49','#efb16c'),('#283b39','#9c814b','#f5cf80'),('#232d48','#7b89ac','#e9ab69'),('#123643','#3e8a91','#b4eee0'),('#3b2436','#bd864b','#ffe098'),('#203e3a','#7caa75','#d8e6ac'),('#323449','#a29aaa','#efe4cc'),('#271d39','#7b547b','#e6a16f'),('#203b3d','#659474','#f4ce82'),('#272d3c','#7c7e8e','#f4a366'),('#192c4b','#648fc0','#a8e8ff'),('#263346','#6a849c','#f0ba7b')]
def rgb(s): return tuple(bytes.fromhex(s[1:]))
def mix(a,b,t): return tuple(int(x+(y-x)*t) for x,y in zip(rgb(a) if isinstance(a,str) else a,rgb(b) if isinstance(b,str) else b))
def save(im,name,scale=2): im.resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST).save(OUT/(name+'.png'))
def scene(i,variant='district'):
    rng=random.Random(i*79+sum(map(ord,variant))); dark,mid,light=PALETTES[i]; im=Image.new('RGB',(300,108)); d=ImageDraw.Draw(im)
    for y in range(108): d.line((0,y,299,y),fill=mix(dark,mid,y/150))
    for _ in range(42):
        x,y=rng.randrange(300),rng.randrange(53); d.point((x,y),fill=mix(light,dark,.25))
    d.ellipse((235,9,253,27),fill=light); d.ellipse((240,6,256,22),fill=mix(dark,mid,.10))
    for k in range(2):
        pts=[(0,83)]+[(x, rng.randrange(37+k*10,68+k*7)) for x in range(0,310,13)]+[(299,108),(0,108)]
        d.polygon(pts,fill=mix(dark,mid,.17+k*.13))
    water=i in (3,11); forest=i in (5,8); cliff=i==9
    ground=81
    for x in range(-10,300,24):
        h=rng.randrange(17,46); w=rng.randrange(16,28); y=ground-h; wall=mix(dark,mid,rng.uniform(.35,.8)); roof=mix(dark,mid,.25)
        if forest and rng.random()<.55:
            d.rectangle((x+8,y+10,x+11,82),fill='#604c43'); d.polygon([(x-3,y+23),(x+10,y-10),(x+25,y+23)],fill=mid); d.polygon([(x,y+12),(x+10,y-17),(x+20,y+12)],fill=mix(mid,light,.2)); continue
        if cliff: y-=rng.randrange(0,15)
        d.rectangle((x,y,x+w,ground),fill=wall); d.line((x,y,x,ground),fill=mix(wall,light,.25));
        if i in (0,6,9):
            d.rectangle((x-2,y-5,x+w+2,y+3),fill=roof)
            for a in range(x-2,x+w,7): d.rectangle((a,y-9,a+4,y-4),fill=roof)
        elif i in (3,4,10): d.ellipse((x-2,y-12,x+w+2,y+8),fill=roof); d.line((x+w//2,y-16,x+w//2,y-8),fill=light)
        else: d.polygon([(x-4,y),(x+w//2,y-13),(x+w+4,y)],fill=roof)
        for a in range(x+4,x+w-3,8):
            for b in range(y+7,ground-6,12): d.rectangle((a,b,a+2,b+4),fill=light if rng.random()<.7 else dark)
        d.rectangle((x+w//2-3,ground-9,x+w//2+3,ground),fill=dark)
    if i in (2,4,6,10):
        x=145; d.rectangle((x-10,21,x+10,82),fill=mid); d.polygon([(x-15,23),(x,5),(x+15,23)],fill=dark); d.ellipse((x-6,28,x+6,40),fill=light); d.line((x,34,x+3,30),fill=dark,width=2)
    d.rectangle((0,83,299,108),fill=mix(dark,mid,.25))
    if water:
        for _ in range(90):
            x,y=rng.randrange(300),rng.randrange(84,108); d.line((x,y,min(299,x+rng.randrange(3,20)),y),fill=mix(mid,light,rng.random()*.5))
        d.polygon([(80,91),(108,91),(100,97),(87,97)],fill='#795242'); d.line((94,73,94,91),fill=light); d.polygon([(94,73),(94,88),(105,88)],fill='#e3d8ad')
    else:
        d.polygon([(127,83),(172,83),(239,108),(49,108)],fill=mix(mid,dark,.3));
        for _ in range(40):
            x,y=rng.randrange(300),rng.randrange(84,108); d.line((x,y,x+3,y),fill=mix(mid,dark,.4))
    for x in (18,278):
        d.rectangle((x,54,x+2,101),fill='#43343a'); d.rectangle((x-3,55,x+5,62),fill=light); d.rectangle((x-4,53,x+6,55),fill=dark)
    if variant=='market':
        for x in (35,105,215):
            d.rectangle((x,72,x+31,97),fill='#684b3c'); d.polygon([(x-4,72),(x+4,60),(x+27,60),(x+35,72)],fill=light)
            for a in range(x+2,x+31,8): d.rectangle((a,64,a+3,72),fill=mid)
            for a in range(x+3,x+30,6): d.ellipse((a,82,a+4,86),fill=light)
    if variant=='travel':
        d.polygon([(140,96),(151,96),(154,107),(137,107)],fill='#292735'); d.ellipse((141,88,150,98),fill='#bd9970'); d.line((151,94,157,106),fill=light,width=2)
        d.line((3,3,296,3),fill=light); d.line((3,104,296,104),fill=light)
    save(im,f'{variant}_{i}')

def portrait(i,state='calm',npc=False,filename=None):
    dark,mid,light=PALETTES[i]; im=Image.new('RGB',(72,84),dark); d=ImageDraw.Draw(im)
    for y in range(84): d.line((0,y,71,y),fill=mix(dark,mid,y/120))
    d.ellipse((8,4,63,59),outline=mix(mid,light,.45),width=1)
    skin=['#78a66e','#c79877','#e2ae83','#79b8b6','#ce9b59','#e4c3a0','#e8c9a7','#ad7183','#bc947a','#909ba6','#88bedc','#d5a882'][i]; shade=mix(skin,dark,.35); hi=mix(skin,'#fff2d2',.22); hair=['#28382e','#864a3b','#d3c6a0','#204d60','#976039','#c6c5a4','#f1e3b9','#3d253a','#513f36','#434958','#e1edf1','#69473a'][i]
    # shoulders, collar and distinct facial silhouette
    d.polygon([(4,83),(8,66),(25,56),(47,56),(64,66),(69,83)],fill=mix(mid,dark,.15)); d.polygon([(24,56),(36,74),(48,56),(44,82),(28,82)],fill=light)
    d.rectangle((29,46,43,62),fill=shade); d.polygon([(21,19),(29,12),(45,12),(53,22),(51,43),(45,53),(36,57),(27,51),(20,41)],fill=skin)
    d.polygon([(20,24),(24,16),(30,12),(30,43),(36,53),(27,51),(20,41)],fill=shade); d.polygon([(33,18),(45,17),(49,26),(48,36),(38,34)],fill=hi)
    if i in (0,2,5,7,8):
        d.polygon([(23,28),(10,19),(15,37),(22,42)],fill=skin); d.polygon([(49,28),(62,19),(57,37),(50,42)],fill=skin)
    else:
        d.ellipse((16,29,25,41),fill=shade); d.ellipse((48,29,56,41),fill=skin)
    if i==4:
        d.ellipse((13,10,59,62),fill=hair); d.ellipse((18,9,29,23),fill=skin); d.ellipse((43,9,54,23),fill=skin); d.ellipse((22,18,50,51),fill=skin); d.ellipse((26,37,46,50),fill='#e4c18a'); d.polygon([(31,39),(41,39),(36,44)],fill=dark)
    else:
        d.polygon([(18,24),(17,15),(26,7),(44,7),(55,17),(53,30),(45,16),(30,19),(23,30)],fill=hair)
        if i==1: d.polygon([(22,39),(29,45),(36,43),(43,45),(50,39),(47,57),(36,66),(25,57)],fill=hair)
        if i==7:
            d.polygon([(18,18),(10,3),(13,22),(24,27)],fill='#e5c7a1'); d.polygon([(54,18),(62,3),(59,22),(48,27)],fill='#e5c7a1')
        if i==6: d.ellipse((17,3,55,12),outline=light,width=2)
        if i==3: d.polygon([(18,27),(7,25),(14,42),(20,41)],fill=mid); d.polygon([(54,27),(65,25),(58,42),(52,41)],fill=mid)
        if i==9: d.line((30,18,36,29,32,36),fill=dark,width=2)
        if i==10: d.polygon([(19,22),(13,12),(25,14),(29,1),(36,11),(44,1),(48,14),(59,11),(53,24)],fill=light)
        if i==0: d.polygon([(26,47),(29,38),(32,48)],fill='#f5e8bc'); d.polygon([(40,48),(43,38),(46,47)],fill='#f5e8bc')
        if i==8: d.polygon([(22,17),(18,4),(29,14)],fill=hair); d.polygon([(50,17),(54,4),(43,14)],fill=hair)
    eye=light if i in (3,6,7,10) else '#eae2cb'
    for x in (27,42):
        d.rectangle((x,30,x+5,32),fill=eye); d.rectangle((x+2,30,x+3,33),fill=dark)
        d.line((x,27 if state!='battle' else 25,x+5,27 if state!='battle' else 29),fill=hair,width=2)
    if i!=4: d.line((35,33,33,41,38,41),fill=shade)
    d.line((32,47,40,46 if state=='dialog' else 47),fill=dark,width=1)
    if state=='battle': d.line((58,47,64,77),fill='#d3d7df',width=3); d.line((55,68,66,66),fill=light,width=2)
    if state=='hurt': d.line((23,35,27,40),fill='#9c4145',width=2); d.line((39,47,43,50),fill='#9c4145')
    if state=='level':
        for x,y in [(10,15),(60,21),(8,49),(62,57)]: d.line((x-3,y,x+3,y),fill=light); d.line((x,y-3,x,y+3),fill=light)
    if state=='travel': d.polygon([(9,23),(14,8),(27,2),(45,2),(58,9),(63,25),(53,18),(45,9),(27,9),(19,20)],fill=mix(mid,dark,.3))
    if npc:
        d.rectangle((3,3,68,80),outline=light); d.ellipse((31,64,41,74),fill=dark,outline=light)
        d.line((35,65,35,72),fill=light,width=2)
    d.rectangle((0,0,71,83),outline=light); save(im,filename or f'portrait_{i}_{state}')

def icon(name):
    im=Image.new('RGB',(32,32),'#242b3a'); d=ImageDraw.Draw(im); gold='#e7c17a'; silver='#c2d0da'; red='#d46566'; blue='#73b7de'; green='#8dcb9a'
    d.rectangle((1,1,30,30),outline='#7a6752')
    if name=='forca': d.polygon([(8,23),(21,5),(26,5),(25,11),(12,25)],fill=silver); d.line((6,19,16,28),fill=gold,width=3)
    elif name=='defesa': d.polygon([(7,7),(16,4),(25,7),(24,20),(16,28),(8,20)],fill=silver); d.polygon([(10,9),(16,7),(22,9),(21,19),(16,24),(11,19)],fill='#58748b')
    elif name=='agilidade': d.polygon([(18,3),(7,18),(15,18),(12,29),(26,12),(18,12)],fill=gold)
    elif name in ('vitalidade','vida'): d.ellipse((5,7,17,19),fill=red); d.ellipse((15,7,27,19),fill=red); d.polygon([(5,15),(16,28),(27,15)],fill=red)
    elif name=='mana': d.polygon([(16,4),(25,18),(22,25),(16,28),(10,25),(7,18)],fill=blue); d.line((13,15,11,20,15,24),fill='#d2eaff',width=2)
    elif name in ('potion','essence','elixir'):
        col={'potion':red,'essence':blue,'elixir':gold}[name]; d.rectangle((12,5,20,9),fill=gold); d.rectangle((13,9,19,15),fill=silver); d.polygon([(13,14),(6,21),(8,27),(24,27),(26,21),(19,14)],fill=silver); d.polygon([(9,20),(23,20),(23,25),(9,25)],fill=col)
    elif name=='ration': d.ellipse((5,10,27,24),fill='#ba8552'); d.line((10,14,15,18),fill=gold,width=2); d.line((17,13,22,17),fill=gold,width=2)
    elif name=='seal': d.ellipse((6,6,26,26),fill=red); d.ellipse((10,10,22,22),outline=gold,width=2); d.line((12,16,20,16),fill=gold,width=2)
    elif name=='xp': d.polygon([(16,3),(19,12),(29,12),(21,19),(24,29),(16,23),(8,29),(11,19),(3,12),(13,12)],fill=gold)
    elif name=='material': d.polygon([(5,16),(14,7),(25,10),(28,20),(20,26),(8,25)],fill=silver); d.line((5,16,20,17,25,10),fill='#687b86',width=2)
    elif name=='book': d.polygon([(4,7),(14,9),(16,13),(18,9),(28,7),(28,25),(18,25),(16,28),(14,25),(4,25)],fill=gold); d.line((16,13,16,26),fill='#795331',width=2)
    save(im,'icon_'+name,1)

def journal():
    im=Image.new('RGB',(300,108),'#2a2535'); d=ImageDraw.Draw(im)
    for y in range(108): d.line((0,y,299,y),fill=mix('#242132','#6a4537',y/130))
    d.ellipse((38,82,262,105),fill='#201c29'); d.polygon([(38,14),(132,21),(150,33),(168,21),(262,14),(267,88),(168,94),(150,103),(132,94),(33,88)],fill='#674337')
    for off in (4,2,0):
        d.polygon([(44,14+off),(132,21+off),(150,34+off),(168,21+off),(256,14+off),(260,83+off),(167,89+off),(150,98+off),(133,89+off),(40,83+off)],fill=['#dcc492','#d2b886','#b5a071'][off//2])
    d.line((150,34,150,96),fill='#80634e',width=2)
    for x in (57,174):
        for y in range(37,81,7): d.line((x,y,x+62-(y%3)*7,y+2),fill='#9a775b')
    d.ellipse((77,27,115,65),outline='#805b48'); d.line((96,29,96,63),fill='#805b48'); d.line((79,46,113,46),fill='#805b48')
    d.polygon([(199,90),(246,33),(260,22),(257,41),(205,91)],fill='#d7d0b2'); d.line((199,90,252,28),fill='#725342',width=2)
    save(im,'journal')
for i in range(12):
    for v in ('district','travel','market'): scene(i,v)
    for st in ('calm','dialog','battle','hurt','level','travel'): portrait(i,st)
for n in ('forca','defesa','agilidade','vitalidade','vida','mana','potion','essence','elixir','ration','seal','xp','material','book'): icon(n)
journal()
for name,i in [('Ione',5),('Raska',0),('Vesper',7),('Maelis',6)]: portrait(i,'dialog',True,'npc_'+name)
# Banners fade from the interface background to the full illustration.
for path in sorted(OUT.glob('*.png')):
    if '_fade' not in path.stem and (path.stem.startswith(('district_','travel_','market_')) or path.stem=='journal'):
        im=Image.open(path).convert('RGB'); bg=Image.new('RGB',im.size,'#2a211b')
        for step,alpha in enumerate((.32,.67)):
            Image.blend(bg,im,alpha).save(OUT/(path.stem+f'_fade{step}.png'))
