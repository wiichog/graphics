from render import *
from obj import Texture,NormalMap

def gourad(render,bar,**kwargs):
    w,v,u = bar

    tA, tB, tC, = kwargs['texture_coords']
    tx = tA.x * w + tB.x * v + tC.x * u 
    ty = tA.y * w + tB.y * v + tC.y * u 
    color = render.texture.get_color(tx,ty)

    iA, iB, iC = [ dot(n,render.light) for n in kwargs['varying_normals']]
    intensity = w*iA + v*iB + u*iC
    return bytes(map(lambda b: round(b*intensity) if b*intensity > 0 else 0, color))

r = Render(800,600)
t = Texture('./models/model.bmp')
r.load('./models/model.obj',(1,1,1),(300,300,300),
texture=t, shader=gourad)
r.display('out.bmp')