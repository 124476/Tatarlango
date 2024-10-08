import os
import sys

import pygame
from random import shuffle, randint
import pickle


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
    image = load_image('players/m.c.front_stop.png')
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
                image = load_image('players/m.c.left_stop.png')
            elif self.direction == 'right':
                image = load_image('players/m.c.right_stop.png')
            elif self.direction == 'down':
                image = load_image('players/m.c.front_stop.png')
            elif self.direction == 'up':
                image = load_image('players/m.c.back_stop.png')
        else:
            if self.direction == 'left':
                image = load_image('players/m.c.left_stop_trans.png')
            elif self.direction == 'right':
                image = load_image('players/m.c.right_stop_trans.png')
            elif self.direction == 'down':
                image = load_image('players/m.c.front_stop_trans.png')
            elif self.direction == 'up':
                image = load_image('players/m.c.back_stop_trans.png')
        self.image = pygame.transform.scale(image, (40, 60))

    def update(self, move_up, move_down, move_left, move_right):
        global all_sprites, player, background
        image = self.image
        current_time = pygame.time.get_ticks()

        stena = []
        if location == 1:
            stena = [(110, 71, 20), (70, 43, 7), (21, 97, 21), (2, 0, 0)]
        elif location == 2:
            stena = [(2, 0, 0)]
        elif location == 3:
            stena = [(148, 222, 237), (0, 0, 0), (44, 27, 4), (141, 109, 69), (237, 191, 132)]
        elif location == 4:
            stena = [(255, 215, 0), (176, 230, 242)]

        if move_left:  # Анимация игрока, когда он идет налево
            self.direction = 'left'
            self.rect.x -= self.run
            self.x -= self.run

            if background.get_rgb(self.x, self.y) in stena:
                self.rect.x += self.run
                self.x += self.run

            for obstacle in obstacles_group:
                if pygame.sprite.collide_mask(player, obstacle) and obstacle.weight_flag and \
                        player.x > obstacle.x + obstacle.weight_pos - obstacle.weight and \
                        (player.y > obstacle.y > player.y - obstacle.height_pos_down
                         or obstacle.y - obstacle.height_pos < player.y < obstacle.y):
                    self.rect.x += self.run
                    self.x += self.run
                    break

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
                    f'players/m.c.left_walk_{self.step}.png')
            else:
                image = load_image(
                    f'players/m.c.left_walk_{self.step}_trans.png')
        if move_right:  # Анимация игрока, когда он идет направо
            self.direction = 'right'
            self.rect.x += self.run
            self.x += self.run

            if background.get_rgb(self.x, self.y) in stena:
                self.rect.x -= self.run
                self.x -= self.run

            for obstacle in obstacles_group:
                if pygame.sprite.collide_mask(player, obstacle) and obstacle.weight_flag \
                        and player.x > obstacle.x + obstacle.weight_pos and \
                        (player.y > obstacle.y > player.y - obstacle.height_pos_down
                         or obstacle.y - obstacle.height_pos < player.y < obstacle.y):
                    self.rect.x -= self.run
                    self.x -= self.run
                    break

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
                    f'players/m.c.right_walk_{self.step}.png')
            else:
                image = load_image(
                    f'players/m.c.right_walk_{self.step}_trans.png')
        if move_up:  # Анимация игрока, когда он идет вверх
            self.direction = 'up'
            self.rect.y -= self.run
            self.y -= self.run

            if background.get_rgb(self.x, self.y) in stena:
                self.rect.y += self.run
                self.y += self.run

            for obstacle in obstacles_group:
                if pygame.sprite.collide_mask(player, obstacle) \
                        and player.y > obstacle.y > player.y - obstacle.height_pos_down:
                    self.rect.y += self.run
                    self.y += self.run
                    break

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
                    f'players/m.c.back_walk_{self.step}.png')
            else:
                image = load_image(
                    f'players/m.c.back_walk_{self.step}_trans.png')
        if move_down:  # Анимация игрока, когда он идет вниз
            self.direction = 'down'
            self.rect.y += self.run
            self.y += self.run

            if background.get_rgb(self.x, self.y) in stena:
                self.rect.y -= self.run
                self.y -= self.run

            for obstacle in obstacles_group:
                if pygame.sprite.collide_mask(player,
                                              obstacle) and obstacle.y - obstacle.height_pos < player.y < obstacle.y:
                    self.rect.y -= self.run
                    self.y -= self.run
                    break

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
                    f'players/m.c.front_walk_{self.step}.png')
            else:
                image = load_image(
                    f'players/m.c.front_walk_{self.step}_trans.png')
        self.image = pygame.transform.scale(image, (40, 60))


class Syuyumbike(pygame.sprite.Sprite):  # Сююмбике
    def __init__(self, pos_x, pos_y, lvl):
        super().__init__(all_sprites, obstacles_group)
        image = load_image(f'objects/syuyumbike/lvl_{lvl}.png')
        self.image = pygame.transform.scale(image, (144, 451))
        self.rect = self.image.get_rect().move(pos_x, pos_y)

        self.x = pos_x
        self.y = pos_y + 451
        self.lvl = lvl
        self.height = 451
        self.height_pos = 10
        self.height_pos_down = 30
        self.weight = 0
        self.weight_pos = 0
        self.weight_flag = False
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, lvl):
        image = load_image(f'objects/syuyumbike/lvl_{lvl}.png')
        self.image = pygame.transform.scale(image, (50, 100))
        self.lvl = lvl


