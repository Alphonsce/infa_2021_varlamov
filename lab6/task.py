import pygame
import random
import pathlib
from pygame.draw import *
pygame.init()

# -------------CONSTANTS-----------------
FPS = 30
WIDTH = 1200
HEIGHT = 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

dt = 1
global_time_ = 0
points = 0
leaderboard = []
time_game_lasts = 20
squares_spawned = 2
square_lives = 5
ball_spawn_part_of_a_second = 2 / 3
# -------------------------------

def click(event):
        '''функция, возвращающая координаты указателя мыши'''
        return(event.pos)


def menu(finished=False, touched_play=False):
    '''функция, которая меню создает'''
    while not finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or touched_play:
                finished = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                x_mouse, y_mouse = click(event)
                if 537 < x_mouse < 663 and 286 < y_mouse < 312:
                    game()
                elif 446 < x_mouse < 502 and 444 < y_mouse < 460:
                    end_of_game()
        font = pygame.font.Font('freesansbold.ttf', 32)
        menu_text = font.render('START!', True, WHITE)
        text_menu_Rect = menu_text.get_rect()
        text_menu_Rect.center = (WIDTH // 2, HEIGHT // 3)
        screen.blit(menu_text, text_menu_Rect)

        exit_text = font.render('EXIT', WHITE, WHITE)
        exit_rect = menu_text.get_rect()
        exit_rect.center = (WIDTH // 2.3, HEIGHT // 2)
        screen.blit(exit_text, exit_rect)
        pygame.display.update()
        screen.fill(BLACK)
    
        

def game(global_time=global_time_, finished=False, dt=1):
    '''функция, запускающая игру'''
    global points, leaderboard
    points = 0
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
        ''' шарики появляются раз ball_spawn_part_of_a_second части секунды '''
        if global_time % 30 * ball_spawn_part_of_a_second == 0:
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
    reading_f = open('write_lead.txt', mode='rt')
    writing_f = open('write_lead.txt', mode='a')

    line = str(points)
    writing_f.write(line + '\n')
    writing_f.close()
    # считывание лидеров из файла для записи на экран:
    already_played = len(reading_f.readlines())
    reading_f.seek(0)
    for _ in range(already_played):
        leaderboard.append(reading_f.readline().strip())
    leaderboard = sorted(leaderboard, key=lambda x: int(x.split()[-1]), reverse=True)
    end_of_game()

def end_of_game(finished=False):
    '''функция, выводящая таблицу рекордов и две кнопочки по окончании игры'''
    global end_this_please
    x_mouse, y_mouse = -13, -13
    while not finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                x_mouse, y_mouse = click(event)
        font = pygame.font.Font('freesansbold.ttf', 22)
        text = font.render('Leaderboards:', True, RED)
        text0 = font.render(leaderboard[0], True, WHITE)
        text1 = font.render('', True, GREEN)
        text2 = font.render('', True, GREEN)
        if len(leaderboard) > 1:
            text1 = font.render(leaderboard[1], True, WHITE)
        if len(leaderboard) > 2:
            text2 = font.render(leaderboard[2], True, WHITE)
        textRect = text.get_rect()
        text0Rect = text.get_rect()
        text1Rect = text.get_rect()
        text2Rect = text.get_rect()
        textRect.center = (WIDTH // 2, HEIGHT // 16)
        text0Rect.center = (WIDTH  // 1.9, HEIGHT // 10 + 50)
        text1Rect.center = (WIDTH  // 1.9, HEIGHT // 10 + 100)
        text2Rect.center = (WIDTH  // 1.9, HEIGHT // 10 + 150)
        screen.blit(text, textRect)
        screen.blit(text0, text0Rect)
        screen.blit(text1, text1Rect)
        screen.blit(text2, text2Rect)

        exit_text = font.render('EXIT', WHITE, BLUE)
        back_to_menu = font.render('BACK TO MENU', WHITE, BLUE)
        exit_rect = text.get_rect()
        back_rect = text.get_rect()
        exit_rect.center = (WIDTH // 2.3, HEIGHT // 2)
        back_rect.center = (WIDTH // 2.3, HEIGHT // 1.5)
        screen.blit(exit_text, exit_rect)
        screen.blit(back_to_menu, back_rect)
        pygame.display.update()

        if 446 < x_mouse < 502 and 444 < y_mouse < 460:
            exit(0)
        elif 446 < x_mouse < 616 and 594 < y_mouse < 610:
            menu()

# запуск функции с меню, которая дальше ведет к игре, игра ведет к итоговому меню, которое либо ведет обратно либо заканчивает всё.   
menu(False, False)

pygame.quit()