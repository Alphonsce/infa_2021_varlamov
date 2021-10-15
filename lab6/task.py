import pygame
import random
import pathlib
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
time_game_lasts = 5
squares_spawned = 3
square_lives = 5
leaderboard = []

name = input('Введите имя, чтобы начать: ')
# создания файлов для записи таблицы лидеров

reading_f = open('write_lead.txt', mode='rt')
writing_f = open('write_lead.txt', mode='a')

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
    ''' функция, двигающая шарик каждую итерацию цикла
        dt позволяет считать время и по прошествии определенного числа
        просто удалять шарик.
     '''
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
        увеличивает свою скорость, появляется squares_spawned раз во время игры в случайные моменты
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
    dic['times_clicked'] = 0
    return dic

def move_square(dt):
    ''' функция, двигающая квадратик '''
    dic['x'] += dic['velx']
    dic['y'] += dic['vely']
    dic['t'] += dt
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
                if (abs(x_mouse - dic['x']) <= dic['a']) and (abs(y_mouse - dic['y']) <= dic['a']):
                    dic['times_clicked'] += 1
                    dic['velx'] *= 1.1 ** dic['times_clicked']
                    dic['vely'] *= 1.1 ** dic['times_clicked']
                    points += 300

    for dic in list_of_squares:
        if global_time >= dic['when'] * 30:
            rect(screen, dic['color'], [dic['x'], dic['y'], dic['a'], dic['a']])
            move_square(dt)
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

# запись в файл
line = name + ': ' + str(points)
writing_f.write(name + ': ' + str(points) + '\n')
writing_f.close()

# считывание лидеров из файла для записи на экран:
already_played = len(reading_f.readlines())
reading_f.seek(0)
for _ in range(already_played):
    leaderboard.append(reading_f.readline().strip())
leaderboard = sorted(leaderboard, key=lambda x: int(x.split()[-1]), reverse=True)

# отображение таблицы лидеров:
finished = False
while not finished:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
    font = pygame.font.Font('freesansbold.ttf', 22)
    text = font.render(f'Leaderboards:', True, BLUE)
    text0 = font.render(leaderboard[0], True, GREEN)
    text1 = font.render(leaderboard[1], True, GREEN)
    text2 = font.render(leaderboard[2], True, GREEN)
    textRect = text.get_rect()
    text0Rect = text.get_rect()
    text1Rect = text.get_rect()
    text2Rect = text.get_rect()
    textRect.center = (WIDTH // 2, HEIGHT // 16)
    text0Rect.center = (WIDTH  // 2, HEIGHT // 10)
    text1Rect.center = (WIDTH  // 2, HEIGHT // 10 + 100)
    text2Rect.center = (WIDTH  // 2, HEIGHT // 10 + 200)
    screen.blit(text, textRect)
    screen.blit(text0, text0Rect)
    screen.blit(text1, text1Rect)
    screen.blit(text2, text2Rect)    
    pygame.display.update()
    

pygame.quit()