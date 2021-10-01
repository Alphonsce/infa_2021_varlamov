import pygame
from pygame.draw import *

FPS = 15
BLUE = (95, 188, 211)
YELLOW = (200, 171, 55)
GREY = (108, 103, 83)
WHITE = (254, 254, 254)
BLACK = (0, 0, 0)
GREEN = (55, 200, 113)
LIGHT_GRAY = (211, 211, 211)

# чтобы много заборов сделать в третьем задании создаю сразу класс для забора:
# lines_in_wall - число полосок в заборе, left_x и start_y задают левый верхний угол забора
# where - это Surface, где будет находится стена.
class wall:
    def __init__(self, where, lines_in_wall, length, width, left_x, start_y):
        self.where = where
        self.lines = lines_in_wall
        self.leng = length
        self.wid = width
        self.left_x = left_x
        self.start_y = start_y
    def draw(self):
        rect(self.where, YELLOW, [self.left_x, self.start_y, self.wid, self.leng])
        rect(self.where, LIGHT_GRAY, [self.left_x, self.start_y, self.wid, self.leng], 1)
        for i in range(1, self.lines):
            x = self.left_x + self.wid // self.lines * i
            line(self.where, BLACK, [x, self.start_y], [x, self.start_y + self.leng])
        line(self.where, BLACK, [self.left_x, self.start_y + self.leng], [self.left_x + self.wid, self.start_y + self.leng])

# далее все Surface'ы создаются через .copy(), чтобы избежать рисования на основном дисплее, то есть
# мы при создании нужного нам Surface, который мы потом будем blit'ить с основным Surface
# делаем так, чтобы при создании до блита ничего на дисплее не рисовалось. Также для всех Surface'ов
# мы сразу создаем объекты get_rect, чтобы быть готовыми их blit'ить.

# Walls:
# здесь создаются экземпляры стенок
wall_surface = pygame.display.set_mode((800, 800)).copy()
wall_rect = wall_surface.get_rect(center=(400, 400))
wa0 = wall(wall_surface, 15, 300, 700, 100, 50)
wa0.draw()
wa2 = wall(wall_surface, 15, 400, 500, 0, 100)
wa2.draw()
wa1 = wall(wall_surface, 15, 300, 300, 0, 250)
wa1.draw()
wa3 = wall(wall_surface, 15, 200, 400, 400, 350)
wa3.draw()

# Dog:
dog_surface = pygame.display.set_mode((800, 800)).copy()
dog_surface.set_colorkey((255, 255, 255))
dog_rect = dog_surface.get_rect(center=(0, 0))

#   Body:
ellipse(dog_surface, GREY, [110, 460, 180, 90])
ellipse(dog_surface, GREY, [220, 450, 100, 70])
circle(dog_surface, GREY, [240, 480], 30)
ellipse(dog_surface, GREY, [250, 460, 30, 115])
ellipse(dog_surface, GREY, [218, 560, 50, 20])
circle(dog_surface, GREY, [315, 495], 30)
ellipse(dog_surface, GREY, [305, 470, 30, 115])
ellipse(dog_surface, GREY, [274, 570, 50, 20])
ellipse(dog_surface, GREY, [95, 485, 45, 110])
ellipse(dog_surface, GREY, [65, 580, 60, 20])
ellipse(dog_surface, GREY, [180, 510, 45, 110])
ellipse(dog_surface, GREY, [150, 605, 60, 20])

#    Head:
rect(dog_surface, GREY, [100, 450, 80, 80])
rect(dog_surface, BLACK, [100, 450, 80, 80], 1)
circle(dog_surface, GREY, [100, 460], 12)
circle(dog_surface, BLACK, [100, 460], 12, 1)
circle(dog_surface, GREY, [180, 460], 12)
circle(dog_surface, BLACK, [180, 460], 12, 1)
arc(dog_surface, BLACK, [105, 505, 70, 40], 0.2, 2.7)
polygon(dog_surface, WHITE, [[125, 507], [130, 490], [135, 505]])
polygon(dog_surface, BLACK, [[125, 507], [130, 490], [135, 505]], 1)
polygon(dog_surface, WHITE, [[165, 510], [160, 492], [155, 509]])
polygon(dog_surface, BLACK, [[165, 510], [160, 492], [155, 509]], 1)
ellipse(dog_surface, WHITE, [115 ,475, 20, 10])
ellipse(dog_surface, BLACK, [115 ,475, 20, 10], 1)
circle(dog_surface, BLACK, [125, 480], 5)
circle(dog_surface, BLACK, [125, 480], 5)
ellipse(dog_surface, WHITE, [150 ,475, 20, 10])
ellipse(dog_surface, BLACK, [150 ,475, 20, 10], 1)
circle(dog_surface, BLACK, [160, 480], 5)
circle(dog_surface, BLACK, [160, 480], 5)

