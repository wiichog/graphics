from render import *

def gourad(render,bar,texture_coords,varying_normals,triangle ):
    w,v,u = bar
    if len(texture_coords)!=0:
        tA, tB, tC, =texture_coords
        tx = tA.x * w + tB.x * v + tC.x * u 
        ty = tA.y * w + tB.y * v + tC.y * u 
        color = render.texture.get_color(tx,ty)
    else:
        color = WHITE
    if(len(varying_normals)!=0):
        iA, iB, iC = [ dot(n,render.light) for n in varying_normals]
        intensity = w*iA + v*iB + u*iC
    else:
        intensity =1 
    return bytes(map(lambda b: round(b*intensity) if b*intensity > 0 else 0, color))

r = Render(800,800)

r.viewport(np.matrix([
        [10, 0, 0, 500],
        [0, 10, 0, 5],
        [0, 0, 10, 0],
        [0, 0, 0, 1]
        ]))
t = Texture('./models/house.bmp')
r.light = V3(0,0,1)
r.lookAt(V3(1,1,1),V3(0,0,0),V3(0,1,0))
r.load('./models/house.obj',texture=t,shader=gourad)

r.viewport(np.matrix([
        [1, 0, 0, 100],
        [0, 1, 0, 70],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
        ]))
t = Texture('./models/pot.bmp')
r.light = V3(0,0,1)
r.lookAt(V3(1,1,1),V3(0,0,0),V3(0,1,0))
r.load('./models/pot.obj',texture=t,shader=gourad)

r.viewport(np.matrix([
        [3, 0, 0, 100],
        [0, 3, 0, 70],
        [0, 0, 3, 0],
        [0, 0, 0, 1]
        ]))
t = Texture('./models/fox.bmp')
r.light = V3(0,0,1)
r.lookAt(V3(1,1,1),V3(0,0,0),V3(0,1,0))
r.load('./models/fox.obj',texture=t,shader=gourad)

r.viewport(np.matrix([
        [1, 0, 0, 170],
        [0, 1, 0, 440],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
        ]))
t = Texture('./models/box.bmp')
r.light = V3(0,0,1)
r.lookAt(V3(1,1,1),V3(0,0,0),V3(0,1,0))
r.load('./models/box.obj',texture=t,shader=gourad)


r.viewport(np.matrix([
        [1, 0, 0, 100],
        [0, 1, 0, 400],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
        ]))
t = Texture('./models/car.bmp')
r.light = V3(0,0,1)
r.lookAt(V3(1,1,1),V3(0,0,0),V3(0,1,0))
r.load('./models/car.obj',texture=t,shader=gourad)


r.display('out.bmp')

