# unworking version without moving surfaces

import math
import random
import pygame


FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600

bullet = 0
balls = []

class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = random.choice(GAME_COLORS)
        self.live = FPS * 3
        self.g = 2.5

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx
        self.y += self.vy
        self.vy += self.g

        if self.x >= WIDTH - self.r:
            self.vx *= -1

        if self.y >= HEIGHT - self.r:
            self.vy *= -1

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )
        pygame.draw.circle(
            self.screen,
            BLACK,
            (self.x, self.y),
            self.r,
            1
        )

    def hittest(self, other):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (self.x - other.x) ** 2 + (self.y - other.y) ** 2 <= (self.r + other.r) ** 2:
            return True

        return False


class Gun:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x = x
        self.y = y

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.pos[1]-450) / ((event.pos[0]-20)))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        gun_surf1 = pygame.Surface((200, 200))
        gun_surf1.fill(WHITE)
        pygame.draw.rect(gun_surf1, self.color, [100, 95, 40 + self.f2_power / 2, 10])
        gun_surf1 = pygame.transform.rotate(gun_surf1, - self.an * 180 / 3.14)
        gun_surf_rect = gun_surf1.get_rect()
        screen.blit(gun_surf1, (self.x - gun_surf_rect.width / 2, self.y - gun_surf_rect.height / 2))
        

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    def __init__(self):
        self.x = random.randint(600, 780)
        self.y = random.randint(300, 550)
        self.r = random.randint(2, 50)
        self.vx = random.randint(-2, 2)
        self.vy = random.randint(-2, 2)
        self.target_surf = pygame.Surface((self.x + self.r, self.y + self.r))
        self.target_surf = self.target_surf.convert_alpha()
        self.target_surf.fill((0, 0, 0, 0))
        self.color = random.choice(GAME_COLORS)


    def new_target(self):
        """ Инициализация новой цели. """
        self.__init__()

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def move_target(self):
        self.x += self.vx
        self.y += self.vy
        self.target_surf.fill(BLACK)

        if self.x >= WIDTH - self.r:
            self.vx *= -1

        if self.y >= HEIGHT - self.r:
            self.vy *= -1

        if self.x <= 0 + self.r:
            self.vx *= -1

        if self.y <= 0 + self.r:
            self.vy *= -1


    def hit(self):
        self.target_surf.fill(WHITE)

    def draw(self):
        pygame.draw.circle(self.target_surf, self.color, [self.x, self.y], self.r)
        screen.blit(self.target_surf, self.target_surf.get_rect())


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

target = Target()
target1 = Target()
targets = [target, target1]
gun = Gun(screen, 20, 450)

finished = False

while not finished:
    screen.fill(WHITE)
    for tar in targets:
        tar.draw()
    gun.draw()
    for b in balls:
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for b in balls:
        b.move()
        for tar in targets: 
            if b.hittest(tar):
                tar.hit()
                tar.new_target()
        b.live -= 1
        if b.live <= 0:
            balls.remove(b)

    for tar in targets:
        tar.move_target()
    gun.power_up()

pygame.quit()
