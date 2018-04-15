import struct

def color(r,g,b):
    return bytes([b,g,r])

BLACK = color(0,0,0)
WHITE = color(255,255,255)


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

    def color(self,color):
        r,g,b = color
        return bytes([b,g,r])

    def clear(self):
        self.pixels = [
            [WHITE for x in range(self.width)]
            for y in range(self.height)
        ]
    
    def write(self,filename):
        f = open(filename,'bw')
         #HEADER
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14+40+self.width * self.height *3))
        f.write(dword(0))
        f.write(dword(14+40))

        #IMAGE HEADER (40 BYTES)
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

    def point(self,x,y,color=None):
        self.pixels[y][x] = color or self.current_color
        
    def set_color(self,color):
        self.current_color = color
    
    def line(self, start, end, color):
        x1, y1 = start
        x2, y2 = end

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
                self.point(y, x, self.color(color))
            else:
                self.point(x, y, self.color(color))
            
            offset += dy * 2
            if offset >= threshold:
                y += 1 if y1 < y2 else -1
                threshold += dx * 2

