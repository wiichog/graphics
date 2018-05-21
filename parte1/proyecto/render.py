import struct
import random
import numpy as np
from obj import Obj, Texture
from collections import namedtuple

# ===============================================================
# Math
# ===============================================================

V2 = namedtuple('Point2',['x','y'])
V3 = namedtuple('Point3',['x','y','z'])

def sum(v0,v1):
    return V3(v0.x + v1.x, v0.y + v1.y, v0.z + v1.z)

def sub(v0,v1):
    return V3(v0.x - v1.x, v0.y - v1.y, v0.z - v1.z)

def mul(v0,k):
    return V3(v0.x*k,v0.y*k,v0.z*k)

def dot(v0,v1):
    return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z

def cross(v0,v1):
    return V3(
        v0.y * v1.z - v0.z * v1.y,
        v0.z * v1.x - v0.x * v1.z,
        v0.x * v1.y - v0.y * v1.x,
    )

def length(v0):
    return (v0.x **2 + v0.y**2 + v0.z**2)**0.5

def norm(v0):
    v0length = length(v0)
    if not v0length:
        return V3(0,0,0)
    return V3(v0.x/v0length,v0.y/v0length,v0.z/v0length)

def bbox(*vertices):
    xs = [vertex.x for vertex in vertices]
    ys = [vertex.y for vertex in vertices]

    xs.sort()
    ys.sort()

    return V2(xs[0],ys[0]),V2(xs[-1],ys[-1])

def barycentric(A,B,C,P):
    bary = cross(
        V3(C.x - A.x, B.x - A.x, A.x - P.x),
        V3(C.y - A.y, B.y - A.y, A.y - P.y)
    )
    if abs(bary[2])<1:
        return -1,-1,-1
    return(
        1 - (bary[0]+bary[1])/bary[2],
        bary[1] / bary[2],
        bary[0] / bary[2]
    )

def ndc(point):
    point = V3(*point)
    return V3(
        point.x / point.z,
        point.y / point.z,
        point.z / point.z
    )
# ===============================================================
# Utils
# ===============================================================
def color(r, g, b):
    return bytes([b, g, r])

BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)

def char(c):
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    return struct.pack('=h',w)

def dword(d):
    return struct.pack('=l',d)

