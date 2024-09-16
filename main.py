import datetime
import os
import random
import sys

import pygame
import sqlite3


def load_image(name, color_key=None):  # Загрузка картинки из data
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


def start_screen():  # Начальное окно
    fon = pygame.transform.scale(load_image('camera-player/fon.png'),
                                 (800, 500))
    screen.blit(fon, (0, 0))
    pygame.display.flip()
    clock.tick(0.7)
    screen.fill((0, 0, 0))


class Background(pygame.sprite.Sprite):  # Задний фон
    def __init__(self, image_path, size_fon):
        super().__init__(all_sprites, background_group)
        self.image = load_image(image_path)
        self.image = pygame.transform.scale(self.image, size_fon)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_threshold(self.image, (237, 28, 36), (1, 1, 1, 255))

    def get_rgb(self, x, y):  # Возвращение цвета о пикселе фона
        pixel = pygame.PixelArray(self.image)
        return self.image.unmap_rgb(pixel[x][y])


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

    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, player_group)
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
        self.run = 5
        self.vis = True

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

        stena = []
        if location == 1:
            stena = [(34, 177, 76), (0, 162, 232), (54, 19, 11),
                     (0, 8, 4), (4, 28, 16), (15, 69, 10), (18, 89, 22)]
        elif location == 2:
            stena = [(2, 0, 0)]
        elif location == 3:
            stena = [(153, 217, 234), (185, 122, 87), (0, 162, 232),
                     (187, 122, 87), (0, 187, 255), (55, 71, 79),
                     (38, 52, 58), (71, 92, 102)]

        if move_left:  # Анимация игрока, когда он идет налево
            self.direction = 'left'
            self.rect.x -= self.run
            self.x -= self.run
            if background.get_rgb(self.x, self.y) in stena:
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
            if background.get_rgb(self.x, self.y) in stena:
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
            if background.get_rgb(self.x, self.y) in stena:
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
            if background.get_rgb(self.x, self.y) in stena:
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


class Syuyumbike(pygame.sprite.Sprite):  # Сююмбике
    def __init__(self, pos_x, pos_y, lvl):
        super().__init__(all_sprites, object_group)
        image = load_image(f'objects/syuyumbike/lvl_{lvl}.png')
        self.image = pygame.transform.scale(image, (50, 100))
        self.rect = self.image.get_rect().move(pos_x, pos_y)

        self.pos_x = pos_x
        self.pos_y = pos_y
        self.lvl = lvl
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, lvl):
        image = load_image(f'objects/syuyumbike/lvl_{lvl}.png')
        self.image = pygame.transform.scale(image, (50, 100))
        self.lvl = lvl


class Npc(pygame.sprite.Sprite):  # Нпс
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, object_group)
        image = load_image(f'npc/traveler.jpg')
        self.image = pygame.transform.scale(image, (60, 100))
        self.rect = self.image.get_rect().move(pos_x, pos_y)

        self.mask = pygame.mask.from_surface(self.image)


class NpcText(pygame.sprite.Sprite):  # Нпс
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, object_group)
        self.first_image = load_image(f'npc/traveler_text.jpg')
        self.image = pygame.transform.scale(self.first_image, (0, 0))
        self.rect = self.image.get_rect().move(pos_x, pos_y)

        self.mask = pygame.mask.from_surface(self.image)

    def update(self, is_text):
        if is_text:
            self.image = pygame.transform.scale(self.first_image, (100, 50))
        else:
            self.image = pygame.transform.scale(self.first_image, (0, 0))


def terminate():
    pygame.quit()
    sys.exit()


