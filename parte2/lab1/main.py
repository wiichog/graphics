import pygame
import random

pygame.init()

RED = (255,0,0)

render = pygame.display.set_mode((800,600))

while True:
    x = random.randint(0,800)
    y = random.randint(0,600)
    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)
    color = (r,g,b)
    render.set_at((x,y), color)#this is only for one point
    #we can use get_at
    pygame.display.flip()
    pass