class Npc(pygame.sprite.Sprite):  # Нпс
    def __init__(self, pos_x, pos_y, lvl_game):
        super().__init__(all_sprites, obstacles_group)
        image = load_image(f'npc/npc_{lvl_game}.png')
        if lvl_game == 1:
            self.image = pygame.transform.scale(image, (48, 100))
            self.height = 100
            self.y = pos_y + 100
        elif lvl_game == 2:
            self.image = pygame.transform.scale(image, (50, 100))
            self.height = 100
            self.y = pos_y + 100
        elif lvl_game == 3:
            self.image = pygame.transform.scale(image, (48, 100))
            self.height = 100
            self.y = pos_y + 100
        elif lvl_game == 4:
            self.image = pygame.transform.scale(image, (50, 100))
            self.height = 100
            self.y = pos_y + 100
        elif lvl_game == 5:
            self.image = pygame.transform.scale(image, (48, 100))
            self.height = 100
            self.y = pos_y + 100
        elif lvl_game == 6:
            self.image = pygame.transform.scale(image, (48, 100))
            self.height = 100
            self.y = pos_y + 100
        else:
            self.image = pygame.transform.scale(image, (50, 100))
            self.height = 100
            self.y = pos_y + 100
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.lvl_game = lvl_game
        self.mask = pygame.mask.from_surface(self.image)

        self.x = pos_x
        self.y = pos_y + self.height
        self.height_pos = 10
        self.height_pos_down = 10
        self.weight = 0
        self.weight_pos = 0
        self.weight_flag = False


class NpcText(pygame.sprite.Sprite):  # Тест нпс
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, object_group)
        self.first_image = load_image(f'npc/npc_text.jpg')
        self.image = pygame.transform.scale(self.first_image, (0, 0))
        self.rect = self.image.get_rect().move(pos_x, pos_y)

        self.mask = pygame.mask.from_surface(self.image)

    def update(self, is_text):
        if is_text:
            self.image = pygame.transform.scale(self.first_image, (100, 50))
        else:
            self.image = pygame.transform.scale(self.first_image, (0, 0))


class Statue(pygame.sprite.Sprite):  # Статуя
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, obstacles_group)
        image = load_image(f'objects/statue/statue.png')
        self.image = pygame.transform.scale(image, (128, 236))
        self.height = 236
        self.y = pos_y + 236
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.mask = pygame.mask.from_surface(self.image)

        self.x = pos_x
        self.y = pos_y + self.height
        self.height_pos = 10
        self.height_pos_down = 10
        self.weight = 0
        self.weight_pos = 0
        self.weight_flag = False


class StatueText(pygame.sprite.Sprite):  # Тест статуи
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, object_group)
        self.first_image = load_image(f'objects/statue/statue_text.jpg')
        self.image = pygame.transform.scale(self.first_image, (0, 0))
        self.rect = self.image.get_rect().move(pos_x, pos_y)

        self.mask = pygame.mask.from_surface(self.image)

    def update(self, is_text):
        if is_text:
            self.image = pygame.transform.scale(self.first_image, (100, 50))
        else:
            self.image = pygame.transform.scale(self.first_image, (0, 0))


class Firework(pygame.sprite.Sprite):  # Фейерверк
    def __init__(self, pos_x, pos_y, index_firework):
        super().__init__(all_sprites, firework_group)
        image = load_image(f'objects/firework/firework_1.png')
        self.image = pygame.transform.scale(image, (200, 210))
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.mask = pygame.mask.from_surface(self.image)
        self.index_firework = index_firework
        self.index = 1
        self.time_replace = 0

    def update(self):
        self.time_replace += 1
        if self.time_replace >= 10:
            self.index = self.index % 14 + 1
            self.time_replace = 0
        image = load_image(f'objects/firework/firework_{self.index}.png')
        self.image = pygame.transform.scale(image, (200, 210))


class Seller(pygame.sprite.Sprite):  # Продавец
    def __init__(self, pos_x, pos_y, lvl_game):
        super().__init__(all_sprites, obstacles_group)
        image = load_image(f'seller/seller.png')
        self.image = pygame.transform.scale(image, (68, 100))
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.lvl_game = lvl_game
        self.mask = pygame.mask.from_surface(self.image)

        self.x = pos_x
        self.y = pos_y + 100
        self.height = 100
        self.height_pos = 10
        self.height_pos_down = 10
        self.weight = 0
        self.weight_pos = 0
        self.weight_flag = False


class SellerText(pygame.sprite.Sprite):  # Текст продавца
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, object_group)
        self.first_image = load_image(f'seller/seller_text.jpg')
        self.image = pygame.transform.scale(self.first_image, (0, 0))
        self.rect = self.image.get_rect().move(pos_x, pos_y)

        self.mask = pygame.mask.from_surface(self.image)

    def update(self, is_text):
        if is_text:
            self.image = pygame.transform.scale(self.first_image, (100, 50))
        else:
            self.image = pygame.transform.scale(self.first_image, (0, 0))