def start_mini_game():
    global background, player, money
    player.kill()
    background = Background('maps/map_3.png', (900, 500))
    player = Player(400, 300)
    text_index = 0
    win_text = 1
    run_game = True

    while run_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    if win_text == 1:
                        add_experience(1)
                        money += 2
                    else:
                        print("Lose")
                    run_game = False
                if event.key == pygame.K_2:
                    if win_text == 2:
                        add_experience(1)
                        money += 2
                    else:
                        print("Lose")
                    run_game = False
                if event.key == pygame.K_3:
                    if win_text == 3:
                        add_experience(1)
                        money += 2
                    else:
                        print("Lose")
                    run_game = False

        fraze_1 = 'Переведите слово "Привет" '
        fraze_2 = '1. сәлам'
        fraze_3 = '2. әле'
        fraze_4 = '3. көн'

        font_text = pygame.font.Font(os.path.join("data/fonts", "Visitor Rus.ttf"), 25)

        render_fraze_1 = font_text.render("", False, (0, 0, 0))
        render_fraze_2 = font_text.render("", False, (0, 0, 0))
        render_fraze_3 = font_text.render("", False, (0, 0, 0))
        render_fraze_4 = font_text.render("", False, (0, 0, 0))

        if text_index <= len(fraze_1):
            render_fraze_1 = font_text.render(fraze_1[:text_index], False, (0, 0, 0))

        elif text_index <= len(fraze_1) + len(fraze_2):
            render_fraze_1 = font_text.render(fraze_1, False, (0, 0, 0))
            render_fraze_2 = font_text.render(fraze_2[:text_index - len(fraze_1)], False, (0, 0, 0))

        elif text_index <= len(fraze_1) + len(fraze_2) + len(fraze_3):
            render_fraze_1 = font_text.render(fraze_1, False, (0, 0, 0))
            render_fraze_2 = font_text.render(fraze_2, False, (0, 0, 0))
            render_fraze_3 = font_text.render(fraze_3[:text_index - len(fraze_1) - len(fraze_2)], False, (0, 0, 0))

        elif i <= len(fraze_1) + len(fraze_2) + len(fraze_3) + len(fraze_4):
            render_fraze_1 = font_text.render(fraze_1, False, (0, 0, 0))
            render_fraze_2 = font_text.render(fraze_2, False, (0, 0, 0))
            render_fraze_3 = font_text.render(fraze_3, False, (0, 0, 0))
            render_fraze_4 = font_text.render(fraze_4[:text_index - len(fraze_1) - len(fraze_2) - len(fraze_3)], False,
                                              (0, 0, 0))
        text_index += 1

        background_group.draw(screen)
        player_group.draw(screen)

        screen.blit(render_fraze_1, (260, 85))
        screen.blit(render_fraze_2, (260, 115))
        screen.blit(render_fraze_3, (260, 145))
        screen.blit(render_fraze_4, (260, 175))

        pygame.display.flip()
        clock.tick(15)

    start_first_location()


def delete_all():  # Удаление всех объектов
    global npc, npc_text, player, camera, background, syuyumbike, door_1, door_2, door_text_1, door_text_2
    player.kill()
    npc.kill()
    npc_text.kill()
    background.kill()
    syuyumbike.kill()
    door_1.kill()
    door_2.kill()
    door_text_1.kill()
    door_text_2.kill()


def start_first_location():  # Создание первой локации
    global npc, npc_text, player, camera, background, syuyumbike, door_1, door_2, door_text_1, door_text_2
    delete_all()

    npc = Npc(800, 170)
    npc_text = NpcText(800, 110)
    player = Player(800, 500)
    camera = Camera()
    background = Background('maps/map_1.png', (1667, 1000))
    syuyumbike = Syuyumbike(1100, 500, 1)
    door_1 = Door(400, 270, 1)
    door_2 = Door(400, 570, 3)
    door_text_1 = DoorText(400, 210, 2)
    door_text_2 = DoorText(400, 510, 2)


def start_two_location():  # Создание второй локации
    global npc, npc_text, player, camera, background, syuyumbike
    delete_all()

    npc = Npc(800, 170)
    npc_text = NpcText(800, 110)
    player = Player(800, 500)
    camera = Camera()
    background = Background('maps/map_2.png', (1667, 1000))
    syuyumbike = Syuyumbike(1100, 500, syuyumbike.lvl)


def start_three_location():  # Создание третей локации
    global npc, npc_text, player, camera, background, syuyumbike
    delete_all()

    npc = Npc(800, 170)
    npc_text = NpcText(800, 110)
    player = Player(800, 500)
    camera = Camera()
    background = Background('maps/map_4.png', (1667, 1000))
    syuyumbike = Syuyumbike(1100, 500, syuyumbike.lvl)


