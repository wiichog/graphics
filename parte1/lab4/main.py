import sys
import random
from render import Render
import cProfile

def single_point():
    r = Render(800,600)
    r.point(100,100)
    r.display('out.bmp')

def single_line():
    r = Render(800,600)
    r.line((15,32),(589,50),(0,0,0))
    r.display('out.bmp')

def face():
    r = Render(800,600)
    r.load('./models/face.obj',(25, 5, 0), (15, 15, 15))
    r.display()
    r.display('out.bmp')

def cube():
    r = Render(800,600)
    r.load('./models/cube.obj',(9,2),(40,40))
    r.display()
    r.display('out.bmp')

def bear():
    r = Render(800,600)
    r.load('./models/bears.obj',(9,2),(40,40))
    r.display()
    r.display('out.bmp')

def grass():
    r = Render(800,600)
    r.load('./models/grass.obj',(9,2),(70,70))
    r.display()
    r.display('out.bmp')

def hand():
    r = Render(800,600)
    r.load('./models/hand.obj',(25, 25, 0), (10, 10, 10))
    r.display()
    r.display('out.bmp')

if __name__ == "__main__":
    example = sys.argv[1] if len(sys.argv) > 1 else ""
    if example == "face":
        face()
    elif example == "cube":
        cube()
    elif example == "bear":
        bear()
    elif example == "grass":
        grass()
    elif example == "hand":
        cProfile.run('hand()')
        
