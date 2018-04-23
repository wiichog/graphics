import sys
import random
from render import Render

def single_point():
    r = Render(800,600)
    r.point(100,100)
    r.display('out.bmp')

def single_line():
    r = Render(800,600)
    r.line((15,32),(589,50))
    r.display('out.bmp')

if __name__ == "__main__":
    example = sys.argv[1] if len(sys.argv) > 1 else ""
    if example == "single_point":
        single_point()
    elif example == "single_line":
        single_line()