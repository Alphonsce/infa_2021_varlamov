import pygame
import random
from pygame.draw import *
pygame.init()

FPS = 1
screen = pygame.display.set_mode((1200, 900))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

def new_ball(x, y, r, vel):
    '''рисует новый шарик '''
    dic = {}
    dic['x'] = x
    dic['y'] = y
    dic['r'] = r
    dic['vel'] = vel
    return dic

def click(event):
    return(event.pos)
    

pygame.display.update()
clock = pygame.time.Clock()
finished = False

numb = 0
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            x_mouse, y_mouse = click(event)   

    dic1 = new_ball(random.randint(50, 1100), random.randint(40, 800), random.randint(30, 50), 0)
    cur_x, cur_y, r = dic1['x'], dic1['y'], dic1['r']
    circle(screen, COLORS[random.randint(1, 5)], (cur_x, cur_y), r)
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()