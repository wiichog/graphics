import sys
import random
from render import Render


def house():
    """
    Draws lines from every corner
    """
    r = Render(800, 600)
    #first rooftop
    for i in range(187):
        r.line((i + 98,411), (i + 426,599),(164,0,0))
    
    #second rooftop
    for i in range(510):
        r.line((i+285,411), (468,193),(204,0,0))
    for i in range(330):
        r.line((288+i,412), (615,599),(204,0,0))
    for i in range(185):
        r.line((615,599),(610+i,412),(204,0,0))
    #wall where is the door
    for i in range(325):
        r.line((138,168),(286,411-i),(186,189,182))
    for i in range(147):
        r.line((138,168),(139+i,410),(186,189,182))
    for i in range(168):
        r.line((428,241),(287,241+i),(186,189,182))
    for i in range(142):
        r.line((429,3),(287+i,240),(186,189,182))
    for i in range(154):
        r.line((429,3),(287,86+i),(186,189,182))
    #door
    for i in range(176):
        r.line((238,110), (322,240-i),(143,89,2))
    for i in range(187):
        r.line((323,240),(238,111+i),(143,89,2))
    #wall of windows with shadow
    for i in range(-46,46):
        r.line((469,193),(429,193-i),(186,189,182))
    for i in range(15):
        r.line((471,184),(757,385-i),(186,189,182))
    for i in range(90):
         r.line((757,385),(471,194-i),(186,189,182))
    for i in range(15):
         r.line((449,170),(471,195-i),(186,189,182))
    #wall of windows
    for i in range(177):
        r.line((429,3),(756,194+i),(211,215,207))
    for i in range(153):
        r.line((756,371),(428,3+i),(211,215,207))
    r.line((428,4),(428,242),(0,0,0))
    #windows
    for i in range(101):
        r.line((531,134),(656,205+i),(52,101,164))
    for i in range(89):
        r.line((657,305),(532,134+i),(52,101,164))
    #shadow for windows
    for i in range(14):
        r.line((657,305),(532,222+i),(32,74,135))
    for i in range(14):
        r.line((533,235),(657,318-i),(32,74,135))
    
    

    #289
    #205
    
    
    r.display('out.bmp')

if __name__ == "__main__":
    example = sys.argv[1] if len(sys.argv) > 1 else ""
    if example == "house":
        house()