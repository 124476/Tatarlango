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
            stena = [(2, 0, 0)]

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
                        (player.y > obstacle.y > player.y - 10
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
                        and player.x > obstacle.x + obstacle.weight_pos and (player.y > obstacle.y > player.y - 10
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
                if pygame.sprite.collide_mask(player, obstacle) and player.y > obstacle.y > player.y - 10:
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
        self.height = 100
        self.image = pygame.transform.scale(image, (60, self.height))
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.lvl_game = lvl_game
        self.mask = pygame.mask.from_surface(self.image)

        self.x = pos_x
        self.y = pos_y + self.height
        self.height_pos = 10
        self.weight = 0
        self.weight_pos = 0
        self.weight_flag = False


class NpcText(pygame.sprite.Sprite):  # Тест нпс
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


class Seller(pygame.sprite.Sprite):  # Продавец
    def __init__(self, pos_x, pos_y, lvl_game):
        super().__init__(all_sprites, obstacles_group)
        image = load_image(f'seller/seller.jpg')
        self.image = pygame.transform.scale(image, (60, 100))
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.lvl_game = lvl_game
        self.mask = pygame.mask.from_surface(self.image)

        self.x = pos_x
        self.y = pos_y + 100
        self.height = 100
        self.height_pos = 10
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
    global koef_money, koef_experience, can_lose, money
    run_game = True

    image = pygame.transform.scale(load_image(f'npc/seller/shop_{tip}.jpg'), (600, 400))

    while run_game:
        for even in pygame.event.get():
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

        background_group.draw(screen)
        object_group.draw(screen)
        player_group.draw(screen)

        font_2 = pygame.font.Font(os.path.join("data/fonts", "Blazma-Regular.ttf"), 30)
        experience_text_2 = font_2.render(f' experience: {experience} / {experiences[experience_index]}',
                                          False, (0, 0, 255))
        money_text_2 = font_2.render(f' money: {money}', False, (255, 255, 0))
        screen.blit(experience_text_2, (0, 0))
        screen.blit(money_text_2, (0, 30))

        font_text = pygame.font.Font(os.path.join("data/fonts", "Blazma-Regular.ttf"), 50)
        fraze = font_text.render(bye_text, False, (0, 0, 0))

        font_text = pygame.font.Font(os.path.join("data/fonts", "Blazma-Regular.ttf"), 25)
        fraze_2 = font_text.render(f" {text_money}", False, color_money)

        screen.blit(image, (100, 70))
        screen.blit(fraze, (350, 250))
        screen.blit(fraze_2, (325, 350))

        if text_money != "Max":
            fraze_3 = font_text.render(f"E) Прокачать", False, (0, 0, 0))
            screen.blit(fraze_3, (325, 380))

        pygame.display.flip()
        clock.tick(35)


def terminate():
    pygame.quit()
    sys.exit()


def start_mini_game(game_lvl):
    global background, player, money, background
    delete_all()

    background = Background('maps/map_3.png', (900, 500))
    player = Player(400, 300)
    text_index = 0
    run_game = True

    quests = [j for j in questions if j['tip'] == str(game_lvl)]

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

    while run_game:
        for even in pygame.event.get():
            if even.type == pygame.QUIT:
                terminate()
            elif even.type == pygame.KEYDOWN:
                if text_index > len(fraze_1) + len(fraze_2) + len(fraze_3) + len(fraze_4) + len(fraze_5):
                    if even.key == pygame.K_1:
                        if win_text == 1:
                            add_experience(game_lvl // 2 + 1)
                            add_money(game_lvl // 2 + 2)
                            save_game()
                            next_mini_game(game_lvl)
                        else:
                            end_mini_game(game_lvl)
                        run_game = False
                    if even.key == pygame.K_2:
                        if win_text == 2:
                            add_experience(game_lvl // 2 + 1)
                            add_money(game_lvl // 2 + 2)
                            save_game()
                            next_mini_game(game_lvl)
                        else:
                            end_mini_game(game_lvl)
                        run_game = False
                    if even.key == pygame.K_3:
                        if win_text == 3:
                            add_experience(game_lvl // 2 + 1)
                            add_money(game_lvl // 2 + 2)
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

        background_group.draw(screen)
        player_group.draw(screen)

        screen.blit(render_fraze_1, (260, 85))
        screen.blit(render_fraze_2, (260, 115))
        screen.blit(render_fraze_3, (260, 145))
        screen.blit(render_fraze_4, (260, 175))
        screen.blit(render_fraze_5, (260, 205))

        pygame.display.flip()
        clock.tick(35)
    start_location()


def next_mini_game(game_lvl):
    fon = os.path.join("data/fonts", "Blazma-Regular.ttf")
    font_text = pygame.font.Font(fon, 50)
    fraze_1 = font_text.render("Правильно", False, (0, 255, 0))
    font_text = pygame.font.Font(fon, 25)
    fraze_2 = font_text.render("E: Следующий", False, (0, 0, 0))
    fraze_3 = font_text.render("P: Выйти", False, (0, 0, 0))

    run_game = True
    while run_game:
        for even in pygame.event.get():
            if even.type == pygame.QUIT:
                terminate()
            elif even.type == pygame.KEYDOWN:
                if even.key == pygame.K_e:
                    start_mini_game(game_lvl)
                    run_game = False
                if even.key == pygame.K_p:
                    return
        if not run_game:
            break

        background_group.draw(screen)
        player_group.draw(screen)

        screen.blit(fraze_1, (260, 85))
        screen.blit(fraze_2, (260, 135))
        screen.blit(fraze_3, (260, 165))

        pygame.display.flip()
        clock.tick(35)


def end_mini_game(game_lvl):
    global losed
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
            if even.type == pygame.QUIT:
                terminate()
            elif even.type == pygame.KEYDOWN:
                if even.key == pygame.K_e:
                    if can_lose > losed:
                        losed += 1
                        start_mini_game(game_lvl)
                        run_game = False
                if even.key == pygame.K_p:
                    return
        if not run_game:
            break

        background_group.draw(screen)
        player_group.draw(screen)

        screen.blit(fraze_1, (260, 85))
        screen.blit(fraze_2, (260, 135))
        screen.blit(fraze_3, (260, 165))

        pygame.display.flip()
        clock.tick(35)


def delete_all():  # Удаление всех объектов
    global npc, npc_text, npc_2, npc_text_2, player, camera, background, syuyumbike, door_1, door_2, door_text_1, \
        door_text_2, door_3, door_text_4, door_3, door_text_4, seller, seller_text, door_5, door_6, door_text_5, \
        door_text_6

    for index_sprite in all_sprites:
        index_sprite.x = -10000000

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
    door_3.kill()
    door_4.kill()
    door_5.kill()
    door_6.kill()
    door_text_1.kill()
    door_text_2.kill()
    door_text_3.kill()
    door_text_4.kill()
    door_text_5.kill()
    door_text_6.kill()
    house.kill()
    tree.kill()


def start_first_location():  # Создание первой локации
    global npc, npc_text, npc_2, npc_text_2, player, camera, background, syuyumbike, door_1, door_2, door_3, door_4, \
        door_5, door_6, door_text_1, door_text_2, door_text_3, door_text_4, door_text_5, door_text_6, \
        seller, seller_text, tree, house
    delete_all()

    npc = Npc(1100, 170, 1)
    npc_text = NpcText(1100, 110)
    npc_2 = Npc(1300, 170, 2)
    npc_text_2 = NpcText(1300, 110)
    seller = Seller(1500, 170, 1)
    seller_text = SellerText(1500, 110)
    player = Player(1300, 800)
    camera = Camera()
    tree = Tree(-15000, -1000000)
    house = House(1100, 460)
    background = Background('maps/map_1.png', (3000, 1500))
    syuyumbike = Syuyumbike(1670, 210, experience_index + 1)
    door_1 = Door(1240, 610, 1, experience_index >= 2)
    door_2 = Door(1500, 700, 2, experience_index >= 4)
    door_3 = Door(-100000, -100000, 3, False)
    door_4 = Door(-100000, -100000, 4, False)
    door_5 = Door(1700, 560, 5, experience_index == 6)
    door_6 = Door(-100000, -100000, 6, False)
    door_text_1 = DoorText(1240, 540, door_1)
    door_text_2 = DoorText(1500, 630, door_2)
    door_text_3 = DoorText(400, 210, door_3)
    door_text_4 = DoorText(400, 510, door_4)
    door_text_5 = DoorText(1700, 490, door_5)
    door_text_6 = DoorText(400, 510, door_6)


def start_two_location():  # Создание второй локации
    global npc, npc_text, npc_2, npc_text_2, player, camera, background, door_1, door_2, door_3, door_4, door_5, door_6, \
        door_text_1, door_text_2, door_text_3, door_text_4, door_text_5, door_text_6, seller, seller_text
    delete_all()

    npc = Npc(800, 170, 3)
    npc_text = NpcText(800, 110)
    npc_2 = Npc(1000, 170, 4)
    npc_text_2 = NpcText(1000, 110)
    seller = Seller(1200, 170, 2)
    seller_text = SellerText(1200, 110)
    player = Player(800, 500)
    camera = Camera()
    background = Background('maps/map_2.png', (1299, 1068))
    door_1 = Door(-100000, -100000, 1, False)
    door_2 = Door(-100000, -100000, 2, False)
    door_3 = Door(400, 270, 3, True)
    door_4 = Door(-100000, -100000, 4, False)
    door_5 = Door(-100000, -100000, 5, False)
    door_6 = Door(-100000, -100000, 6, False)
    door_text_1 = DoorText(400, 210, door_1)
    door_text_2 = DoorText(400, 510, door_2)
    door_text_3 = DoorText(400, 210, door_3)
    door_text_4 = DoorText(400, 210, door_4)
    door_text_5 = DoorText(400, 210, door_5)
    door_text_6 = DoorText(400, 510, door_6)


def start_three_location():  # Создание третей локации
    global npc, npc_text, npc_2, npc_text_2, player, camera, background, door_1, door_2, door_3, door_4, door_5, door_6, \
        door_text_1, door_text_2, door_text_3, door_text_4, door_text_5, door_text_6, seller, seller_text, tree
    delete_all()

    npc = Npc(800, 170, 5)
    npc_text = NpcText(800, 110)
    npc_2 = Npc(1000, 170, 6)
    npc_text_2 = NpcText(1000, 110)
    seller = Seller(1000, 470, 3)
    seller_text = SellerText(1000, 410)
    player = Player(800, 1000)
    camera = Camera()
    tree = Tree(425, 837)
    background = Background('maps/map_4.png', (1920, 2325))
    door_1 = Door(-100000, -100000, 1, False)
    door_2 = Door(-100000, -100000, 2, False)
    door_3 = Door(-100000, -100000, 3, False)
    door_4 = Door(790, 625, 4, True)
    door_5 = Door(-100000, -100000, 5, False)
    door_6 = Door(-100000, -100000, 6, False)
    door_text_1 = DoorText(400, 210, door_1)
    door_text_2 = DoorText(400, 510, door_2)
    door_text_3 = DoorText(400, 210, door_3)
    door_text_4 = DoorText(400, 210, door_4)
    door_text_5 = DoorText(400, 210, door_5)
    door_text_6 = DoorText(400, 510, door_6)


def start_four_location():  # Создание третей локации
    global npc_text_2, player, camera, background, door_1, door_2, door_3, door_4, door_5, door_6, \
        door_text_1, door_text_2, door_text_3, door_text_4, door_text_5, door_text_6
    delete_all()

    player = Player(450, 400)
    camera = Camera()
    background = Background('maps/map_5.png', (900, 800))
    door_1 = Door(-100000, -100000, 1, False)
    door_2 = Door(-100000, -100000, 2, False)
    door_3 = Door(-100000, -100000, 3, False)
    door_4 = Door(-100000, -100000, 4, False)
    door_5 = Door(-100000, -100000, 5, False)
    door_6 = Door(600, 300, 6, True)
    door_text_1 = DoorText(400, 210, door_1)
    door_text_2 = DoorText(400, 510, door_2)
    door_text_3 = DoorText(400, 210, door_3)
    door_text_4 = DoorText(400, 210, door_4)
    door_text_5 = DoorText(300, 240, door_5)
    door_text_6 = DoorText(600, 240, door_6)


def add_experience(count):
    global experience, experience_index
    experience += count * koef_experience
    if experience_index != 7 and experiences[experience_index] <= experience:
        experience -= experiences[experience_index]
        experience_index += 1
        syuyumbike.update(syuyumbike.lvl + 1)


def add_money(count):
    global money
    money += count * koef_money


class Door(pygame.sprite.Sprite):  # Нпс
    def __init__(self, pos_x, pos_y, image, is_open):
        super().__init__(all_sprites, obstacles_group)
        image = load_image(f'doors/door_{image}/door_{2 if is_open else 1}.png')
        self.image = pygame.transform.scale(image, (60, 82))
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.mask = pygame.mask.from_surface(self.image)
        self.is_open = is_open

        self.x = pos_x
        self.y = pos_y + 100
        self.height = 100
        self.height_pos = 10
        self.weight = 0
        self.weight_pos = 0
        self.weight_flag = False

    def update(self, image):
        self.image = pygame.transform.scale(load_image(f'doors/door_{image}.png'), (80, 100))


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
        self.image = pygame.transform.scale(self.image, (100, 160))
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.mask = pygame.mask.from_surface(self.image)
        self.x = pos_x
        self.y = pos_y + 150
        self.height = 160
        self.height_pos = 10
        self.weight = 0
        self.weight_pos = 0
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
npc = Npc(1100, 170, 1)
npc_text = NpcText(1100, 110)
npc_2 = Npc(1300, 170, 2)
npc_text_2 = NpcText(1300, 110)
seller = Seller(1500, 170, 1)
seller_text = SellerText(1500, 110)
player = Player(2050, 800)
camera = Camera()
tree = Tree(1500000000, 500000000)
house = House(1400, 460)
background = Background('maps/map_1.png', (4500, 1500))
syuyumbike = Syuyumbike(2420, 210, experience_index + 1)
door_1 = Door(1551, 625, 1, experience_index >= 2)
door_2 = Door(2250, 700, 2, experience_index >= 4)
door_3 = Door(-100000, -100000, 3, False)
door_4 = Door(-100000, -100000, 4, False)
door_5 = Door(1700, 560, 5, experience_index == 6)
door_6 = Door(-100000, -100000, 6, False)
door_text_1 = DoorText(1551, 550, door_1)
door_text_2 = DoorText(1500, 630, door_2)
door_text_3 = DoorText(400, 210, door_3)
door_text_4 = DoorText(400, 510, door_4)
door_text_5 = DoorText(1700, 490, door_5)
door_text_6 = DoorText(400, 510, door_6)

if __name__ == '__main__':  # Запуск программы
    pygame.init()
    pygame.display.set_caption('Tatarlango')
    size = width, height = 1200, 800
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)
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
                        losed = 0
                        start_mini_game(npc.lvl_game)
                    if pygame.sprite.collide_mask(player, npc_2):
                        losed = 0
                        start_mini_game(npc_2.lvl_game)
                    if pygame.sprite.collide_mask(player, seller):
                        shop(location)

                    if pygame.sprite.collide_mask(player, door_1) and door_1.is_open:
                        location = 2
                        start_two_location()
                    if pygame.sprite.collide_mask(player, door_2) and door_2.is_open:
                        location = 3
                        start_three_location()
                    if pygame.sprite.collide_mask(player, door_3) and door_3.is_open:
                        location = 1
                        start_first_location()
                    if pygame.sprite.collide_mask(player, door_4) and door_4.is_open:
                        location = 1
                        start_first_location()
                    if pygame.sprite.collide_mask(player, door_5) and door_5.is_open:
                        location = 4
                        start_four_location()
                    if pygame.sprite.collide_mask(player, door_6) and door_6.is_open:
                        location = 1
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

        obstacles_up_group = pygame.sprite.Group()
        obstacles_down_group = pygame.sprite.Group()

        for i in obstacles_group:
            if i.y < player.y:
                obstacles_up_group.add(i)
            else:
                obstacles_down_group.add(i)

        if location == 1:
            screen.fill((21, 97, 21))
        elif location == 2:
            screen.fill((0, 0, 0))
        elif location == 3:
            screen.fill((148, 222, 237))
        else:
            screen.fill((2, 0, 0))
        background_group.draw(screen)
        obstacles_up_group.draw(screen)
        player_group.draw(screen)
        obstacles_down_group.draw(screen)
        object_group.draw(screen)

        font = pygame.font.Font(os.path.join("data/fonts", "Blazma-Regular.ttf"), 30)
        if experience_index < 6:
            experien_text = f' опыт: {experience} / {experiences[experience_index]}'
        else:
            experien_text = f' макс'
        experience_text = font.render(experien_text, False, (0, 0, 255))
        money_text = font.render(f' монеты: {money}', False, (255, 255, 0))
        screen.blit(experience_text, (0, 0))
        screen.blit(money_text, (0, 30))

        pygame.display.flip()
        clock.tick(FPS)
