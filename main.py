import datetime
import os
import random
import sys

import pygame
import sqlite3


def load_image(name, colorkey=None):  # Загрузка картинки из data
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def start_screen():  # Начальное окно
    fon = pygame.transform.scale(load_image('camera-player/fon.png'),
                                 (800, 500))
    screen.blit(fon, (0, 0))
    pygame.display.flip()
    clock.tick(0.7)
    screen.fill((0, 0, 0))


class Background(pygame.sprite.Sprite):  # Задний фон
    def __init__(self, image_path, size):
        super().__init__(background_group, all_sprites)
        self.image = load_image(image_path)
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_threshold(self.image, (237, 28, 36), (1, 1, 1, 255))

    def get_rgb(self, x, y):  # Возвращение цвета о пикселе фона
        pixel = pygame.PixelArray(self.image)
        print(x, y)
        return self.image.unmap_rgb(pixel[x][y])

    def update(self, imageBoss, size):
        self.image = load_image(imageBoss)
        self.image = pygame.transform.scale(self.image, size)


class Camera:  # Камера, движение за игроком
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):  # камера на объекте target
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


class Player(pygame.sprite.Sprite):  # Игрок
    image = load_image('players_image/m.c.front_stop.png')
    image = pygame.transform.scale(image, (40, 60))

    def __init__(self, pos_x, pos_y, stena, key=False, pas=False):
        super().__init__(player_group, all_sprites)
        self.image = Player.image
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.x = pos_x + 20
        self.y = pos_y + 60
        self.step = 1
        self.back = False
        self.last_skin_change_time = 0
        self.direction = ''
        self.mask = pygame.mask.from_surface(self.image)
        self.loc = 0
        self.key = key
        self.pas = pas
        self.run = 5
        self.vis = True
        self.apples = 0
        self.task_text = 0
        self.ones = True
        if stena == 1:
            self.stena = [(2, 0, 0)]
        elif stena == 2:
            self.stena = [(34, 177, 76), (0, 162, 232), (54, 19, 11),
                          (0, 8, 4), (4, 28, 16), (15, 69, 10), (18, 89, 22)]
        elif stena == 3:
            self.stena = [(153, 217, 234), (185, 122, 87), (0, 162, 232),
                          (187, 122, 87), (0, 187, 255), (55, 71, 79),
                          (38, 52, 58), (71, 92, 102)]

    def stop(self):  # Анимация игрока при остановке
        image = self.image
        if self.vis:
            if self.direction == 'left':
                image = load_image('players_image/m.c.left_stop.png')
            elif self.direction == 'right':
                image = load_image('players_image/m.c.right_stop.png')
            elif self.direction == 'down':
                image = load_image('players_image/m.c.front_stop.png')
            elif self.direction == 'up':
                image = load_image('players_image/m.c.back_stop.png')
        else:
            if self.direction == 'left':
                image = load_image('players_image/m.c.left_stop_trans.png')
            elif self.direction == 'right':
                image = load_image('players_image/m.c.right_stop_trans.png')
            elif self.direction == 'down':
                image = load_image('players_image/m.c.front_stop_trans.png')
            elif self.direction == 'up':
                image = load_image('players_image/m.c.back_stop_trans.png')
        self.image = pygame.transform.scale(image, (40, 60))

    def update(self, move_up, move_down, move_left, move_right):
        global all_sprites, player, background
        image = self.image
        current_time = pygame.time.get_ticks()

        if move_left:  # Анимация игрока, когда он идет налево
            self.direction = 'left'
            self.rect.x -= self.run
            self.x -= self.run
            if background.get_rgb(self.x, self.y) in self.stena:
                self.rect.x += self.run
                self.x += self.run
            if current_time - self.last_skin_change_time > 150:
                self.last_skin_change_time = current_time
                if self.step == 1:
                    self.step += 1
                    self.back = False
                elif self.step == 2:
                    if self.back:
                        self.step -= 1
                    else:
                        self.step += 1
                elif self.step == 3:
                    self.step -= 1
                    self.back = True
            if self.vis:
                image = load_image(
                    f'players_image/m.c.left_walk_{self.step}.png')
            else:
                image = load_image(
                    f'players_image/m.c.left_walk_{self.step}_trans.png')
        if move_right:  # Анимация игрока, когда он идет направо
            self.direction = 'right'
            self.rect.x += self.run
            self.x += self.run
            if background.get_rgb(self.x, self.y) in self.stena:
                self.rect.x -= self.run
                self.x -= self.run
            if current_time - self.last_skin_change_time > 150:
                self.last_skin_change_time = current_time
                if self.step == 1:
                    self.step += 1
                    self.back = False
                elif self.step == 2:
                    if self.back:
                        self.step -= 1
                    else:
                        self.step += 1
                elif self.step == 3:
                    self.step -= 1
                    self.back = True
            if self.vis:
                image = load_image(
                    f'players_image/m.c.right_walk_{self.step}.png')
            else:
                image = load_image(
                    f'players_image/m.c.right_walk_{self.step}_trans.png')
        if move_up:  # Анимация игрока, когда он идет вверх
            self.direction = 'up'
            self.rect.y -= self.run
            self.y -= self.run
            if background.get_rgb(self.x, self.y) in self.stena:
                self.rect.y += self.run
                self.y += self.run
            if current_time - self.last_skin_change_time > 150:
                self.last_skin_change_time = current_time
                if self.step == 1:
                    self.step += 1
                    self.back = False
                elif self.step == 2:
                    if self.back:
                        self.step -= 1
                    else:
                        self.step += 1
                elif self.step == 3:
                    self.step -= 1
                    self.back = True
            if self.vis:
                image = load_image(
                    f'players_image/m.c.back_walk_{self.step}.png')
            else:
                image = load_image(
                    f'players_image/m.c.back_walk_{self.step}_trans.png')
        if move_down:  # Анимация игрока, когда он идет вниз
            self.direction = 'down'
            self.rect.y += self.run
            self.y += self.run
            if background.get_rgb(self.x, self.y) in self.stena:
                self.rect.y -= self.run
                self.y -= self.run
            if current_time - self.last_skin_change_time > 150:
                self.last_skin_change_time = current_time
                if self.step == 1:
                    self.step += 1
                    self.back = False
                elif self.step == 2:
                    if self.back:
                        self.step -= 1
                    else:
                        self.step += 1
                elif self.step == 3:
                    self.step -= 1
                    self.back = True
            if self.vis:
                image = load_image(
                    f'players_image/m.c.front_walk_{self.step}.png')
            else:
                image = load_image(
                    f'players_image/m.c.front_walk_{self.step}_trans.png')
        self.image = pygame.transform.scale(image, (40, 60))


# Создание объектов всей игры
clock = pygame.time.Clock()
FPS = 60

# группы спрайтов
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
background_group = pygame.sprite.Group()
camera_group = pygame.sprite.Group()

player = Player(800, 500, 1)
camera = Camera()
background = Background('maps/map_1.png', (1667, 1000))

if __name__ == '__main__':  # Запуск программы
    pygame.init()
    pygame.display.set_caption('Clash of tatar')
    size = width, height = 800, 500
    screen = pygame.display.set_mode(size)
    start_screen()

    i = 0
    running = True
    while running:  # Основной цикл
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pass
                if event.key == pygame.K_e:
                    pass
            if event.type == pygame.KEYUP:
                player.stop()

        keys = pygame.key.get_pressed()

        # Обновление игровых объектов
        player.update(
            keys[pygame.K_UP] or keys[pygame.K_w],
            keys[pygame.K_DOWN] or keys[pygame.K_s],
            keys[pygame.K_LEFT] or keys[pygame.K_a],
            keys[pygame.K_RIGHT] or keys[pygame.K_d]
        )
        player.update(False, False, False, False)

        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)
        camera.update(player)

        background_group.draw(screen)
        player_group.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)