def shop(tip):
    global koef_money, koef_experience, can_lose, money, current_size
    run_game = True

    image = pygame.transform.scale(load_image(f'seller/shop_{tip}.jpg'), (600, 400))

    while run_game:
        for even in pygame.event.get():
            if even.type == pygame.VIDEORESIZE:
                current_size = even.size

            if even.type == pygame.QUIT:
                terminate()
            elif even.type == pygame.KEYDOWN:
                if even.key == pygame.K_p:
                    run_game = False
                if even.key == pygame.K_e:
                    if tip == 1 and koef_money != 6 and improving_vocabulary[1][koef_money - 1] <= money:
                        money -= improving_vocabulary[1][koef_money - 1]
                        koef_money += 1
                    elif tip == 2 and koef_experience != 6 and improving_vocabulary[2][koef_experience - 1] <= money:
                        money -= improving_vocabulary[2][koef_experience - 1]
                        koef_experience += 1
                    elif tip == 3 and can_lose != 6 and improving_vocabulary[3][can_lose - 1] <= money:
                        money -= improving_vocabulary[1][can_lose - 1]
                        can_lose += 1
                    save_game()
        if not run_game:
            break

        if tip == 1:
            bye_text = f"x{koef_money}"
            if koef_money == 6:
                text_money = "Max лвл"
            else:
                text_money = f"{improving_vocabulary[1][koef_money - 1]} монет"
            if improving_vocabulary[1][koef_money - 1] <= money:
                color_money = (0, 255, 0)
            else:
                color_money = (255, 0, 0)
        elif tip == 2:
            bye_text = f"x{koef_experience}"
            if koef_experience == 6:
                text_money = "Max лвл"
            else:
                text_money = f"{improving_vocabulary[2][koef_experience - 1]} монет"
            if improving_vocabulary[2][koef_experience - 1] <= money:
                color_money = (0, 255, 0)
            else:
                color_money = (255, 0, 0)
        elif tip == 3:
            bye_text = f"x{can_lose}"
            if can_lose == 6:
                text_money = "Max лвл"
            else:
                text_money = f"{improving_vocabulary[3][can_lose - 1]} монет"
            if improving_vocabulary[3][can_lose - 1] <= money:
                color_money = (0, 255, 0)
            else:
                color_money = (255, 0, 0)
        else:
            bye_text = ""
            text_money = ""
            color_money = (0, 0, 0)

        if player.loc == 1:
            virtual_screen.fill((34, 177, 76))
        elif player.loc == 2:
            virtual_screen.fill((2, 0, 0))
        elif player.loc == 3:
            virtual_screen.fill((153, 217, 234))

        background_group.draw(virtual_screen)
        object_group.draw(virtual_screen)
        player_group.draw(virtual_screen)

        font_2 = pygame.font.Font(
            os.path.join("data/fonts", "Blazma-Regular.ttf"), 30)
        if experience_index < 6:
            experien_text_2 = f' опыт: {experience} / {experiences[experience_index]}'
        else:
            experien_text_2 = f' макс'
        experience_text_2 = font_2.render(experien_text_2, False, (0, 0, 255))
        money_text_2 = font_2.render(f' монеты: {money}', False, (255, 255, 0))
        virtual_screen.blit(experience_text_2, (0, 0))
        virtual_screen.blit(money_text_2, (0, 30))

        font_text = pygame.font.Font(os.path.join("data/fonts", "Blazma-Regular.ttf"), 50)
        fraze = font_text.render(bye_text, False, (0, 0, 0))

        font_text = pygame.font.Font(os.path.join("data/fonts", "Blazma-Regular.ttf"), 25)
        fraze_2 = font_text.render(f" {text_money}", False, color_money)

        virtual_screen.blit(image, (100, 70))
        virtual_screen.blit(fraze, (350, 250))
        virtual_screen.blit(fraze_2, (325, 350))

        if text_money != "Max":
            fraze_3 = font_text.render(f"E) Прокачать", False, (0, 0, 0))
            virtual_screen.blit(fraze_3, (325, 380))

        scale_surface = pygame.transform.scale(virtual_screen, current_size)
        screen.blit(scale_surface, (0, 0))

        pygame.display.flip()
        clock.tick(35)


def terminate():
    pygame.quit()
    sys.exit()


