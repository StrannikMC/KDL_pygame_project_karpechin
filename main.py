import pygame
import sys
from pygame.locals import *
import random
import time

pygame.init()

# Устанавливаем частоту обновления
FPS = 60
FramePerSec = pygame.time.Clock()

# основные цвета
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Переменные для игры
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0

# подключаем шрифты
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("AnimatedStreet.png")

# создаем экран и заполняем белым цветом
DISPLAYSURF = pygame.display.set_mode((400, 600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")


# класс Противник, рандомное появление, перемещается сверху вниз
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > 600:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


# класс игрок, перемещение происходит влево-вправо. Закомментированная область кода для перемещения вверх-вниз
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        # if pressed_keys[K_UP]:
        # self.rect.move_ip(0, -5)
        # if pressed_keys[K_DOWN]:
        # self.rect.move_ip(0,5)

        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)


class Background:
    def __init__(self):
        self.bgimage = pygame.image.load('AnimatedStreet.png')
        self.rectBGimg = self.bgimage.get_rect()

        self.bgY1 = 0
        self.bgX1 = 0

        self.bgY2 = self.rectBGimg.height
        self.bgX2 = 0

        self.movingUpSpeed = 5

    def update(self):
        self.bgY2 += self.movingUpSpeed
        self.bgY1 += self.movingUpSpeed
        if self.bgY2 >= self.rectBGimg.height:
            self.bgY2 = -self.rectBGimg.height
        if self.bgY1 >= self.rectBGimg.height:
            self.bgY1 = -self.rectBGimg.height

    def render(self):
        DISPLAYSURF.blit(self.bgimage, (self.bgX1, self.bgY1))
        DISPLAYSURF.blit(self.bgimage, (self.bgX2, self.bgY2))


class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


# Загружаем объекты
P1 = Player()
E1 = Enemy()
back_ground = Background()

# Собираем группы, позволяет управлять спрайтами сразу
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

# подключаем счетчик через событие
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)


def main_menu():
    while True:
        DISPLAYSURF.fill(WHITE)

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = font.render("МЕНЮ", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(200, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("Play Rect.png"), pos=(200, 250),
                             text_input="ИГРАТЬ", font=font, base_color="#d7fcd4", hovering_color="White")

        QUIT_BUTTON = Button(image=pygame.image.load("Quit Rect.png"), pos=(200, 450),
                             text_input="ВЫХОД", font=font, base_color="#d7fcd4", hovering_color="White")

        DISPLAYSURF.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(DISPLAYSURF)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


def play():
    SPEED = 5
    # основной цикл
    while True:

        # проходим по всем событиям, при возникновении события quit завершаем игру
        for event in pygame.event.get():
            if event.type == INC_SPEED:
                SPEED += 0.5
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # отрисовываем текст используя рендер шрифта, обновляем каждый тик
        back_ground.update()
        back_ground.render()
        scores = font_small.render(str(SCORE), True, BLACK)
        DISPLAYSURF.blit(scores, (10, 10))

        # перерисовываем спрайты по их перемещению
        for entity in all_sprites:
            DISPLAYSURF.blit(entity.image, entity.rect)
            entity.move()

        # проверяем столкновение, если столкновение произошло, проигрываем звук проигрыша и окно завершения
        if pygame.sprite.spritecollideany(P1, enemies):
            pygame.mixer.Sound('crash.wav').play()
            time.sleep(0.5)

            DISPLAYSURF.fill(RED)
            DISPLAYSURF.blit(game_over, (30, 250))

            pygame.display.update()
            for entity in all_sprites:
                entity.kill()
            time.sleep(2)
            main_menu()

        pygame.display.update()
        FramePerSec.tick(FPS)


main_menu()
