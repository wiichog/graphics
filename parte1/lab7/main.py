import sys
import random
from render import Render
from obj import Texture

def model():
    r = Render(800, 600)
    t = Texture('./models/model.bmp')
    r.load('./models/model.obj', (1, 1, 1), (300, 300, 300), texture=t)
    r.display('out.bmp')

def face():
    r = Render(800, 600)
    t = Texture('./models/earth.bmp')
    r.load('./face.obj', (25, 5, 0), (15, 15, 15))
    r.display('out.bmp')

def earth():
    r = Render(800, 600)
    t = Texture('./models/earth.bmp')
    r.load('./models/earth.obj', (800, 600, 0), (0.5, 0.5, 1), texture=t)
    r.display('out.bmp')

if __name__ == "__main__":
    example = sys.argv[1] if len(sys.argv) > 1 else ""

    if example == "model":
        model()
    elif example == "face":
        face()
    elif example == "earth":
        earth()
    else:
        print("Usage: python3 examples.py <example>")
        print("\nExample can be one of:\n")
        print("face: ", face.__doc__)
        print("earth: ", earth.__doc__)