def add_experience(count):
    global experience, experience_index
    experience += count
    if experiences[experience_index] <= experience:
        experience -= experiences[experience_index]
        experience_index += 1
        syuyumbike.update(syuyumbike.lvl + 1)


class Door(pygame.sprite.Sprite):  # Нпс
    def __init__(self, pos_x, pos_y, image):
        super().__init__(all_sprites, object_group)
        image = load_image(f'doors/door_{image}.png')
        self.image = pygame.transform.scale(image, (80, 100))
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, image):
        self.image = pygame.transform.scale(load_image(f'doors/door_{image}.png'), (80, 100))


class DoorText(pygame.sprite.Sprite):  # Нпс
    def __init__(self, pos_x, pos_y, tip_text):
        super().__init__(all_sprites, object_group)
        self.first_image = load_image(f'doors/door_text_{tip_text}.jpg')
        self.image = pygame.transform.scale(self.first_image, (0, 0))
        self.rect = self.image.get_rect().move(pos_x, pos_y)

        self.mask = pygame.mask.from_surface(self.image)

    def update(self, is_text):
        if is_text:
            self.image = pygame.transform.scale(self.first_image, (100, 50))
        else:
            self.image = pygame.transform.scale(self.first_image, (0, 0))


# Создание объектов всей игры
clock = pygame.time.Clock()
FPS = 60

# Создание групп спрайтов
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
background_group = pygame.sprite.Group()
camera_group = pygame.sprite.Group()
object_group = pygame.sprite.Group()

# Опыт
experience = 0
experience_index = 0
experiences = [5, 30, 50, 100, 250]

# Монеты
money = 0

# Локация
location = 1

# Создание объектов
npc = Npc(800, 170)
npc_text = NpcText(800, 110)
player = Player(800, 500)
camera = Camera()
background = Background('maps/map_1.png', (1667, 1000))
syuyumbike = Syuyumbike(1100, 500, 1)
door_1 = Door(400, 270, 1)
door_2 = Door(400, 570, 3)
door_text_1 = DoorText(400, 210, 2)
door_text_2 = DoorText(400, 510, 2)

if __name__ == '__main__':  # Запуск программы
    pygame.init()
    pygame.display.set_caption('Tatarlango')
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
                if event.key == pygame.K_e:
                    if pygame.sprite.collide_mask(player, npc):
                        start_mini_game()
                    if pygame.sprite.collide_mask(player, door_1):
                        location = 2
                        start_two_location()
                    if pygame.sprite.collide_mask(player, door_2):
                        print(2)
            if event.type == pygame.KEYUP:
                player.stop()

        if player.loc == 1:
            screen.fill((34, 177, 76))
        elif player.loc == 2:
            screen.fill((2, 0, 0))
        elif player.loc == 3:
            screen.fill((153, 217, 234))

        keys = pygame.key.get_pressed()

        # Обновление игровых объектов
        player.update(
            keys[pygame.K_UP] or keys[pygame.K_w],
            keys[pygame.K_DOWN] or keys[pygame.K_s],
            keys[pygame.K_LEFT] or keys[pygame.K_a],
            keys[pygame.K_RIGHT] or keys[pygame.K_d]
        )
        player.update(False, False, False, False)

        npc_text.update(pygame.sprite.collide_mask(player, npc))
        door_text_1.update(pygame.sprite.collide_mask(player, door_1))
        door_text_2.update(pygame.sprite.collide_mask(player, door_2))

        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)
        camera.update(player)

        background_group.draw(screen)
        object_group.draw(screen)
        player_group.draw(screen)

        font = pygame.font.Font(os.path.join("data/fonts", "Visitor Rus.ttf"), 30)
        experience_text = font.render(f' experience: {experience} / {experiences[experience_index]}',
                                      False, (0, 0, 255))
        money_text = font.render(f' money: {money}', False, (255, 255, 0))
        screen.blit(experience_text, (0, 0))
        screen.blit(money_text, (0, 30))

        pygame.display.flip()
        clock.tick(FPS)
