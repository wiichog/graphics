import sys
import random
from render import Render

def single_point():
    r = Render(800,600)
    r.point(100,100)
    r.display('out.bmp')

def square():
    width = 800
    height = 600
    r = Render(width,height)

    padding = 10

    square_w = width - padding
    square_h = height - padding

    for x in range(width):
        if(x > padding and x < square_w):
            r.point(x,square_h)
            r.point(x,padding)

    for y in range(height):
        if(y>padding and y<square_h):
            r.point(square_w,y)
            r.point(padding,y)

    r.display('out.bmp')

def diagonal():
    width = 800
    height = 600
    r = Render(width,height)

    for x in range(width):
        for y in range(height):
            if x==y:
                r.point(x,y)
    
    r.display('out.bmp')

def static():

    width = 800
    height = 600
    r = Render(width,height)
    
    for x in range(width):
        for y in range(height):
            if random.random() > 0.5:
                r.point(x,y)
    
    r.display('out.bmp')

def color_static():

    width = 800
    height = 600
    r = Render(width,height)
    
    for x in range(width):
        for y in range(height):
            r.point(x,y, r.ccolor(
                random.randint(0,255),
                random.randint(0,255),
                random.randint(0,255)
            ))
    
    r.display('out.bmp')

def stars():
    width = 800
    height = 600
    r = Render(width,height)

    def star(s,y,size):
        c = random.randint(0,255)
        r.set_color(color(c,c,c))

        if size==1:
            r.point(x,y)
        elif size ==2:
            r.point(x,y)
            r.point(x+1,y)
            r.point(x,y+1)
            r.point(x+1,y+1)
        elif size ==3:
            r.point(x,y)
            r.point(x+1,y)
            r.point(x,y+1)
            r.point(x-1,y)
            r.point(x,y-1)

    for x in range(width-4):
        for y in random(height-4):
            if random.random()<0.001:
                star(x+2,y+2,random.randint(1,3))
    
    r.display('out.bmp')

if __name__ == "__main__":
    example = sys.argv[1] if len(sys.argv) > 1 else ""
    if example == "single_point":
        single_point()
    elif example == "square":
        square()
    elif example == "diagonal":
        diagonal()
    elif example == "static":
        static()
    elif example == "color_static":
        color_static()
    elif example == "stars":
        stars()
    else:
        print("Usage: python3 examples.py <example>")
        print("\nExample can be one of:\n")
        print("single_point: ", single_point.__doc__)
        print("square: ", square.__doc__)
        print("diagonal: ", diagonal.__doc__)
        print("static: ", static.__doc__)
        print("color_static: ", color_static.__doc__)
        print("stars: ", stars.__doc__)