class Render(object):
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.current_color = WHITE
        self.clear()
        self.texture = None
        self.shader = None
        self.normalmap = None


    def color(self,color):
        r,g,b = color
        return bytes([b,g,r])

    def clear(self):
        self.pixels = [
            [WHITE for x in range(self.width)]
            for y in range(self.height)
        ]
        self.zbuffer = [
            [-float('inf') for x in range(self.width)]
            for y in range(self.height)
        ]
    
    def write(self,filename):
        f = open(filename,'bw')
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14+40+self.width * self.height *3))
        f.write(dword(0))
        f.write(dword(14+40))
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width * self.height *3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        for x in range(self.height):
            for y in range(self.width):
                f.write(self.pixels[x][y])
        f.close()
    
    def display(self, filename='out.bmp'):
        self.write(filename)
        try:
            from wand.image import Image
            from wand.display import display
            with Image(filename=filename) as image:
                display(image)
        except ImportError:
            pass 

    def set_color(self,color):
        self.current_color = color
    
    def point(self, x, y, color = None):
        try:
            self.pixels[y][x] = color or self.current_color
        except:
            pass

    def line(self, start, end, color = None):
        start = V2(*start[:2])
        end = V2(*end[:2])
        x1, y1 = int(start.x), int(start.y)
        x2, y2 = int(end.x), int(end.y)

        dy = abs(y2 - y1)
        dx = abs(x2 - x1)
        steep = dy > dx

        if steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2

        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        dy = abs(y2 - y1)
        dx = abs(x2 - x1)

        offset = 0
        threshold = dx

        y = y1
        for x in range(x1, x2 + 1):
            if steep:
                self.point(y, x, color)
            else:
                self.point(x, y, color)
            
            offset += dy * 2
            if offset >= threshold:
                y += 1 if y1 < y2 else -1
                threshold += dx * 2


    def triangle(self, A, B, C, color=None, texture_coords=(), varying_normals=()):
        bbox_min, bbox_max = bbox(A, B, C)
        for x in range(bbox_min.x, bbox_max.x + 1):
            for y in range(bbox_min.y, bbox_max.y + 1):
                w, v, u = barycentric(A, B, C, V2(x, y))
                if w < 0 or v < 0 or u < 0:  # 0 is actually a valid value! (it is on the edge)
                    continue
                color = self.shader(self,
                    triangle=(A, B, C),
                    bar=(w, v, u),
                    varying_normals=varying_normals,
                    texture_coords=texture_coords)

                z = A.z * w + B.z * v + C.z * u
                try:
                    if x < len(self.zbuffer) and y < len(self.zbuffer[x]) and z > self.zbuffer[x][y]:
                        self.point(x, y, color)
                        self.zbuffer[x][y] = z
                except:
                    pass

    def transform(self,vertex,translate=(0,0,0),scale=(1,1,1)):
        vertex = V3(*vertex)
        augmented_vertex = [
            vertex.x,
            vertex.y,
            vertex.z,
            1
        ]
        transformed_Vertex = np.dot(
            self.ViewPort,
            augmented_vertex
        ).tolist()[0]

        return V3(
            round(transformed_Vertex[0]/transformed_Vertex[3]),
            round(transformed_Vertex[1]/transformed_Vertex[3]),
            round(transformed_Vertex[2
            ]/transformed_Vertex[3])
        )

    def load(self, filename, translate=(0, 0, 0), scale=(1, 1, 1), texture=None, shader=None, normalmap=None):
        model = Obj(filename)
        self.light = V3(0,0,1)
        self.texture = texture
        self.shader = shader
        self.normalmap = normalmap

        for face in model.faces:
            vcount = len(face)

            if vcount==3:
                f1 = face[0][0]-1
                f2 = face[1][0]-1
                f3 = face[2][0]-1

                a = self.transform(V3(*model.vertices[f1]), translate, scale)
                b = self.transform(V3(*model.vertices[f2]), translate, scale)
                c = self.transform(V3(*model.vertices[f3]), translate, scale)


                n1 = face[0][2] -1
                n2 = face[1][2] -1
                n3 = face[2][2] -1
                nA = V3(*model.normals[n1])
                nB = V3(*model.normals[n2])
                nC = V3(*model.normals[n3])
                t1 = face[0][1]-1
                t2 = face[1][1]-1
                t3 = face[2][1]-1
                tA = V3(*model.tvertices[t1])
                tB = V3(*model.tvertices[t2])
                tC = V3(*model.tvertices[t3])
                
                self.triangle(a,b,c, texture_coords=(tA,tB,tC),varying_normals=(nA,nB,nC))

            else:
                f1 = face[0][0]-1
                f2 = face[1][0]-1
                f3 = face[2][0]-1
                f4 = face[3][0]-1

                vertices = [
                    self.transform(model.vertices[f1],translate,scale),
                    self.transform(model.vertices[f2],translate,scale),
                    self.transform(model.vertices[f3],translate,scale),
                    self.transform(model.vertices[f4],translate,scale)
                ]
                
                normal = norm(cross(sub(vertices[0],vertices[1]),sub(vertices[1],vertices[2])))
                intensity = dot(normal,self.light)
                grey = round(255*intensity)
                
                if grey<0:
                    continue 

                A,B,C,D = vertices
                
                self.triangle(A, B, C, color(grey, grey, grey))
                self.triangle(A, C, D, color(grey, grey, grey))
    
    def lookAt(self, eye, center, up):
        z = norm(sub(eye,center))
        x = norm(cross(up, z))
        y = norm(cross(z, x))

        self.View = np.matrix([
            [x.x,x.y,x.z,-center.x],
            [y.x,y.y,y.z,-center.y],
            [z.x,z.y,z.z,-center.z],
            [0,0,0,1]
        ])

        self.projection(-1/length(sub(eye,center)))

    def projection(self,coeff):
        self.Projection = np.matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, coeff, 1]
        ])
    
    def viewport(self,viewport):
        self.ViewPort = viewport