import pygame
from pygame.draw import *
import numpy
import random

# A and B are speeds
# WIDTH and HIGHT are sizes of the display
WIDTH = 800
HEIGHT = 800
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def draw_little_bird(x_little_bird, y_little_bird, size_of_little_bird, angle_of_little_bird):
    """ Функция рисует дальнюю птицу. 
    x_little_bird, y_little_bird - Указываются координаты верхнего угла рисунка с птицей.
    size_of_little_bird - размер рисунка в пикселях
    angle_of_little_bird - наклон птицы влево в градусах.
    Ничего не возвращает.
    """
    global outside_surface
    bird_surface = pygame.Surface((size_of_little_bird * 2, size_of_little_bird), pygame.SRCALPHA)
    outside_surface = bird_surface
    bird_surface.fill((0, 0, 0, 0))
    arc(bird_surface, (255, 255, 255), 
        [size_of_little_bird, 0, size_of_little_bird, size_of_little_bird / 2], 
        numpy.pi/2, numpy.pi, 3)
    arc(bird_surface, (255, 255, 255), 
        [0, 0, size_of_little_bird, size_of_little_bird / 2], 
        0, numpy.pi / 2, 3)
    screen.blit(pygame.transform.rotate(bird_surface, angle_of_little_bird), (x_little_bird - size_of_little_bird, y_little_bird))

screen = pygame.display.set_mode((400, 400))
draw_little_bird(50, 400, 60, 0)

class moving_object(pygame.sprite.Sprite):
    def __init__(self, Vx, Vy):
        pygame.sprite.Sprite.__init__(self)
        self.image = outside_surface
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.Vx = Vx
        self.Vy = Vy
        
        
    def update(self):
        self.rect.x += self.Vx
        self.rect.y += self.Vy
#        self.image = pygame.transform().scale(outside_surface, (400, 400), (400, 400))

# Создаем игру и окно
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
for i in range(5):
    i = moving_object(random.randint(-5, 5), random.randint(-5, 5))
    all_sprites.add(i)
bird1 = moving_object(1, 1)
bird2 = moving_object(-1, -1)
all_sprites.add(bird1, bird2)

# Цикл игры
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновление
    all_sprites.update()
    
    # Рендеринг
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()