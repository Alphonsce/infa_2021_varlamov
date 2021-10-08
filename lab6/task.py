import pygame
import random
from pygame.draw import *
pygame.init()

FPS = 30
WIDTH = 1200
HEIGHT = 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

dt = 1
glob_t = 0
points = 0

def new_ball(x, y, r, velx, vely):
    '''рисует новый шарик '''
    dic = {}
    dic['x'] = x
    dic['y'] = y
    dic['r'] = r
    dic['velx'] = velx
    dic['vely'] = vely
    dic['t'] = 0
    dic['color'] = COLORS[random.randint(1, 5)]
    return dic

def move_ball(dt):
    '''функция, двигающая шарик каждую итерацию цикла'''
    dic['x'] += dic['velx']
    dic['y'] += dic['vely']
    dic['t'] += dt

def click(event):
    return(event.pos)
    
clock = pygame.time.Clock()
finished = False
list_of_dics = []
list_of_dics.append(new_ball(random.randint(100, 1100), random.randint(100, 800), random.randint(30, 50), random.randint(-6, 6), random.randint(-6, 6)))

while not finished:
    if glob_t % 15 == 0:
        list_of_dics.append(new_ball(random.randint(100, 1100), random.randint(100, 800), random.randint(30, 50), random.randint(-6, 6), random.randint(-6, 6)))
    clock.tick(FPS)
    hit_marker = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            x_mouse, y_mouse = click(event)


    for dic in list_of_dics:
        cur_x, cur_y, r = dic['x'], dic['y'], dic['r']
        move_ball(dt)
        circle(screen, dic['color'], (cur_x, cur_y), r)
        if dic['t'] >= 60:
            list_of_dics.remove(dic)
        
    pygame.display.update()
    screen.fill(BLACK)
    glob_t += 1

pygame.quit()