import numpy as np, os, sys
from PIL import Image, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
import make_textures as mt
W,H=1080,1350
mt.W,mt.H=W,H
rng=np.random.default_rng(3)
# base: warm oatmeal linen
base=mt.paper((214,204,188),grain=7,mottle=5,fibers=3200,fiber_tone=(-10,9),specks=40)
# linen weave
y,x=np.mgrid[0:H,0:W]
weave=(np.sin(x*1.9)*0.5+np.sin(y*1.9)*0.5)*2.2
base+=weave[...,None]
# top sheet: cream deckle-edged paper on left
sheet=mt.paper((238,233,223),grain=5,mottle=4,fibers=900,fiber_tone=(-10,7),specks=60)
edge_x=640
n=np.cumsum(rng.normal(0,1.6,H)); n-=np.linspace(n[0],n[-1],H)
n=np.array(Image.fromarray(np.uint8(np.clip(n+128,0,255))).resize((1,H)).getdata(),float).ravel()-128
fine=rng.normal(0,2.2,H)
ex=edge_x+n*0.9+fine
mask=(x<ex[:,None]).astype(np.float32)
mask=np.asarray(Image.fromarray(np.uint8(mask*255)).filter(ImageFilter.GaussianBlur(0.8)),np.float32)/255
# shadow cast by sheet onto linen
sh=np.asarray(Image.fromarray(np.uint8(mask*255)).filter(ImageFilter.GaussianBlur(14)),np.float32)/255
sh=np.roll(sh,10,axis=1)
base*= (1-0.22*sh*(1-mask))[...,None]
# fibrous torn rim (lighter)
rim=np.clip(mask-np.asarray(Image.fromarray(np.uint8(mask*255)).filter(ImageFilter.MinFilter(5)),np.float32)/255,0,1)
img=base*(1-mask[...,None])+sheet*mask[...,None]
img+= (rim*10)[...,None]
Image.fromarray(np.uint8(np.clip(img,0,255))).save('out/slide2-layered-paper.jpg',quality=94)
print('ok')
