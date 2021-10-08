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
time_game_lasts = 30
squares_spawned = 5
square_lives = 5

# writing_f = open('results.txt', mode='rt')
# reading_f = open('results.txt', mode='rt')

def new_ball(x, y, r, velx, vely):
    ''' задает параметры нового шарика '''
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
    ''' функция, двигающая шарик каждую итерацию цикла '''
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

def new_square(x, y, velx, vely, when_spawned):
    ''' функция, которая создает движущийся квадратик, при нажатии на который, он каждый раз
        увеличивает свою скорость в 2 раза, появляется squares_spawned раз во время игры в случайные моменты
        времени на square_lives секунд.
    '''
    dic = {}
    dic['x'] = x
    dic['y'] = y
    dic['a'] = 70
    dic['velx'] = velx
    dic['vely'] = vely
    dic['t'] = 0
    dic['color'] = YELLOW
    dic['when'] = when_spawned
    return dic

def move_square(dt, times_clicked=1):
    ''' функция, двигающая квадратик '''
    dic['x'] += dic['velx']
    dic['y'] += dic['vely']
    dic['t'] += dt
    dic['velx'] *= times_clicked
    dic['vely'] *= times_clicked
    if dic['x'] <= 0:
        dic['velx'] *= -1
    if dic['x'] >= WIDTH - dic['a']:
        dic['velx'] *= -1
    if dic['y'] <= 0:
        dic['vely'] *= -1
    if dic['y'] >= HEIGHT - dic['a']:
        dic['vely'] *= -1

def click(event):
    '''функция, возвращающая координаты указателя мыши'''
    return(event.pos)
    
clock = pygame.time.Clock()
finished = False
list_of_dics = []
list_of_dics.append(new_ball(random.randint(100, 1100), random.randint(100, 800), random.randint(30, 50), random.randint(-6, 6), random.randint(-6, 6)))
list_of_squares = []
for _ in range(squares_spawned):
    list_of_squares.append(new_square(random.randint(100, 1100), 
    random.randint(100, 800), [-7, -6, -5, -4, 4, 5, 6, 7][random.randint(0, 7)], [-7, -6, -5, -4, 4, 5, 6, 7][random.randint(0, 7)], random.randint(1, time_game_lasts * 0.85 // 1)))

while not finished:
    ''' шарики появляются раз в полсекунды '''
    if global_time % 15 == 0:
        list_of_dics.append(new_ball(random.randint(100, 1100), random.randint(100, 800), random.randint(30, 50), random.randint(-6, 6), random.randint(-6, 6)))
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or global_time >= 30 * time_game_lasts:
            finished = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            x_mouse, y_mouse = click(event)        
            for dic in list_of_dics:
                if (x_mouse - dic['x']) ** 2 + (y_mouse - dic['y']) ** 2 <= dic['r'] ** 2 + 1:
                    list_of_dics.remove(dic)
                    points += 5 * (abs(dic['velx']) + abs(dic['vely'])) + 3 * (70 - dic['r'])

    for dic in list_of_squares:
        if global_time >= dic['when'] * 30:
            rect(screen, dic['color'], [dic['x'], dic['y'], dic['a'], dic['a']])
            move_square(dt, 1)
            if dic['t'] >= square_lives * 30:
                list_of_squares.remove(dic)

    for dic in list_of_dics:     
        move_ball(dt)
        circle(screen, dic['color'], (dic['x'], dic['y']), dic['r'])
        if dic['t'] >= 60:
            list_of_dics.remove(dic)

    # создание Surface с текстом
    font = pygame.font.Font('freesansbold.ttf', 22)
    text = font.render(f'Score: {points}', True, GREEN, BLUE)
    text1 = font.render(f'Time left: {30 - global_time // 30}', True, GREEN, BLUE)
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