# Здесь мы меняем конфигурации всех собак
# методы pygame.transform возвращают нам новый измененный указанным образом Surface
dog_1_surface = dog_surface.copy()
dog_1_rect = dog_surface.get_rect(center=(400, 400))

dog_2_surface = pygame.transform.flip(dog_surface.copy(), True, False)
dog_2_rect = dog_surface.get_rect(center=(0, 550))

dog_3_surface = pygame.transform.flip(dog_surface.copy(), True, False)
dog_3_rect = dog_surface.get_rect(center=(500, 380))

dog_4_surface = pygame.transform.scale2x(dog_surface.copy())
dog_4_rect = dog_4_surface.get_rect(center=(1200, 500))

# Dog house:
house_surface = pygame.display.set_mode((800, 800)).copy()
house_rect = house_surface.get_rect(center=(400, 400))
polygon(house_surface, YELLOW, [[600, 420], [520, 480], [640, 545]])
polygon(house_surface, BLACK, [[600, 420], [520, 480], [640, 545]], 1)
polygon(house_surface, YELLOW, [[600, 420], [640, 545], [640 + 40, 545 - 20], [600 + 40, 420 - 20]])
polygon(house_surface, BLACK, [[600, 420], [640, 545], [640 + 40, 545 - 20], [600 + 40, 420 - 20]], 1)
polygon(house_surface, YELLOW, [[520, 480], [520, 480 + 90], [640, 545 + 90], [640, 545]])
polygon(house_surface, BLACK, [[520, 480], [520, 480 + 90], [640, 545 + 90], [640, 545]], 1)
polygon(house_surface, YELLOW, [[640, 545], [680, 525], [680, 595], [640, 635]])
polygon(house_surface, BLACK, [[640, 545], [680, 525], [680, 595], [640, 635]], 1)
circle(house_surface, BLACK, [575, 555], 25)

# chain:
chain_surface = pygame.display.set_mode((800, 800)).copy()
chain_rect = chain_surface.get_rect(center=(400, 400))
chain_surface.set_colorkey((255, 255, 255))
ellipse(chain_surface, BLACK, [570 - 30 / 1.4, 555 + 17 / 1.4, 25, 15], 1)
circle(chain_surface, BLACK, [536, 586], 10, 1)
circle(chain_surface, GREY, [545, 575], 8)
circle(chain_surface, BLACK, [545, 575], 8, 1)
ellipse(chain_surface, BLACK, [508, 590, 30, 10], 1)
circle(chain_surface, BLACK, [505, 598], 8, 1)
ellipse(chain_surface, BLACK, [462, 593, 40, 15], 1)
circle(chain_surface, BLACK, [455, 599], 10, 1)
ellipse(chain_surface, BLACK, [425, 592, 30, 5], 1)
circle(chain_surface, BLACK, [420, 592], 10, 1)
ellipse(chain_surface, BLACK, [392, 593, 25, 10], 1)
ellipse(chain_surface, BLACK, [372, 598, 25, 10], 1)

# Экран и фон
screen = pygame.display.set_mode((800, 800))
rect(screen, BLUE, [0, 0 , 800, 800 / 2], 0)
polygon(screen, GREEN, [[0, 800], [0, 400], [800, 400], [800, 800]])

# Здесь происходит отрисовка всего на дисплее, мы blit'им наши Surface'ы в указанной для них rect области
# в один общий Surface. Удобство заключается в том, что мы можем спокойно выбрать порядок отрисовки, а не двигать
# огромные куски кода, чтобы указать порядок.
screen.blit(wall_surface, wall_rect)
screen.blit(dog_1_surface, dog_1_rect)
screen.blit(dog_2_surface, dog_2_rect) 
screen.blit(dog_3_surface, dog_3_rect)
screen.blit(house_surface, house_rect)
screen.blit(chain_surface, chain_rect)
screen.blit(dog_4_surface, dog_4_rect)

pygame.init()
pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()