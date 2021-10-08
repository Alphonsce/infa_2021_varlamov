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
global_time = 0
points = 0

def new_ball(x, y, r, velx, vely):
    ''' задает параметры нового шарика
    '''
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
    if dic['x'] <= dic['r']:
        dic['velx'] *= -1
    if dic['x'] >= WIDTH - dic['r']:
        dic['velx'] *= -1
    if dic['y'] <= dic['r']:
        dic['vely'] *= -1
    if dic['y'] >= HEIGHT - dic['r']:
        dic['vely'] *= -1
    

def click(event):
    '''функция, возвращающая координаты указателя мыши'''
    return(event.pos)
    
clock = pygame.time.Clock()
finished = False
list_of_dics = []
list_of_dics.append(new_ball(random.randint(100, 1100), random.randint(100, 800), random.randint(30, 50), random.randint(-6, 6), random.randint(-6, 6)))

while not finished:
    if global_time % 15 == 0:
        list_of_dics.append(new_ball(random.randint(100, 1100), random.randint(100, 800), random.randint(30, 50), random.randint(-6, 6), random.randint(-6, 6)))
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or global_time >= 30 * 60:
            finished = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            x_mouse, y_mouse = click(event)        
            for dic in list_of_dics:
                if (x_mouse - dic['x']) ** 2 + (y_mouse - dic['y']) ** 2 <= r ** 2 + 1:
                    list_of_dics.remove(dic)
                    points += 5 * (abs(dic['velx']) + abs(dic['vely'])) + 3 * (70 - dic['r'])


    for dic in list_of_dics:     
        cur_x, cur_y, r = dic['x'], dic['y'], dic['r']
        move_ball(dt)
        circle(screen, dic['color'], (cur_x, cur_y), r)
        if dic['t'] >= 60:
            list_of_dics.remove(dic)

    # создание Surface с текстом
    font = pygame.font.Font('freesansbold.ttf', 22)
    text = font.render(f'Score: {points}', True, GREEN, BLUE)
    text1 = font.render(f'Time left: {60 - global_time // 30}', True, GREEN, BLUE)
    textRect = text.get_rect()
    text1Rect = text.get_rect()
    textRect.center = (WIDTH // 16, HEIGHT // 16)
    text1Rect.center = (WIDTH * 14 // 16, HEIGHT // 16)
    screen.blit(text, textRect)
    screen.blit(text1, text1Rect)    
    pygame.display.update()
    screen.fill(BLACK)

    global_time += 1


pygame.quit()