def start_mini_game(game_lvl):
    global background, player, money, background, current_size

    if location == 1:
        delete_first_location()
    elif location == 2:
        delete_two_location()
    elif location == 3:
        delete_three_location()

    background = Background('maps/map_3.png', (900, 500))
    npc_image = pygame.transform.scale(load_image(f'npc/npc_{game_lvl}.png'), (100, 200))
    player = Player(400, 300)
    text_index = 0
    run_game = True

    quests = [j for j in questions if j['tip'] == str(game_lvl) and int(j['lvl']) <= experience_index + 1]

    quest_index = randint(0, len(quests) - 1)
    start_quest = ['answer_one', 'answer_two', 'answer_three', 'answer_four']
    end_quest = ['answer_one', 'answer_two', 'answer_three', 'answer_four']
    shuffle(end_quest)

    fraze_1 = quests[quest_index]["question"]
    fraze_2 = '1: ' + quests[quest_index][end_quest[start_quest.index('answer_one')]]
    fraze_3 = '2: ' + quests[quest_index][end_quest[start_quest.index('answer_two')]]
    fraze_4 = '3: ' + quests[quest_index][end_quest[start_quest.index('answer_three')]]
    fraze_5 = '4: ' + quests[quest_index][end_quest[start_quest.index('answer_four')]]
    win_text = end_quest.index('answer_one') + 1

    exp = 0
    mon = 0
    if game_lvl == 1 or game_lvl == 2:
        exp = 1
        mon = 2
    elif game_lvl == 3 or game_lvl == 4:
        exp = 1
        mon = 2
    elif game_lvl == 5 or game_lvl == 6:
        exp = 1
        mon = 2

    while run_game:
        for even in pygame.event.get():
            if even.type == pygame.VIDEORESIZE:
                current_size = even.size

            if even.type == pygame.QUIT:
                terminate()
            elif even.type == pygame.KEYDOWN:
                if text_index > len(fraze_1) + len(fraze_2) + len(fraze_3) + len(fraze_4) + len(fraze_5):
                    if even.key == pygame.K_1:
                        if win_text == 1:
                            add_experience(exp)
                            add_money(mon)
                            save_game()
                            next_mini_game(game_lvl)
                        else:
                            end_mini_game(game_lvl)
                        run_game = False
                    if even.key == pygame.K_2:
                        if win_text == 2:
                            add_experience(exp)
                            add_money(mon)
                            save_game()
                            next_mini_game(game_lvl)
                        else:
                            end_mini_game(game_lvl)
                        run_game = False
                    if even.key == pygame.K_3:
                        if win_text == 3:
                            add_experience(exp)
                            add_money(mon)
                            save_game()
                            next_mini_game(game_lvl)
                        else:
                            end_mini_game(game_lvl)
                        run_game = False
                    if even.key == pygame.K_4:
                        if win_text == 4:
                            add_experience(game_lvl // 2 + 1)
                            add_money(game_lvl // 2 + 2)
                            save_game()
                            next_mini_game(game_lvl)
                        else:
                            end_mini_game(game_lvl)
                        run_game = False
        if not run_game:
            break

        font_text = pygame.font.Font(os.path.join("data/fonts", "Blazma-Regular.ttf"), 25)

        if text_index <= len(fraze_1):
            render_fraze_1 = font_text.render(fraze_1[:text_index], False, (0, 0, 0))
            render_fraze_2 = font_text.render("", False, (0, 0, 0))
            render_fraze_3 = font_text.render("", False, (0, 0, 0))
            render_fraze_4 = font_text.render("", False, (0, 0, 0))
            render_fraze_5 = font_text.render("", False, (0, 0, 0))

        elif text_index <= len(fraze_1) + len(fraze_2):
            render_fraze_1 = font_text.render(fraze_1, False, (0, 0, 0))
            render_fraze_2 = font_text.render(fraze_2[:text_index - len(fraze_1)], False, (0, 0, 0))
            render_fraze_3 = font_text.render("", False, (0, 0, 0))
            render_fraze_4 = font_text.render("", False, (0, 0, 0))
            render_fraze_5 = font_text.render("", False, (0, 0, 0))

        elif text_index <= len(fraze_1) + len(fraze_2) + len(fraze_3):
            render_fraze_1 = font_text.render(fraze_1, False, (0, 0, 0))
            render_fraze_2 = font_text.render(fraze_2, False, (0, 0, 0))
            render_fraze_3 = font_text.render(fraze_3[:text_index - len(fraze_1) - len(fraze_2)], False, (0, 0, 0))
            render_fraze_4 = font_text.render("", False, (0, 0, 0))
            render_fraze_5 = font_text.render("", False, (0, 0, 0))

        elif text_index < len(fraze_1) + len(fraze_2) + len(fraze_3) + len(fraze_4):
            render_fraze_1 = font_text.render(fraze_1, False, (0, 0, 0))
            render_fraze_2 = font_text.render(fraze_2, False, (0, 0, 0))
            render_fraze_3 = font_text.render(fraze_3, False, (0, 0, 0))
            render_fraze_4 = font_text.render(fraze_4[:text_index - len(fraze_1) - len(fraze_2) - len(fraze_3)], False,
                                              (0, 0, 0))
            render_fraze_5 = font_text.render("", False, (0, 0, 0))

        elif text_index < len(fraze_1) + len(fraze_2) + len(fraze_3) + len(fraze_4) + len(fraze_5):
            render_fraze_1 = font_text.render(fraze_1, False, (0, 0, 0))
            render_fraze_2 = font_text.render(fraze_2, False, (0, 0, 0))
            render_fraze_3 = font_text.render(fraze_3, False, (0, 0, 0))
            render_fraze_4 = font_text.render(fraze_4, False, (0, 0, 0))
            render_fraze_5 = font_text.render(
                fraze_5[:text_index - len(fraze_1) - len(fraze_2) - len(fraze_3) - len(fraze_4)], False, (0, 0, 0))
        else:
            render_fraze_1 = font_text.render(fraze_1, False, (0, 0, 0))
            render_fraze_2 = font_text.render(fraze_2, False, (0, 0, 0))
            render_fraze_3 = font_text.render(fraze_3, False, (0, 0, 0))
            render_fraze_4 = font_text.render(fraze_4, False, (0, 0, 0))
            render_fraze_5 = font_text.render(fraze_5, False, (0, 0, 0))

        text_index += 1

        background_group.draw(virtual_screen)
        virtual_screen.blit(npc_image, (100, 100))
        player_group.draw(virtual_screen)

        virtual_screen.blit(render_fraze_1, (260, 85))
        virtual_screen.blit(render_fraze_2, (260, 115))
        virtual_screen.blit(render_fraze_3, (260, 145))
        virtual_screen.blit(render_fraze_4, (260, 175))
        virtual_screen.blit(render_fraze_5, (260, 205))

        scale_surface = pygame.transform.scale(virtual_screen, current_size)
        screen.blit(scale_surface, (0, 0))

        pygame.display.flip()
        clock.tick(35)
    start_location()


def next_mini_game(game_lvl):
    global current_size
    fon = os.path.join("data/fonts", "Blazma-Regular.ttf")
    font_text = pygame.font.Font(fon, 50)
    fraze_1 = font_text.render("Правильно", False, (0, 255, 0))
    font_text = pygame.font.Font(fon, 25)
    fraze_2 = font_text.render("E: Следующий", False, (0, 0, 0))
    fraze_3 = font_text.render("P: Выйти", False, (0, 0, 0))
    npc_image = pygame.transform.scale(load_image(f'npc/npc_{game_lvl}.png'), (100, 200))

    run_game = True

    while run_game:
        for even in pygame.event.get():
            if even.type == pygame.VIDEORESIZE:
                current_size = even.size

            if even.type == pygame.QUIT:
                terminate()
            elif even.type == pygame.KEYDOWN:
                if even.key == pygame.K_e:
                    player.y = 1000000
                    player.kill()
                    background.kill()
                    start_mini_game(game_lvl)
                    run_game = False
                if even.key == pygame.K_p:
                    player.y = 1000000
                    player.kill()
                    background.kill()
                    return
        if not run_game:
            break

        background_group.draw(virtual_screen)
        virtual_screen.blit(npc_image, (100, 100))
        player_group.draw(virtual_screen)

        virtual_screen.blit(fraze_1, (260, 85))
        virtual_screen.blit(fraze_2, (260, 135))
        virtual_screen.blit(fraze_3, (260, 165))

        scale_surface = pygame.transform.scale(virtual_screen, current_size)
        screen.blit(scale_surface, (0, 0))

        pygame.display.flip()
        clock.tick(35)


def end_mini_game(game_lvl):
    global losed, current_size

    npc_image = pygame.transform.scale(load_image(f'npc/npc_{game_lvl}.png'), (100, 200))
    fon = os.path.join("data/fonts", "Blazma-Regular.ttf")
    font_text = pygame.font.Font(fon, 50)
    fraze_1 = font_text.render("Неправильно", False, (255, 0, 0))
    font_text = pygame.font.Font(fon, 25)

    if can_lose > losed:
        fraze_2 = font_text.render("E: Следующий", False, (0, 0, 0))
    else:
        fraze_2 = font_text.render(f"Все попытки потрачены {losed} / {can_lose}", False, (0, 0, 0))
    fraze_3 = font_text.render("P: Выйти", False, (0, 0, 0))

    run_game = True
    while run_game:
        for even in pygame.event.get():
            if even.type == pygame.VIDEORESIZE:
                current_size = even.size

            if even.type == pygame.QUIT:
                terminate()
            elif even.type == pygame.KEYDOWN:
                if even.key == pygame.K_e:
                    if can_lose > losed:
                        losed += 1
                        player.y = 1000000
                        player.kill()
                        background.kill()
                        start_mini_game(game_lvl)
                        run_game = False
                if even.key == pygame.K_p:
                    return
        if not run_game:
            break

        background_group.draw(virtual_screen)
        virtual_screen.blit(npc_image, (100, 100))
        player_group.draw(virtual_screen)

        virtual_screen.blit(fraze_1, (260, 85))
        virtual_screen.blit(fraze_2, (260, 135))
        virtual_screen.blit(fraze_3, (260, 165))

        scale_surface = pygame.transform.scale(virtual_screen, current_size)
        screen.blit(scale_surface, (0, 0))

        pygame.display.flip()
        clock.tick(35)


def delete_first_location():  # Удаление всех объектов первой локации
    global npc, npc_text, npc_2, npc_text_2, player, camera, background, syuyumbike, door_1, door_2, \
        door_5, door_text_1, door_text_2, door_text_5, seller, seller_text, house

    for index_sprite in all_sprites:
        index_sprite.x = -10000000

    pygame.mixer.music.stop()
    player.kill()
    npc.kill()
    npc_text.kill()
    npc_2.kill()
    npc_text_2.kill()
    seller.kill()
    seller_text.kill()
    background.kill()
    syuyumbike.kill()
    door_1.kill()
    door_2.kill()
    door_5.kill()
    door_text_1.kill()
    door_text_2.kill()
    door_text_5.kill()
    house.kill()


def delete_two_location():  # Удаление всех объектов второй локации
    global npc, npc_text, npc_2, npc_text_2, player, camera, background, door_3, door_text_3, seller, seller_text

    for index_sprite in all_sprites:
        index_sprite.x = -10000000

    pygame.mixer.music.stop()
    player.kill()
    npc.kill()
    npc_text.kill()
    npc_2.kill()
    npc_text_2.kill()
    seller.kill()
    seller_text.kill()
    background.kill()
    syuyumbike.kill()
    door_3.kill()
    door_text_3.kill()
    house.kill()


def delete_three_location():  # Удаление всех объектов третей локации
    global npc, npc_text, npc_2, npc_text_2, player, camera, background, door_4, door_text_4, seller, seller_text, tree

    for index_sprite in all_sprites:
        index_sprite.x = -10000000

    pygame.mixer.music.stop()
    player.kill()
    npc.kill()
    npc_text.kill()
    npc_2.kill()
    npc_text_2.kill()
    seller.kill()
    seller_text.kill()
    background.kill()
    syuyumbike.kill()
    door_4.kill()
    door_text_4.kill()
    house.kill()
    tree.kill()


def delete_four_location():  # Удаление всех объектов четвертой локации
    global player, camera, background, syuyumbike, door_6, door_text_6, firework_1, firework_2, statue, statue_text

    for index_sprite in all_sprites:
        index_sprite.x = -10000000

    pygame.mixer.music.stop()
    player.kill()
    background.kill()
    syuyumbike.kill()
    door_6.kill()
    door_text_6.kill()
    statue.kill()
    statue_text.kill()
    firework_1.kill()
    firework_2.kill()


def refresh_groups():
    global all_sprites, player_group, background_group, camera_group, object_group, trees_group, obstacles_group, firework_group

    all_sprites = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    background_group = pygame.sprite.Group()
    camera_group = pygame.sprite.Group()
    object_group = pygame.sprite.Group()
    trees_group = pygame.sprite.Group()
    obstacles_group = pygame.sprite.Group()
    firework_group = pygame.sprite.Group()


def start_first_location():  # Создание первой локации
    global npc, npc_text, npc_2, npc_text_2, player, camera, background, syuyumbike, door_1, door_2, \
        door_5, door_text_1, door_text_2, door_text_5, seller, seller_text, house
    refresh_groups()

    npc = Npc(1740, 230, 1)
    npc_text = NpcText(1740, 160)
    npc_2 = Npc(1910, 230, 2)
    npc_text_2 = NpcText(1910, 160)
    seller = Seller(1770, 920, 1)
    seller_text = SellerText(1770, 850)
    player = Player(2050, 800)
    camera = Camera()
    house = House(1400, 460)
    background = Background('maps/map_1.png', (4500, 1500))
    syuyumbike = Syuyumbike(2100, 210, experience_index + 1)
    door_1 = Door(1551, 625, 1, experience_index >= 2)
    door_2 = Door(1450, 350, 2, experience_index >= 4)
    door_5 = Door(2141, 588, 5, experience_index == 6)
    door_text_1 = DoorText(1551, 550, door_1)
    door_text_2 = DoorText(1450, 280, door_2)
    door_text_5 = DoorText(2141, 510, door_5)


def start_two_location():  # Создание второй локации
    global npc, npc_text, npc_2, npc_text_2, player, camera, background, door_3, door_text_3, seller, seller_text
    refresh_groups()

    npc = Npc(550, 400, 3)
    npc_text = NpcText(550, 330)
    npc_2 = Npc(740, 400, 4)
    npc_text_2 = NpcText(740, 330)
    seller = Seller(290, 640, 2)
    seller_text = SellerText(290, 570)
    player = Player(637, 748)
    camera = Camera()
    background = Background('maps/map_2.png', (1299, 1068))
    door_3 = Door(970, 456, 3, True)
    door_text_3 = DoorText(970, 385, door_3)


def start_three_location():  # Создание третей локации
    global npc, npc_text, npc_2, npc_text_2, player, camera, background, door_4, door_text_4, seller, seller_text, tree
    refresh_groups()

    npc = Npc(1210, 670, 5)
    npc_text = NpcText(1210, 600)
    npc_2 = Npc(1030, 647, 6)
    npc_text_2 = NpcText(1030, 577)
    seller = Seller(400, 1000, 3)
    seller_text = SellerText(400, 930)
    player = Player(680, 750)
    camera = Camera()
    tree = Tree(340, 655)
    background = Background('maps/map_4.png', (1920, 2325))
    door_4 = Door(685, 612, 4, True)
    door_text_4 = DoorText(685, 542, door_4)


def start_four_location():  # Создание пятой локации
    global npc_text_2, player, camera, background, door_6, door_text_6, firework_1, firework_2, statue, statue_text
    refresh_groups()

    pygame.mixer.music.load("data/music/mus_town.ogg")
    pygame.mixer.music.set_volume(10)
    pygame.mixer.music.play(loops=-1)

    player = Player(780, 650)
    camera = Camera()
    background = Background('maps/map_5.png', (1600, 1000))
    door_6 = Door(769, 715, 6, True)
    door_text_6 = DoorText(769, 645, door_6)
    firework_1 = Firework(400, 70, 1)
    firework_2 = Firework(1100, 70, 2)
    statue = Statue(750, 200)
    statue_text = StatueText(750, 130)


def add_experience(count):
    global experience, experience_index
    experience += count * koef_experience
    if experience_index != 6 and experiences[experience_index] <= experience:
        experience -= experiences[experience_index]
        experience_index += 1
        syuyumbike.update(syuyumbike.lvl + 1)


def add_money(count):
    global money
    money += count * koef_money


class Door(pygame.sprite.Sprite):  # Нпс
    def __init__(self, pos_x, pos_y, image, is_open):
        super().__init__(all_sprites, obstacles_group)
        self.tips = image
        image = load_image(f'doors/door_{self.tips}/door_{2 if is_open else 1}.png')
        self.height_pos_down = 10
        if self.tips == 1 or self.tips == 3:
            self.image = pygame.transform.scale(image, (60, 82))
            self.height = 82
            self.y = pos_y + 82
        elif self.tips == 2 or self.tips == 4:
            self.image = pygame.transform.scale(image, (100, 100))
            self.height = 100
            self.y = pos_y + 100
        elif self.tips == 5:
            self.image = pygame.transform.scale(image, (62, 73))
            self.height = 73
            self.y = pos_y + 73
            self.height_pos_down = 10
        elif self.tips == 6:
            self.image = pygame.transform.scale(image, (62, 73))
            self.height = 73
            self.y = pos_y + 50
        else:
            self.image = pygame.transform.scale(image, (80, 100))
            self.height = 100
            self.y = pos_y + 100
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.mask = pygame.mask.from_surface(self.image)
        self.is_open = is_open

        self.x = pos_x
        self.y = pos_y + 100
        self.height_pos = 30
        self.weight = 0
        self.weight_pos = 0
        self.weight_flag = False


class DoorText(pygame.sprite.Sprite):  # Нпс
    def __init__(self, pos_x, pos_y, this_door):
        super().__init__(all_sprites, object_group)
        self.first_image = load_image(f'doors/door_text_{1 if this_door.is_open else 2}.jpg')
        self.image = pygame.transform.scale(self.first_image, (0, 0))
        self.rect = self.image.get_rect().move(pos_x, pos_y)

        self.mask = pygame.mask.from_surface(self.image)

    def update(self, is_text):
        if is_text:
            self.image = pygame.transform.scale(self.first_image, (100, 50))
        else:
            self.image = pygame.transform.scale(self.first_image, (0, 0))


class Tree(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, obstacles_group, trees_group)
        self.image = load_image('objects/tree_of_heaven.png')
        self.image = pygame.transform.scale(self.image, (200, 320))
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.mask = pygame.mask.from_surface(self.image)
        self.x = pos_x
        self.y = pos_y + 320
        self.height = 320
        self.height_pos = 10
        self.weight = 0
        self.weight_pos = 0
        self.height_pos_down = 10
        self.weight_flag = False


class House(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, obstacles_group, trees_group)
        self.image = load_image('objects/house.png')
        self.image = pygame.transform.scale(self.image, (280, 250))
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.mask = pygame.mask.from_surface(self.image)
        self.x = pos_x
        self.y = pos_y + 250
        self.height = 210
        self.height_pos = 100
        self.height_pos_down = 20
        self.weight = 280
        self.weight_pos = 10
        self.weight_flag = True


def save_game():  # Сохранения игры
    state = {
        'koef_experience': koef_experience,
        'koef_money': koef_money,
        'can_lose': can_lose,
        'experience': experience,
        'experience_index': experience_index,
        'money': money
    }

    with open('data/game_player.pkl', 'wb') as f:
        pickle.dump(state, f)


def load_game():  # Загрузка сохраненной игры
    global koef_experience, koef_money, can_lose, experience, experience_index, money, questions
    try:
        with open('data/game_player.pkl', 'rb') as f:
            state = pickle.load(f)
        koef_experience = state['koef_experience']
        koef_money = state['koef_money']
        can_lose = state['can_lose']
        experience = state['experience']
        experience_index = state['experience_index']
        money = state['money']
    except Exception:
        pass

    with open('data/game_db.pkl', 'rb') as f:
        p = pickle.load(f)
        questions = []
        for j in p:
            questions.append({
                'id': bytes(j['id']).decode(),
                'tip': bytes(j['tip']).decode(),
                'lvl': bytes(j['lvl']).decode(),
                'question': bytes(j['question']).decode(),
                'answer_one': bytes(j['answer_one']).decode(),
                'answer_two': bytes(j['answer_two']).decode(),
                'answer_three': bytes(j['answer_three']).decode(),
                'answer_four': bytes(j['answer_four']).decode()
            })


def start_location():
    if location == 1:
        start_first_location()
    elif location == 2:
        start_two_location()
    elif location == 3:
        start_three_location()


def titre_screen():  # Субтитры
    global current_size, current_size
    j = 0
    i = 0
    sybtit = load_image('camera-player/credits.png')

    pygame.mixer.music.load("data/music/final_melody.ogg")
    pygame.mixer.music.set_volume(50)
    pygame.mixer.music.play(loops=-1)

    while True:
        for even in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                current_size = event.size

            if even.type == pygame.QUIT:
                terminate()

        virtual_screen.fill((0, 0, 0))
        virtual_screen.blit(sybtit, (0, -j + 400))

        scale_surface = pygame.transform.scale(virtual_screen, current_size)
        screen.blit(scale_surface, (0, 0))

        pygame.display.flip()

        j += 1.5
        if 2500 < j < 3000:
            # Постепенное уменьшение громкости
            pygame.mixer.music.set_volume(
                0.5 - i * 0.4 / 500)  # Примерное уменьшение до 0.1 за 3000 итераций
            i += 1
        elif j >= 3000:
            pygame.mixer.music.load("data/music/mus_town.ogg")
            pygame.mixer.music.set_volume(10)
            pygame.mixer.music.play(loops=-1)
            return

        clock.tick(FPS)


# Создание объектов всей игры
clock = pygame.time.Clock()
FPS = 60

# Создание групп спрайтов
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
background_group = pygame.sprite.Group()
camera_group = pygame.sprite.Group()
object_group = pygame.sprite.Group()
trees_group = pygame.sprite.Group()
obstacles_group = pygame.sprite.Group()
firework_group = pygame.sprite.Group()

# Опыт
experience = 0
experience_index = 0
experiences = [5, 50, 200, 500, 1000, 1500, 3000]

# Монеты
money = 0

# Локация
location = 1

# Улучшения
koef_experience = 1
koef_money = 1
can_lose = 1
losed = 0

# Словари данных
improving_vocabulary = {
    1: [15, 50, 200, 500, 1500],
    2: [80, 300, 600, 1500, 3000],
    3: [50, 200, 500, 800, 1500]
}
questions = {

}

# Загрузка игры
load_game()

# Создание объектов
npc = Npc(1740, 230, 1)
npc_text = NpcText(1740, 160)
npc_2 = Npc(1910, 230, 2)
npc_text_2 = NpcText(1910, 160)
seller = Seller(1770, 920, 1)
seller_text = SellerText(1770, 850)
statue = Statue(100000, 10000000)
statue_text = StatueText(100000, 10000000)
player = Player(2050, 800)
camera = Camera()
tree = Tree(1500000000, 500000000)
firework_1 = Firework(1500000000, 500000000, 1)
firework_2 = Firework(1500000000, 500000000, 2)
house = House(1400, 460)
background = Background('maps/map_1.png', (4500, 1500))
syuyumbike = Syuyumbike(2100, 210, experience_index + 1)
door_1 = Door(1551, 625, 1, experience_index >= 2)
door_2 = Door(1450, 350, 2, experience_index >= 4)
door_3 = Door(-100000, -100000, 3, False)
door_4 = Door(-100000, -100000, 4, False)
door_5 = Door(2141, 588, 5, experience_index == 6)
door_6 = Door(-100000, -100000, 6, False)
door_text_1 = DoorText(1551, 550, door_1)
door_text_2 = DoorText(1450, 280, door_2)
door_text_3 = DoorText(400, 210, door_3)
door_text_4 = DoorText(400, 510, door_4)
door_text_5 = DoorText(2141, 510, door_5)
door_text_6 = DoorText(400, 510, door_6)

if __name__ == '__main__':  # Запуск программы
    pygame.init()
    pygame.display.set_caption('Tatarlango')
    size = width, height = 800, 500
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)

    virtual_screen = pygame.Surface((width, height))
    current_size = screen.get_size()

    start_screen()

    i = 0
    running = True
    while running:  # Основной цикл
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                current_size = event.size
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    if pygame.sprite.collide_mask(player, npc):
                        losed = 0
                        start_mini_game(npc.lvl_game)
                    if pygame.sprite.collide_mask(player, npc_2):
                        losed = 0
                        start_mini_game(npc_2.lvl_game)
                    if pygame.sprite.collide_mask(player, seller):
                        shop(location)
                    if pygame.sprite.collide_mask(player, statue):
                        titre_screen()

                    if location == 1 and pygame.sprite.collide_mask(player, door_1) and door_1.is_open:
                        location = 2
                        delete_first_location()
                        start_two_location()
                    if location == 1 and pygame.sprite.collide_mask(player, door_2) and door_2.is_open:
                        location = 3
                        delete_first_location()
                        start_three_location()
                    if location == 2 and pygame.sprite.collide_mask(player, door_3) and door_3.is_open:
                        location = 1
                        delete_two_location()
                        start_first_location()
                    if location == 3 and pygame.sprite.collide_mask(player, door_4) and door_4.is_open:
                        location = 1
                        delete_three_location()
                        start_first_location()
                    if location == 1 and pygame.sprite.collide_mask(player, door_5) and door_5.is_open:
                        location = 4
                        delete_first_location()
                        start_four_location()
                    if location == 4 and pygame.sprite.collide_mask(player, door_6) and door_6.is_open:
                        location = 1
                        delete_four_location()
                        start_first_location()
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
        npc_text_2.update(pygame.sprite.collide_mask(player, npc_2))
        seller_text.update(pygame.sprite.collide_mask(player, seller))
        statue_text.update(pygame.sprite.collide_mask(player, statue))
        door_text_1.update(pygame.sprite.collide_mask(player, door_1))
        door_text_2.update(pygame.sprite.collide_mask(player, door_2))
        door_text_3.update(pygame.sprite.collide_mask(player, door_3))
        door_text_4.update(pygame.sprite.collide_mask(player, door_4))
        door_text_5.update(pygame.sprite.collide_mask(player, door_5))
        door_text_6.update(pygame.sprite.collide_mask(player, door_6))

        # Обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)
        camera.update(player)

        firework_group.update()
        obstacles_up_group = pygame.sprite.Group()
        obstacles_down_group = pygame.sprite.Group()

        for i in obstacles_group:
            if i.y < player.y:
                obstacles_up_group.add(i)
            else:
                obstacles_down_group.add(i)

        if location == 1:
            virtual_screen.fill((21, 97, 21))
        elif location == 2:
            virtual_screen.fill((0, 0, 0))
        elif location == 3:
            virtual_screen.fill((148, 222, 237))
        elif location == 4:
            virtual_screen.fill((176, 230, 242))
        else:
            virtual_screen.fill((2, 0, 0))

        background_group.draw(virtual_screen)
        obstacles_up_group.draw(virtual_screen)
        player_group.draw(virtual_screen)
        obstacles_down_group.draw(virtual_screen)
        object_group.draw(virtual_screen)
        firework_group.draw(virtual_screen)

        font = pygame.font.Font(os.path.join("data/fonts", "Blazma-Regular.ttf"), 30)
        if experience_index < 6:
            experien_text = f' опыт: {experience} / {experiences[experience_index]}'
        else:
            experien_text = f' макс'
        experience_text = font.render(experien_text, False, (0, 0, 255))
        money_text = font.render(f' монеты: {money}', False, (255, 255, 0))
        virtual_screen.blit(experience_text, (0, 0))
        virtual_screen.blit(money_text, (0, 30))

        scaled_surface = pygame.transform.scale(virtual_screen, current_size)
        screen.blit(scaled_surface, (0, 0))

        pygame.display.flip()
        clock.tick(FPS)
