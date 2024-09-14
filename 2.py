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


def newDialog():  # Обновление диалога
    font_path = os.path.join("data/fonts", "Visitor Rus.ttf")
    font = pygame.font.Font(font_path, 20)
    render_fraze_1 = font.render('', False, (255, 255, 255))
    render_fraze_2 = font.render('', False, (255, 255, 255))
    render_fraze_3 = font.render('', False, (255, 255, 255))
    return render_fraze_1, render_fraze_2, render_fraze_3


def mathGame(m):  # Комната с магом математики
    global background, all_sprites, player_group, player, door, \
        door_group, rectangle_group, loc5, loc11, loc14, x, y
    if player.loc == 10:
        fon = pygame.transform.scale(load_image(m), (800, 505))
    else:
        fon = pygame.transform.scale(load_image(m), (800, 505))
    screen.blit(fon, (0, 0))
    a = random.randint(0, 100)
    difference = random.randint(0, 9)
    b = difference - a
    if m == 'maps/a1_m4.png':
        fraze_1 = 'Я великий маг этого подземелья,'
        fraze_2 = 'и я никому не дам ходить по нему'
        fraze_3 = 'без моего разрешения!'
    elif m == 'maps/a2_m5.png':
        fraze_1 = 'Вот мы снова встретились,'
        fraze_2 = 'и в этот раз ты не уйдёшь так легко.'
        fraze_3 = 'Дальше я тебя не пропущу!'
    else:
        fraze_1 = 'Вот мы снова встретились,'
        fraze_2 = 'и в этот раз ты далеко прошел'
        fraze_3 = 'дальше ты не уйдешь!'
    if m != 'maps/a3_m2.png':
        color = (255, 255, 255)
    else:
        color = (0, 0, 0)

    if player.loc <= 5:
        screen.fill((2, 0, 0))
    elif 5 < player.loc <= 12:
        screen.fill((34, 177, 76))
    else:
        screen.fill((153, 217, 234))
    screen.blit(fon, (0, 0))
    font_path = os.path.join("data/fonts", "Visitor Rus.ttf")
    font = pygame.font.Font(font_path, 20)
    render_fraze_1, render_fraze_2, render_fraze_3 = newDialog()

    win = False
    i = 1
    k = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    if menu([render_fraze_1, render_fraze_2, render_fraze_3],
                            m):
                        return
                    screen.blit(fon, (0, 0))
                if ((event.key == pygame.K_z or event.key == pygame.K_RETURN)
                        and k == 0):
                    if player.loc <= 5:
                        screen.fill((2, 0, 0))
                    elif 5 < player.loc <= 12:
                        screen.fill((34, 177, 76))
                    else:
                        screen.fill((153, 217, 234))
                    screen.blit(fon, (0, 0))
                    if b < 0:
                        question = f"{a}{b}"
                    else:
                        question = f"{a} + {b}"
                    fraze_1 = 'Но ты можешь понадеется на себя,'
                    fraze_2 = 'и решить мою задачу'
                    fraze_3 = 'сколько будет: ' + question
                    render_fraze_1, render_fraze_2, render_fraze_3 = (
                        newDialog())
                    i = 1
                    k = 1
                elif 48 <= event.key <= 58 and k == 1:
                    fraze_1 = event.key - 48
                    render_fraze_1, render_fraze_2, render_fraze_3 = (
                        newDialog())
                    if fraze_1 == difference:
                        if player.loc <= 5:
                            screen.fill((2, 0, 0))
                        elif 5 < player.loc <= 12:
                            screen.fill((34, 177, 76))
                        else:
                            screen.fill((153, 217, 234))
                        screen.blit(fon, (0, 0))
                        if m == 'maps/a1_m4.png':
                            fraze_1 = 'Я вижу, что ты неплох в математике!'
                            fraze_2 = 'На этот раз я тебя пропускаю,'
                            fraze_3 = 'но мы еще встретимся!'
                        elif m == 'maps/a2_m5.png':
                            fraze_1 = 'Я вижу, что ты до сих пор неплох!'
                            fraze_2 = 'В этот раз я тебя пропускаю,'
                            fraze_3 = 'но еще одна наша встреча неизбежна!'
                        else:
                            fraze_1 = ('Я вижу, что ты также силен в '
                                       'математике!')
                            fraze_2 = 'на этот раз покажи себя в равном бою'
                            fraze_3 = 'с истинным магом!'
                        win = True
                    else:
                        if player.loc <= 5:
                            screen.fill((2, 0, 0))
                        elif 5 < player.loc <= 12:
                            screen.fill((34, 177, 76))
                        else:
                            screen.fill((153, 217, 234))
                        screen.blit(fon, (0, 0))
                        fraze_1 = 'Я вижу, что ты слаб,'
                        fraze_2 = 'возвращайся,'
                        fraze_3 = 'лишь когда будешь достоин'
                    i = 1
                    k = 2
                elif ((event.key == pygame.K_z or event.key == pygame.K_RETURN)
                      and k == 2):
                    if win:
                        if m == 'maps/a1_m4.png':
                            all_sprites = pygame.sprite.Group()
                            player_group = pygame.sprite.Group()
                            rectangle_group = pygame.sprite.Group()
                            background = Background('maps/a1_m5.png',
                                                    (839, 1300))
                            all_sprites.add(background)
                            sign1.rect.y = 1000
                            sign2.rect.y = 1000
                            sign3.rect.y = 700
                            sign4.rect.y = 700
                            sign5.rect.y = 400
                            sign6.rect.y = 400
                            all_sprites.add(sign1, sign2, sign3, sign4, sign5,
                                            sign6)
                            sign_group.add(sign1, sign2, sign3, sign4, sign5,
                                           sign6)
                            player = Player(419, 1100, 1)
                            door = Door(362, 30, 1, 2)
                            player.loc = 3
                            loc5 = 0
                        elif m == 'maps/a2_m5.png':
                            a2_location('m2')
                        else:
                            a3_location('m3')
                        camera.update(player)
                        for sprite in all_sprites:
                            camera.apply(sprite)
                        return
                    else:
                        if m == 'maps/a1_m4.png':
                            end_screen(12, False)
                        elif m == 'maps/a2_m5.png':
                            end_screen(21, False)
                        else:
                            end_screen(31, False)
                        return

        if i <= len(fraze_1):
            render_fraze_1 = font.render(fraze_1[:i], False, color)
        elif i <= len(fraze_1) + len(fraze_2):
            render_fraze_2 = font.render(fraze_2[:i - len(fraze_1)], False,
                                         color)
        elif i <= len(fraze_1) + len(fraze_2) + len(fraze_3):
            render_fraze_3 = font.render(
                fraze_3[:i - len(fraze_1) - len(fraze_2)], False,
                color)
        i += 1
        if m == 'maps/a1_m4.png':
            screen.blit(render_fraze_1, (230, 85))
            screen.blit(render_fraze_2, (230, 115))
            screen.blit(render_fraze_3, (230, 145))
        elif m == 'maps/a2_m5.png':
            screen.blit(render_fraze_1, (250, 33))
            screen.blit(render_fraze_2, (250, 51))
            screen.blit(render_fraze_3, (250, 69))
        else:
            screen.blit(render_fraze_1, (230, 85))
            screen.blit(render_fraze_2, (230, 115))
            screen.blit(render_fraze_3, (230, 145))
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(20)
        clock.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def learnScreen():
    fon = pygame.transform.scale(load_image('camera-player/blackfon.png'),
                                 (800, 500))
    screen.blit(fon, (0, 0))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif (event.type == pygame.KEYDOWN or event.type ==
                  pygame.MOUSEBUTTONDOWN):
                return
            elif event.key == pygame.K_ESCAPE:
                return
        clock.tick(FPS)


def start_screen():  # Начальное окно
    fon = pygame.transform.scale(load_image('camera-player/fon.png'),
                                 (800, 500))
    screen.blit(fon, (0, 0))
    pygame.display.flip()
    clock.tick(0.7)
    screen.fill((0, 0, 0))
    menuGet()


def end_screen(n, winOrdie):  # Окно при прохождении акта, либо при проигрыше
    global idSaves
    if not winOrdie:
        fon = pygame.transform.scale(load_image('camera-player/gameover.png'),
                                     (800, 500))
    else:
        fon = pygame.transform.scale(load_image('camera-player/gamewin.png'),
                                     (800, 500))
    fon = pygame.transform.scale(fon, (800, 500))
    screen.blit(fon, (0, 0))
    pygame.display.flip()

    font_path = os.path.join("data/fonts", "Visitor Rus.ttf")
    font = pygame.font.Font(font_path, 35)
    tm = (datetime.datetime.now() - time).total_seconds()
    t2 = font.render(f"{int(tm // 60)} min {int(tm - (tm // 60) * 60)} sec",
                     False, (64, 51, 64))

    if winOrdie:
        t = font.render(f"", False, (64, 51, 64))

        con = sqlite3.connect("data/bd.sqlite")
        cur = con.cursor()
        cur.execute(
            f"INSERT INTO player(IdSaves, act, time) VALUES({idSaves}, {n}, "
            f"'{tm}')")
        con.commit()
        con.close()
    else:
        t = font.render(f"Lose", False, (64, 51, 64))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif (event.type == pygame.KEYDOWN or event.type ==
                  pygame.MOUSEBUTTONDOWN):
                if n == 4:
                    credits_screen()
                    results()
                    act1()
                else:
                    if n == 2:
                        act3()
                    elif n == 31:
                        act3()
                        a3_location('m1')
                    elif n == 32:
                        act3()
                        a3_location('m2')
                    elif n == 1:
                        act2()
                    elif n == 21:
                        act2()
                        a2_location('m1')
                    elif n == 21:
                        act2()
                        a2_location('m2')
                    elif n == 11:
                        act1()
                        a1_location('m1')
                    elif n == 12:
                        act1()
                        a1_location('m2')
                    elif n == 13:
                        act1()
                        a1_location('m3')
                    else:
                        act1()
                return

        screen.blit(t, (100, 250))
        screen.blit(t2, (100, 300))
        pygame.display.flip()
        clock.tick(FPS)


def act1():  # Создание 1 акта
    global all_sprites, player_group, player, background, door, door_group, \
        i, word_group, x, y, loc5, time, runi
    time = datetime.datetime.now()
    fon = pygame.transform.scale(load_image('camera-player/act1.png'),
                                 (800, 500))
    pygame.mixer.music.load("data/music/start_sound.ogg")
    pygame.mixer.music.set_volume(valueMusic)
    pygame.mixer.music.play(loops=-1)
    screen.blit(fon, (0, 0))
    pygame.display.flip()
    clock.tick(1)

    all_sprites = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    door_group = pygame.sprite.Group()
    background = Background('maps/a1_m1.png', (1360, 760))
    door = Door(1180, 440, 1, 1)
    all_sprites.add(background)
    door_group.add(door)
    pygame.mixer.music.load("data/music/act1_main.ogg")
    pygame.mixer.music.set_volume(valueMusic)
    pygame.mixer.music.play(loops=-1)
    player = Player(290, 470, 1)
    word_group = pygame.sprite.Group()
    x, y = 0, 0
    loc5 = 0
    i = 0
    runi = -600
    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)

    screen.blit(
        pygame.transform.scale(load_image("camera-player/run.png"), (40, 40)),
        (5, 5))
    font_path = os.path.join("data/fonts", "Visitor Rus.ttf")
    txt = pygame.font.Font(font_path, 35).render(f"active", True,
                                                 (255, 0, 0))
    screen.blit(txt, (50, 0))
    all_sprites.draw(screen)


def act2():  # Создание 2 акта
    global all_sprites, player_group, player, background, door, \
        door_group, time, x, y, door2, door3, pas, loc11, img, runi
    time = datetime.datetime.now()
    fon = pygame.transform.scale(load_image('camera-player/act2.png'),
                                 (800, 500))
    pygame.mixer.music.load("data/music/start_sound.ogg")
    pygame.mixer.music.set_volume(valueMusic)
    pygame.mixer.music.play(loops=-1)
    screen.blit(fon, (0, 0))
    pygame.display.flip()
    clock.tick(1)

    all_sprites = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    door_group = pygame.sprite.Group()
    background = Background('maps/a2_m1.png', (2060, 1500))
    door = Door(350, 840, 2, 1)
    door2 = Door(1528, 540, 2, 1)
    door3 = Door(350, 540, 2, 1)
    all_sprites.add(background)
    door_group.add(door, door2, door3)
    pas = Pass(850, 700)
    img = load_image('objects/key.jpg')
    img = pygame.transform.scale(img, (50, 50))
    pygame.mixer.music.load("data/music/act2_main.ogg")
    pygame.mixer.music.set_volume(valueMusic)
    pygame.mixer.music.play(loops=-1)
    x, y = 0, 0
    loc11 = 0
    runi = -600
    player = Player(730, 730, 2)
    player.loc = 6
    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)

    screen.blit(
        pygame.transform.scale(load_image("camera-player/run.png"), (40, 40)),
        (5, 5))
    font_path = os.path.join("data/fonts", "Visitor Rus.ttf")
    txt = pygame.font.Font(font_path, 35).render(f"active", True,
                                                 (255, 0, 0))
    screen.blit(txt, (50, 0))
    all_sprites.draw(screen)
    door_group.draw(screen)


def act3():  # Создание 3 акта
    global all_sprites, player_group, player, background, door, door_group, \
        i, x, y, time, defen, traveler, apples, runi
    fon = pygame.transform.scale(load_image('camera-player/act3.png'),
                                 (800, 500))
    screen.blit(fon, (0, 0))
    pygame.mixer.music.load("data/music/start_sound.ogg")
    pygame.mixer.music.set_volume(valueMusic)
    pygame.mixer.music.play(loops=-1)
    pygame.display.flip()
    clock.tick(1)

    all_sprites = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    door_group = pygame.sprite.Group()
    background = Background('maps/a3_m1.png', (4000, 2480))
    all_sprites.add(background)
    pygame.mixer.music.load("data/music/act3_main.ogg")
    pygame.mixer.music.set_volume(valueMusic)
    pygame.mixer.music.play(loops=-1)
    door = Door(550, 1720, 3, 3)
    door_group.add(door)
    player = Player(530, 200, 3)
    traveler = Traveler(3400, 1320)
    player.loc = 13
    runi = -600
    defen = Defense(770, 1200)
    apples = [
        Apple(1800, 2090),
        Apple(1810, 2110),
        Apple(2100, 2260),
        Apple(3600, 540),
        Apple(3570, 450)
    ]
    AppleTree(1828, 1930),
    AppleTree(2100, 2100),
    AppleTree(3670, 360)

    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)

    screen.blit(
        pygame.transform.scale(load_image("camera-player/run.png"), (40, 40)),
        (5, 5))
    font_path = os.path.join("data/fonts", "Visitor Rus.ttf")
    txt = pygame.font.Font(font_path, 35).render(f"active", True,
                                                 (255, 0, 0))
    screen.blit(txt, (50, 0))
    all_sprites.draw(screen)


t1 = None
t2 = None
t3 = None
t4 = None
t5 = None


def other_color(cl1, cl2, cl3, cl4):  # Смена цвета кнопки в меню
    global t1, t2, t3, t4
    font_path = os.path.join("data/fonts", "Visitor Rus.ttf")
    font = pygame.font.Font(font_path, 40)
    t1 = font.render(f"Music",
                     False, cl1)
    t2 = font.render(f"How play",
                     False, cl2)
    t3 = font.render(f"Exit",
                     False, cl3)
    t4 = font.render(f"Cancel",
                     False, cl4)


def a1_location(m):
    global all_sprites, player_group, word_group, door_group, background, \
        door, player, rectangle_group, x, y, loc5, time, boss_Act1
    tm = (datetime.datetime.now() - time).total_seconds()
    time = datetime.datetime.now()
    if m == 'm1':
        all_sprites = pygame.sprite.Group()
        player_group = pygame.sprite.Group()
        word_group = pygame.sprite.Group()
        door_group = pygame.sprite.Group()
        background = Background('maps/a1_m3.png', (2100, 500))
        all_sprites.add(background)
        pygame.mixer.music.load("data/music/act1_main.ogg")
        pygame.mixer.music.set_volume(valueMusic)
        pygame.mixer.music.play(loops=-1)
        door = Door(1800, 200, 1, 1)
        player = Player(200, 330, 1)
        player.loc = 2
        con = sqlite3.connect("data/bd.sqlite")
        cur = con.cursor()
        cur.execute(f"""DELETE from player where idSaves == {idSaves} 
        and act == 11""")
        cur.execute(
            f"INSERT INTO player(IdSaves, act, time) VALUES({idSaves}, 11, "
            f"'{tm}')")
        con.commit()
        con.close()
    elif m == 'm2':
        all_sprites = pygame.sprite.Group()
        player_group = pygame.sprite.Group()
        background = Background('maps/a1_m4.png', (700, 500))
        all_sprites.add(background)
        pygame.mixer.music.load("data/music/act1_main.ogg")
        pygame.mixer.music.set_volume(valueMusic)
        pygame.mixer.music.play(loops=-1)
        player = Player(385, 300, 1)
        player.loc = 3
        mathGame('maps/a1_m4.png')
        con = sqlite3.connect("data/bd.sqlite")
        cur = con.cursor()
        cur.execute(f"""DELETE from player where idSaves == {idSaves} 
        and act == 12""")
        cur.execute(
            f"INSERT INTO player(IdSaves, act, time) VALUES({idSaves}, 12, "
            f"'{tm}')")
        con.commit()
        con.close()
    elif m == 'm3':
        all_sprites = pygame.sprite.Group()
        player_group = pygame.sprite.Group()
        rectangle_group = pygame.sprite.Group()
        background = Background('maps/a1_m6.png', (900, 784))
        all_sprites.add(background)
        pygame.mixer.music.load("data/music/act1_boss.ogg")
        pygame.mixer.music.set_volume(valueMusic)
        pygame.mixer.music.play(loops=-1)
        player = Player(450, 300, 1)
        player.loc = 4
        x = player.x
        y = player.y

        boss_Act1 = Boss_act1(300, -180)
        loc5 = 0
        door = Door(20000, 20000, 1, 1)

        con = sqlite3.connect("data/bd.sqlite")
        cur = con.cursor()
        cur.execute(f"""DELETE from player where idSaves == {idSaves} 
        and act == 13""")
        cur.execute(
            f"INSERT INTO player(IdSaves, act, time) VALUES({idSaves}, 13, "
            f"'{tm}')")
        con.commit()
        con.close()


def a2_location(m):
    global all_sprites, player_group, door_group, background, pas, door, \
        door2, door3, pas, player, rectangle_group, x, y, loc11, time, boss_Act2
    tm = (datetime.datetime.now() - time).total_seconds()
    time = datetime.datetime.now()
    if m == 'm1':
        all_sprites = pygame.sprite.Group()
        player_group = pygame.sprite.Group()
        door_group = pygame.sprite.Group()
        background = Background('maps/a2_m4.png', (2060, 1500))
        pas = Pass(850, 550)
        door = Door(350, 840, 2, 1)
        door2 = Door(1528, 540, 2, 1)
        door3 = Door(350, 540, 2, 1)
        all_sprites.add(background)
        door_group.add(door)
        door_group.add(door2)
        door_group.add(door3)
        pas = Pass(840, 600)
        player = Player(player.x, player.y - 60, 2)
        player.loc = 9
        pygame.mixer.music.load("data/music/act2_main.ogg")
        pygame.mixer.music.set_volume(valueMusic)
        pygame.mixer.music.play(loops=-1)
        con = sqlite3.connect("data/bd.sqlite")
        cur = con.cursor()
        cur.execute(f"""DELETE from player where idSaves == {idSaves} 
        and act == 21""")
        cur.execute(
            f"INSERT INTO player(IdSaves, act, time) VALUES({idSaves}, 21, "
            f"'{tm}')")
        con.commit()
        con.close()
    else:
        all_sprites = pygame.sprite.Group()
        player_group = pygame.sprite.Group()
        rectangle_group = pygame.sprite.Group()
        background = Background('maps/a2_m6.png',
                                (1667, 1000))
        all_sprites.add(background)
        player = Player(850, 506, 2)
        player.loc = 11
        door.rect.x = 20000
        door2.rect.x = 20000
        door3.rect.x = 20000
        boss_Act2 = Boss_act2(750, -35)
        x = player.x
        y = player.y
        loc11 = 0
        pygame.mixer.music.load("data/music/act2_boss.ogg")
        pygame.mixer.music.set_volume(valueMusic)
        pygame.mixer.music.play(loops=-1)

        con = sqlite3.connect("data/bd.sqlite")
        cur = con.cursor()
        cur.execute(f"""DELETE from player where idSaves == {idSaves} 
        and act == 22""")
        cur.execute(
            f"INSERT INTO player(IdSaves, act, time) VALUES({idSaves}, 22, "
            f"'{tm}')")
        con.commit()
        con.close()


def a3_location(m):
    global all_sprites, player_group, background, player, rectangle_group, \
        x, y, loc14, time, boss_Act3, boss_Act3_group
    tm = (datetime.datetime.now() - time).total_seconds()
    time = datetime.datetime.now()
    if m == 'm1':
        all_sprites = pygame.sprite.Group()
        player_group = pygame.sprite.Group()
        background = Background('maps/a3_m2.png', (750, 400))
        all_sprites.add(background)
        player = Player(385, 300, 1)
        player.loc = 14
        pygame.mixer.music.load("data/music/act3_main.ogg")
        pygame.mixer.music.set_volume(valueMusic)
        pygame.mixer.music.play(loops=-1)
        mathGame('maps/a3_m2.png')
        con = sqlite3.connect("data/bd.sqlite")
        cur = con.cursor()
        cur.execute(f"""DELETE from player where idSaves == {idSaves} 
        and act == 31""")
        cur.execute(
            f"INSERT INTO player(IdSaves, act, time) VALUES({idSaves}, 31, "
            f"'{tm}')")
        con.commit()
        con.close()
    else:
        all_sprites = pygame.sprite.Group()
        player_group = pygame.sprite.Group()
        rectangle_group = pygame.sprite.Group()
        background = Background('maps/a3_m3.png',
                                (2210, 1300))
        all_sprites.add(background)
        player = Player(1105, 650, 3)
        player.loc = 15
        door.rect.x = 20000
        x = player.x
        y = player.y
        loc14 = 0
        boss_Act3_group = pygame.sprite.Group()
        boss_Act3 = Boss_act3(20000, 20000)
        boss_Act3_group.add(boss_Act3)
        pygame.mixer.music.load("data/music/act3_boss.ogg")
        pygame.mixer.music.set_volume(valueMusic)
        pygame.mixer.music.play(loops=-1)

        con = sqlite3.connect("data/bd.sqlite")
        cur = con.cursor()
        cur.execute(f"""DELETE from player where idSaves == {idSaves} 
        and act == 32""")
        cur.execute(
            f"INSERT INTO player(IdSaves, act, time) VALUES({idSaves}, 32, "
            f"'{tm}')")
        con.commit()
        con.close()


def music(arg, m):
    global running, valueMusic
    # Цвета
    white = (255, 0, 0)

    # Создание ползунка
    font_path = os.path.join("data/fonts", "Visitor Rus.ttf")
    font = pygame.font.Font(font_path, 40)
    texttt = font.render('Volume:', True, white)

    pygame.mixer.music.set_volume(valueMusic)  # Установка начальной громкости

    try:
        if running:
            n = 0
    except Exception:
        running = True
    # Главный цикл
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                    return

        # Обработка ползунка
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and valueMusic < 1.0:
            valueMusic += 0.01
        elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and valueMusic > 0.0:
            valueMusic -= 0.01

        pygame.mixer.music.set_volume(valueMusic)  # Обновление громкости

        # Обновление текста
        volume_text = font.render(str(int(valueMusic * 100)), True, white)

        if arg:
            fon = pygame.transform.scale(load_image(m), (800, 505))
            screen.blit(fon, (0, 0))
            if m == 'maps/a1_m4.png':
                screen.blit(arg[0], (230, 85))
                screen.blit(arg[1], (230, 115))
                screen.blit(arg[2], (230, 145))
            elif m == 'maps/a2_m5.png':
                screen.blit(arg[0], (250, 33))
                screen.blit(arg[1], (250, 51))
                screen.blit(arg[2], (250, 69))
            else:
                screen.blit(arg[0], (230, 85))
                screen.blit(arg[1], (230, 115))
                screen.blit(arg[2], (230, 145))
            player_group.draw(screen)
            screen.blit(texttt, (300, 160))
            screen.blit(volume_text, (330, 260))
        else:
            # Отрисовка
            all_sprites.draw(screen)
            if player.loc <= 5:
                screen.fill((2, 0, 0))
            elif 5 < player.loc <= 12:
                screen.fill((34, 177, 76))
            else:
                screen.fill((153, 217, 234))

            # обновляем положение всех спрайтов
            for sprite in all_sprites:
                camera.apply(sprite)
            camera.update(player)
            wizardRus.update()
            all_sprites.draw(screen)
            if player.loc == 7:
                screen.blit(task_text, (x - player.x + 780, y -
                                        player.y + 160))

            if not player.key and pygame.sprite.collide_mask(player, chest):
                # Взаимодействие с сундуком
                font_path = os.path.join("data/fonts", "Visitor Rus.ttf")
                font = pygame.font.Font(font_path, 40)
                task_text = font.render("Нужен ключ!", False, (255, 255, 255))
                screen.blit(task_text, (300, 0))

            if pygame.sprite.collide_mask(player,
                                          traveler):  # Взаимодействие с нпс
                font_path = os.path.join("data/fonts", "Visitor Rus.ttf")
                font = pygame.font.Font(font_path, 25)
                if player.apples not in [5, 6]:
                    task_text = font.render("Принеси мне 5 яблок, в обмен "
                                            "на инфор"
                                            "мацию.", False, (255, 255, 255))
                    task_text2 = font.render('Они находятся рядом с 3-мя '
                                             'яблонями',
                                             False, (255, 255, 255))
                else:
                    task_text = font.render(
                        "Выпей воды из речки, и ты станешь невидимым.", False,
                        (255, 255, 255))
                    task_text2 = font.render(
                        'Это поможет тебе скрыться от стражника', False,
                        (255, 255, 255))
                    player.apples = 6
                screen.blit(task_text, (180, 0))
                screen.blit(task_text2, (180, 40))

            if (not player.pas and pygame.sprite.collide_mask(player, pas) and
                    player.loc == 6):  # Взаимодействие с автоматом
                font_path = os.path.join("data/fonts", "Visitor Rus.ttf")
                font = pygame.font.Font(font_path, 40)
                task_text = font.render("Нужна монета!", False,
                                        (255, 255, 255))
                screen.blit(task_text, (300, 0))
            player_group.draw(screen)

            if player.loc == 2:
                word_group.draw(screen)

            screen.blit(pygame.transform.scale(load_image("camera-player/run."
                                                          "png"),
                                               (40, 40)),
                        (5, 5))
            font_path = os.path.join("data/fonts", "Visitor Rus.ttf")
            if runi == -600:  # Активация ускорения
                txt = pygame.font.Font(font_path, 35).render("active", True,
                                                             (255, 0, 0))
                screen.blit(txt, (50, 0))
            else:
                txt = pygame.font.Font(font_path, 30).render(
                    f"{(runi + 660) // 60}", True, (255, 0, 0))
                screen.blit(txt, (50, 5))

            if player.key:
                screen.blit(img, (750, 0))

            if player.apples != 6:
                for i in range(player.apples):
                    screen.blit(img, (770 - i * 30, 0))

            door_group.draw(screen)
            defense_group.draw(screen)
            apple_trees_group.draw(screen)
            apple_group.draw(screen)
            screen.blit(texttt, (300, 160))
            screen.blit(volume_text, (330, 260))
        pygame.display.flip()
        pygame.time.Clock().tick(60)


def menu(arg, m):  # Меню
    COLOR1 = (64, 64, 64)
    COLOR2 = (255, 0, 0)

    other_color(COLOR1, COLOR1, COLOR1, COLOR2)
    colT = 4

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    colT -= 1
                    if colT == 0:
                        colT = 4
                        other_color(COLOR1, COLOR1, COLOR1,
                                    COLOR2)
                    if colT == 1:
                        other_color(COLOR2, COLOR1, COLOR1,
                                    COLOR1)
                    if colT == 2:
                        other_color(COLOR1, COLOR2, COLOR1,
                                    COLOR1)
                    if colT == 3:
                        other_color(COLOR1, COLOR1, COLOR2,
                                    COLOR1)

                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    colT += 1
                    if colT == 5:
                        colT = 1
                        other_color(COLOR2, COLOR1, COLOR1,
                                    COLOR1)
                    if colT == 4:
                        other_color(COLOR1, COLOR1, COLOR1, COLOR2)
                    if colT == 2:
                        other_color(COLOR1, COLOR2, COLOR1,
                                    COLOR1)
                    if colT == 3:
                        other_color(COLOR1, COLOR1, COLOR2,
                                    COLOR1)

                if (event.key == pygame.K_SPACE or event.key == pygame.K_p or
                        event.key == pygame.K_RETURN):
                    if colT == 1:
                        music(arg, m)
                    if colT == 2:
                        learnScreen()
                    if colT == 3:
                        pygame.mixer.music.pause()
                        start_screen()
                        return True
                    return
                if event.key == pygame.K_ESCAPE:
                    return

        screen.blit(t1, (300, 80))
        screen.blit(t2, (300, 160))
        screen.blit(t3, (300, 240))
        screen.blit(t4, (300, 320))
        pygame.display.flip()
        clock.tick(FPS)


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

    def update(self, move_up, move_down, move_left, move_right, passaa=None):
        global all_sprites, background, player, player_group, door_group, \
            door, word_group, x, y, task_text, ok_tip, door2, door3, \
            chest, img, pas, rectangle_group, loc5, loc11, text1, text2, \
            text3, text4, defense_group
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
        if pygame.sprite.collide_mask(self, door):  # Соприкосновение со дверью
            if self.loc == 0:
                all_sprites = pygame.sprite.Group()
                player_group = pygame.sprite.Group()
                door_group = pygame.sprite.Group()
                background = Background('maps/a1_m2.png', (839, 1300))
                all_sprites.add(background)
                player = Player(419, 950, 1)
                player.loc = 1
                wizardRus.rect.x = 419
                wizardRus.rect.y = 600
                wizardRus.canRun = False
                wizardRus.y = 600
                all_sprites.add(wizardRus)
                door = Door(363, 48, 1, 2)
            elif self.loc == 1:
                a1_location('m1')
            elif self.loc == 2:
                a1_location('m2')
            elif self.loc == 3:
                a1_location('m3')
            elif self.loc == 5:
                door.rect.x = 20000
                self.loc = 6
                end_screen(1, True)
            elif self.loc == 6 or self.loc == 9:
                button_question = ['Сердце', "Почки", "Мозг", "Лёгкие"]
                all_sprites = pygame.sprite.Group()
                player_group = pygame.sprite.Group()
                word_group = pygame.sprite.Group()
                door_group = pygame.sprite.Group()
                background = Background('maps/a2_m2.png', (2380, 1500))
                all_sprites.add(background)
                door = Door(1670, 750, 2, 1)
                for j in range(1, 5):
                    button_group.add(Button(775 + j * 150, 800, j))
                player = Player(1600, 750, 2, key=player.key, pas=player.pas)
                font_path = os.path.join("data/fonts", "Visitor Rus.ttf")
                font = pygame.font.Font(font_path, 50)
                ok_tip = random.randint(0, 3)
                task_text = font.render(button_question[ok_tip], False,
                                        (255, 255, 255))
                x, y = 700, 640
                player.loc = 7
            elif self.loc == 7:
                all_sprites = pygame.sprite.Group()
                player_group = pygame.sprite.Group()
                door_group = pygame.sprite.Group()
                background = Background('maps/a2_m1.png', (2060, 1500))
                door = Door(350, 840, 2, 1)
                door2 = Door(1528, 540, 2, 1)
                door3 = Door(350, 540, 2, 1)
                all_sprites.add(background)
                door_group.add(door, door2, door3)
                pas = Pass(850, 700)
                player = Player(480, 840, 2, key=player.key, pas=player.pas)
                player.loc = 6
            elif self.loc == 12:
                door.rect.x = 20000
                self.loc = 13
                end_screen(2, True)
            elif self.loc == 13:
                a3_location('m1')
            elif self.loc == 16:
                door.rect.x = 20000
                self.loc = 17
                end_screen(4, True)
        for j in apples:
            if pygame.sprite.collide_mask(self, j):
                j.rect.x = 20000
                player.apples += 1
                img = load_image('objects/apple.jpg')
                img = pygame.transform.scale(img, (30, 30))
        self.task_text = ''
        if 740 < self.x < 1130 and 1100 < self.y < 1330 and self.loc == 13 and self.vis:
            font_path = os.path.join("data/fonts", "Visitor Rus.ttf")
            font = pygame.font.Font(font_path, 40)
            self.task_text = font.render("Дальше нельзя", False, (0, 0, 0))
        if pygame.sprite.collide_mask(self, door3):
            if self.loc == 6 or self.loc == 9:
                all_sprites = pygame.sprite.Group()
                player_group = pygame.sprite.Group()
                word_group = pygame.sprite.Group()
                door_group = pygame.sprite.Group()
                background = Background('maps/a2_m3.png', (4000, 4000))
                all_sprites.add(background)
                chest = Chest(777, 742)
                door3 = Door(3450, 810, 2, 1)
                player = Player(3360, 800, 2, key=player.key, pas=player.pas)
                x, y = 700, 640
                player.loc = 8
            elif self.loc == 8:
                all_sprites = pygame.sprite.Group()
                player_group = pygame.sprite.Group()
                door_group = pygame.sprite.Group()
                background = Background('maps/a2_m1.png', (2060, 1500))
                door = Door(350, 840, 2, 1)
                door2 = Door(1528, 540, 2, 1)
                door3 = Door(350, 540, 2, 1)
                all_sprites.add(background)
                door_group.add(door, door2, door3)
                pas = Pass(850, 700)
                player = Player(480, 540, 2, key=player.key, pas=player.pas)
                player.loc = 6
        if pygame.sprite.collide_mask(self, chest) and self.loc != 9:
            if player.key:
                if self.ones:
                    player.pas = True
                    img = load_image('objects/cash.jpg')
                    img = pygame.transform.scale(img, (50, 50))
                    chest.image = pygame.transform.scale(
                        load_image('objects/chest_open.jpg'), (60, 40))
                    self.ones = False
        if player.apples == 6 and background.get_rgb(self.x + self.run,
                                                     self.y + self.run) == \
                (0, 187, 255):
            player.vis = False

        if pygame.sprite.collide_mask(self, pas) and self.loc != 9:
            if player.pas:
                a2_location('m1')
        if pygame.sprite.collide_mask(self, door2):
            all_sprites = pygame.sprite.Group()
            player_group = pygame.sprite.Group()
            background = Background('maps/a1_m4.png', (750, 400))
            all_sprites.add(background)
            player = Player(335, 200, 1)
            player.loc = 10
            mathGame('maps/a2_m5.png')
        elif pygame.sprite.collide_mask(self, sign1):
            font_path = os.path.join("data/fonts", "Visitor Rus.ttf")
            font = pygame.font.Font(font_path, 20)
            text1 = font.render(
                'Беги, пока не поздно! Это Маг Физик! Он владеет силами', False,
                (255, 255, 255))
            text2 = font.render(
                'природы и науки. Ни один закон физики не может ему', False,
                (255, 255, 255))
            text3 = font.render(
                'противостоять. Ты на пути его научных исследований',
                False, (255, 255, 255))
            text4 = font.render(
                'исследований, и это будет последнее, что ты увидишь!',
                False, (255, 255, 255))
        elif pygame.sprite.collide_mask(self, sign2):
            font_path = os.path.join("data/fonts", "Visitor Rus.ttf")
            font = pygame.font.Font(font_path, 20)
            text1 = font.render('Эти ворота скрывают ТЕБЯ от НЕГО!', False,
                                (255, 255, 255))
            text2 = font.render(
                'Он никогда не проигрывал в научных битвах до этого.', False,
                (255, 255, 255))
            text3 = font.render(
                'Он мог бы сбежать отсюда, но власть, которую он',
                False, (255, 255, 255))
            text4 = font.render('получил здесь очень манит его.', False,
                                (255, 255, 255))
        elif pygame.sprite.collide_mask(self, sign3):
            font_path = os.path.join("data/fonts", "Visitor Rus.ttf")
            font = pygame.font.Font(font_path, 20)
            text1 = font.render(
                'Он умеет изменять структуру времени. ', False,
                (255, 255, 255))
            text2 = font.render(
                'Твое будущее уже записано, и оно в его руках.', False,
                (255, 255, 255))
            text3 = font.render(
                'Никто не смог выйти из его лабиринта времени.',
                False, (255, 255, 255))
            text4 = font.render('', False,
                                (255, 255, 255))
        elif pygame.sprite.collide_mask(self, sign4):
            font_path = os.path.join("data/fonts", "Visitor Rus.ttf")
            font = pygame.font.Font(font_path, 20)
            text1 = font.render(
                'Когда он разгневан, его силы становятся', False,
                (255, 255, 255))
            text2 = font.render(
                'неописуемыми. Попадись на его пути, и ты станешь', False,
                (255, 255, 255))
            text3 = font.render(
                'частью его физического эксперимента!',
                False, (255, 255, 255))
            text4 = font.render('', False,
                                (255, 255, 255))
        elif pygame.sprite.collide_mask(self, sign5):
            font_path = os.path.join("data/fonts", "Visitor Rus.ttf")
            font = pygame.font.Font(font_path, 20)
            text1 = font.render(
                'Его ум остр, как лучи света. Ни одна тайна не может', False,
                (255, 255, 255))
            text2 = font.render(
                'ускользнуть от его внимания.', False,
                (255, 255, 255))
            text3 = font.render(
                'Твои мысли уже известны ему.',
                False, (255, 255, 255))
            text4 = font.render('', False,
                                (255, 255, 255))
        elif pygame.sprite.collide_mask(self, sign6):
            font_path = os.path.join("data/fonts", "Visitor Rus.ttf")
            font = pygame.font.Font(font_path, 20)
            text1 = font.render(
                'Он проник в самые глубины квантовой реальности.', False,
                (255, 255, 255))
            text2 = font.render(
                'Вселенная - это его лаборатория.', False,
                (255, 255, 255))
            text3 = font.render(
                'Попытайся не потеряться в его',
                False, (255, 255, 255))
            text4 = font.render('многомерных исследованиях.', False,
                                (255, 255, 255))
        elif self.loc == 3:
            font_path = os.path.join("data/fonts", "Visitor Rus.ttf")
            font = pygame.font.Font(font_path, 20)
            text1 = font.render('', False, (255, 255, 255))
            text2 = font.render('', False, (255, 255, 255))
            text3 = font.render('', False, (255, 255, 255))
            text4 = font.render('', False, (255, 255, 255))
        for defen in defense_group:
            if pygame.sprite.collide_mask(self, defen) and self.vis:
                # Откидываем игрока назад при коллизии
                if move_left:
                    self.rect.x += self.run
                    self.x += self.run
                if move_right:
                    self.rect.x -= self.run
                    self.x -= self.run
                if move_up:
                    self.rect.y += self.run
                    self.y += self.run
                if move_down:
                    self.rect.y -= self.run
                    self.y -= self.run

        for apple_tree in apple_trees_group:
            if pygame.sprite.collide_mask(self, apple_tree):
                # Откидываем игрока назад при коллизии
                if move_left:
                    self.rect.x += self.run
                    self.x += self.run
                if move_right:
                    self.rect.x -= self.run
                    self.x -= self.run
                if move_up:
                    self.rect.y += self.run
                    self.y += self.run
                if move_down:
                    self.rect.y -= self.run
                    self.y -= self.run
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)


class AppleTree(pygame.sprite.Sprite):  # Дерево
    def __init__(self, x_pos, y_pos):
        super().__init__(all_sprites, apple_trees_group)
        image = load_image('objects/apple_tree.png')
        image = pygame.transform.scale(image, (120, 200))
        self.image = image
        self.rect = self.image.get_rect().move(x_pos, y_pos)


class Sign(pygame.sprite.Sprite):  # Табличка
    image = load_image('objects/sign.png')
    image = pygame.transform.scale(image, (51, 54))

    def __init__(self, x_pos, y_pos):
        super().__init__(all_sprites, sign_group)
        self.image = Sign.image
        self.rect = self.image.get_rect().move(x_pos, y_pos)


class Letters(pygame.sprite.Sprite):  # Буквы для атаки
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites)
        random_letters = random.choice(['objects/letter_a.png',
                                        'objects/letter_b.png',
                                        'objects/letter_v.png',
                                        'objects/letter_g.png',
                                        'objects/letter_d.png'])
        image_path = load_image(random_letters)
        self.image = pygame.transform.scale(image_path, (40, 60))
        self.rect = self.image.get_rect().move(pos_x, pos_y)

    def update(self):
        self.rect.x -= 9
        if pygame.sprite.collide_mask(self, player):
            end_screen(11, False)
            return


class Background(pygame.sprite.Sprite):  # Задний фон
    def __init__(self, image_path, size):
        super().__init__()
        self.image = load_image(image_path)
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_threshold(self.image, (237, 28, 36),
                                               (1, 1, 1, 255))

    def get_rgb(self, x, y):  # Возвращение цвета о пикселе фона
        pixel = pygame.PixelArray(self.image)
        return self.image.unmap_rgb(pixel[x][y])

    def update(self, imageBoss, size):
        self.image = load_image(imageBoss)
        self.image = pygame.transform.scale(self.image, size)


class Door(pygame.sprite.Sprite):  # Дверь
    def __init__(self, pos_x, pos_y, act, tip):
        super().__init__(all_sprites)
        if act == 1:
            image_path = load_image(f'doors/door_act1_{tip}.png')
        elif act == 2:
            image_path = load_image('doors/door_act2.png')
        if act == 3:
            image_path = load_image('doors/door_act3.png')
        if tip == 1:
            self.image = pygame.transform.scale(image_path, (120, 96))
        elif tip == 2:
            self.image = pygame.transform.scale(image_path, (112, 67))
        elif tip == 3:
            self.image = pygame.transform.scale(image_path, (120, 120))
        self.rect = self.image.get_rect().move(pos_x, pos_y + 20)
        self.mask = pygame.mask.from_surface(self.image)


class Rectangle(pygame.sprite.Sprite):  # Атакующие объекты из комнат боссов
    def __init__(self, pos_x, pos_y, vx, vy, xx, yy, canDamage, image):
        image_path = load_image(image)
        image_path = pygame.transform.scale(image_path, (xx, yy))
        sprite_image = image_path
        super().__init__(rectangle_group, all_sprites)
        self.image = sprite_image
        self.rect = self.image.get_rect().move(pos_x, pos_y + 20)
        self.mask = pygame.mask.from_surface(self.image)
        self.vx = vx
        self.vy = vy
        self.canDamage = canDamage

    def update(self):  # Обновление движения
        global rectangle_group, plat
        self.rect.x += 2 * self.vx
        self.rect.y += 2 * self.vy
        if self.canDamage and not (pygame.sprite.collide_mask(player, plat)):
            if pygame.sprite.collide_mask(self, player):
                for j in rectangle_group:
                    j.rect.x = 10000

                rectangle_group = pygame.sprite.Group()
                if player.loc == 4:
                    end_screen(13, False)
                elif player.loc == 11:
                    end_screen(22, False)
                elif player.loc == 15:
                    end_screen(32, False)
                return


class Button(pygame.sprite.Sprite):  # Кнопки выбора
    def __init__(self, pos_x, pos_y, tip):
        super().__init__(all_sprites)
        if player.loc == 15:
            image_path = load_image(f'buttons/button{tip}_{tip}.jpg')
        else:
            image_path = load_image(f'buttons/button{tip}.png')
        self.image = pygame.transform.scale(image_path, (80, 80))
        self.rect = self.image.get_rect().move(pos_x, pos_y + 20)
        self.mask = pygame.mask.from_surface(self.image)
        self.tip = tip
        self.tm = 300

    def update(self):
        if player.loc != 15:
            if pygame.sprite.spritecollideany(self, player_group):
                font_path = os.path.join("data/fonts", "Visitor Rus.ttf")
                font = pygame.font.Font(font_path, 50)
                screen.blit(
                    font.render(str(self.tm // 60 + 1), False, (0, 0, 0)),
                    (350, 0))
                if self.tm // 60 + 1 == 0:
                    if self.tip == ok_tip + 1:
                        self.tm += 1
                        player.key = True
                    else:
                        for j in button_group:
                            j.rect.x = 20000
                        end_screen(1, False)
                self.tm -= 1
            else:
                self.tm = 300


class Pass(pygame.sprite.Sprite):  # Автомат у речки
    image = load_image('objects/pass.png')
    image = pygame.transform.scale(image, (79, 90))

    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = Pass.image
        self.rect = self.image.get_rect().move(pos_x, pos_y)


class Chest(pygame.sprite.Sprite):  # Сундук
    image = load_image('objects/chest.jpg')
    image = pygame.transform.scale(image, (60, 40))

    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = Chest.image
        self.rect = self.image.get_rect().move(pos_x, pos_y)


class Defense(pygame.sprite.Sprite):  # Защитник
    image = load_image('npc/defens.jpg')
    image = pygame.transform.scale(image, (283, 260))

    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, defense_group)
        self.image = Defense.image
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.mask = pygame.mask.from_surface(self.image)


class Apple(pygame.sprite.Sprite):  # Яблоко
    image = load_image('objects/apple.jpg')
    image = pygame.transform.scale(image, (20, 20))

    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, apple_group)
        self.image = Apple.image
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.mask = pygame.mask.from_surface(self.image)


class Traveler(pygame.sprite.Sprite):  # НПС, путник у реки
    image = load_image('npc/traveler.jpg')
    image = pygame.transform.scale(image, (70, 118))

    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = Traveler.image
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.mask = pygame.mask.from_surface(self.image)


class Platform(pygame.sprite.Sprite):  # Платформа 3 акта босса
    image = load_image('objects/platform.jpg')
    image = pygame.transform.scale(image, (100, 90))

    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = Platform.image
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.mask = pygame.mask.from_surface(self.image)


class Boss_act1(pygame.sprite.Sprite):  # Босс 1 акт
    image = load_image('npc/wizard_physics.png')
    image = pygame.transform.scale(image, (300, 200))

    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = Boss_act1.image
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.mask = pygame.mask.from_surface(self.image)


class Boss_act2(pygame.sprite.Sprite):  # Босс 1 акт
    image = load_image('npc/wizard_nature.png')
    image = pygame.transform.scale(image, (200, 300))

    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = Boss_act2.image
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.mask = pygame.mask.from_surface(self.image)


class Boss_act3(pygame.sprite.Sprite):  # Босс 3 акт
    image = load_image('npc/wizard.png')
    image = pygame.transform.scale(image, (200, 200))

    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = Boss_act3.image
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.mask = pygame.mask.from_surface(self.image)


class WizardRus(pygame.sprite.Sprite):  # Маг 1 акта
    image = load_image('npc/wizardRus.png')
    image = pygame.transform.scale(image, (90, 90))

    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = WizardRus.image
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.canRun = False
        self.y = pos_y

    def update(self):
        if self.canRun:
            self.rect.y -= 15
            self.y -= 15
            if self.y <= -100:
                self.rect.y = -1000
        if player.y <= 800:
            self.canRun = True


class WizardRus_2(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__(all_sprites, wizardRus_2_group)
        image = load_image('npc/wizardRus.png')
        image = pygame.transform.scale(image, (110, 110))
        image = pygame.transform.flip(image, True, False)
        self.image = image
        self.rect = self.image.get_rect().move(x_pos, y_pos)


wizardRus = WizardRus(2000, 2000)


def act3_buttons():  # Создание кнопок для выбора ответа
    global task_text, difference, question, buttons, a, b, tm
    a = random.randint(0, 100)
    difference = random.randint(1, 4)
    b = difference - a
    if b < 0:
        question = f"{a}{b}"
    else:
        question = f"{a} + {b}"
    font_path = os.path.join("data/fonts", "Visitor Rus.ttf")
    font = pygame.font.Font(font_path, 50)
    task_text = font.render(question, False, (0, 0, 0))
    buttons = []
    for j in range(1, 5):
        buttons.append(
            Button(x - player.x + j * 150, y - player.y + 200, j))
    tm = 180
    screen.blit(font.render(str(tm // 60 + 1), False, (0, 0, 0)),
                (350, 0))


def results():  # Таблица результатов
    con = sqlite3.connect("data/bd.sqlite")
    cur = con.cursor()
    result1 = cur.execute(f"""SELECT time FROM player
            WHERE idSaves == {idSaves} and act != 0 ORDER BY 
            time""").fetchall()
    cur.execute(f"""DELETE from player where idSaves == {idSaves} and act 
    != 0""")

    con.commit()
    con.close()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif (event.type == pygame.KEYDOWN or event.type ==
                  pygame.MOUSEBUTTONDOWN):
                return
        screen.blit(load_image("camera-player/sybtit.png"), (0, 0))
        font_path = os.path.join("data/fonts", "Visitor Rus.ttf")

        font = pygame.font.Font(font_path, 50)
        text_1 = font.render("WIN", False, (255, 255, 255))
        text_2 = font.render("Your time:", False, (255, 255, 255))
        tm = float(sum([float(i[0]) for i in result1]))
        text_3 = font.render(f'{int(tm // 60)} min '
                             f'{int(tm - (tm // 60) * 60)} sec',
                             False, (255, 255, 255))
        screen.blit(text_1, (250, 50))
        screen.blit(text_2, (250, 110))
        screen.blit(text_3, (250, 170))
        pygame.display.flip()
        clock.tick(FPS)


def credits_screen():  # Субтитры
    j = 0
    sybtit = load_image('camera-player/sybtit.png')
    pygame.mixer.music.load("data/music/final_melody.ogg")
    pygame.mixer.music.set_volume(valueMusic)
    pygame.mixer.music.play(loops=-1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        screen.blit(sybtit, (0, -j))
        pygame.display.flip()

        j += 2
        if j >= 1750:
            return

        clock.tick(FPS)


def getResult(n):
    con = sqlite3.connect("data/bd.sqlite")
    cur = con.cursor()
    result = cur.execute(f"""SELECT act, time FROM player
                                    WHERE IdSaves == {n}""").fetchall()
    result = [i[0] for i in result]
    if '32' in result:
        act_loc = 'Act - 3 location - 3'
    elif '31' in result:
        act_loc = 'Act - 3 location - 2'
    elif '2' in result:
        act_loc = 'Act - 3 location - 1'
    elif '22' in result:
        act_loc = 'Act - 2 location - 3'
    elif '21' in result:
        act_loc = 'Act - 2 location - 2'
    elif '1' in result:
        act_loc = 'Act - 2 location - 1'
    elif '13' in result:
        act_loc = 'Act - 1 location - 4'
    elif '12' in result:
        act_loc = 'Act - 1 location - 3'
    elif '11' in result:
        act_loc = 'Act - 1 location - 2'
    else:
        act_loc = 'Act - 1 location - 1'
    return act_loc


def other_color2(cl1, cl2, cl3, cl4, cl5):  # Смена цвета кнопки в меню
    global t1, t2, t3, t4, t5
    font_path = os.path.join("data/fonts", "Visitor Rus.ttf")
    font = pygame.font.Font(font_path, 30)
    t1 = font.render(f"Сохранение 1: {getResult(1)}",
                     False, cl1)
    t2 = font.render(f"Сохранение 2: {getResult(2)}",
                     False, cl2)
    t3 = font.render(f"Сохранение 3: {getResult(3)}",
                     False, cl3)
    t4 = font.render(f"Сохранение 4: {getResult(4)}",
                     False, cl4)
    t5 = font.render(f"Сохранение 5: {getResult(5)}",
                     False, cl5)


def menuGet():  # Меню в начале
    global idSaves
    COLOR1 = (64, 64, 64)
    COLOR2 = (255, 0, 0)

    other_color2(COLOR2, COLOR1, COLOR1, COLOR1, COLOR1)
    colT = 1
    pygame.mixer.music.pause()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    colT -= 1
                    if colT == 0:
                        colT = 5
                        other_color2(COLOR1, COLOR1, COLOR1, COLOR1,
                                     COLOR2)
                    if colT == 1:
                        other_color2(COLOR2, COLOR1, COLOR1,
                                     COLOR1, COLOR1)
                    if colT == 2:
                        other_color2(COLOR1, COLOR2, COLOR1,
                                     COLOR1, COLOR1)
                    if colT == 3:
                        other_color2(COLOR1, COLOR1, COLOR2,
                                     COLOR1, COLOR1)
                    if colT == 4:
                        other_color2(COLOR1, COLOR1, COLOR1,
                                     COLOR2, COLOR1)

                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    colT += 1
                    if colT == 6:
                        colT = 1
                        other_color2(COLOR2, COLOR1, COLOR1,
                                     COLOR1, COLOR1)
                    if colT == 5:
                        other_color2(COLOR1, COLOR1, COLOR1, COLOR1,
                                     COLOR2)
                    if colT == 2:
                        other_color2(COLOR1, COLOR2, COLOR1,
                                     COLOR1, COLOR1)
                    if colT == 3:
                        other_color2(COLOR1, COLOR1, COLOR2,
                                     COLOR1, COLOR1)
                    if colT == 4:
                        other_color2(COLOR1, COLOR1, COLOR1,
                                     COLOR2, COLOR1)

                if (event.key == pygame.K_SPACE or
                        event.key == pygame.K_RETURN):
                    con = sqlite3.connect("data/bd.sqlite")
                    cur = con.cursor()
                    if colT == 1:
                        result = cur.execute("""SELECT act FROM player
                                WHERE IdSaves == 1""").fetchall()
                        idSaves = 1
                    elif colT == 2:
                        result = cur.execute("""SELECT act FROM player
                                WHERE IdSaves == 2""").fetchall()
                        idSaves = 2
                    elif colT == 3:
                        result = cur.execute("""SELECT act FROM player
                                WHERE IdSaves == 3""").fetchall()
                        idSaves = 3
                    elif colT == 4:
                        result = cur.execute("""SELECT act FROM player
                                WHERE IdSaves == 4""").fetchall()
                        idSaves = 4
                    else:
                        result = cur.execute("""SELECT act FROM player
                                WHERE IdSaves == 5""").fetchall()
                        idSaves = 5
                    result = [i[0] for i in result]
                    if '32' in result:
                        act3()
                        a3_location('m2')
                    elif '31' in result:
                        act3()
                        a3_location('m1')
                    elif '2' in result:
                        act3()
                    elif '22' in result:
                        act2()
                        a2_location('m2')
                    elif '21' in result:
                        act2()
                        a2_location('m1')
                    elif '1' in result:
                        act2()
                    elif '13' in result:
                        act1()
                        a1_location('m3')
                    elif '12' in result:
                        act1()
                        a1_location('m2')
                    elif '11' in result:
                        act1()
                        a1_location('m1')
                    else:
                        act1()
                    pygame.mixer.music.play(loops=-1)
                    con.close()
                    return

        screen.blit(t1, (100, 50))
        screen.blit(t2, (100, 130))
        screen.blit(t3, (100, 210))
        screen.blit(t4, (100, 290))
        screen.blit(t5, (100, 370))
        pygame.display.flip()
        clock.tick(FPS)


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


# Создание объектов всей игры
clock = pygame.time.Clock()
FPS = 60
# группы спрайтов
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
door_group = pygame.sprite.Group()
rectangle_group = pygame.sprite.Group()
button_group = pygame.sprite.Group()
word_group = pygame.sprite.Group()
sign_group = pygame.sprite.Group()
text_group = pygame.sprite.Group()
defense_group = pygame.sprite.Group()
apple_trees_group = pygame.sprite.Group()
apple_group = pygame.sprite.Group()
wizardRus_2_group = pygame.sprite.Group()
boss_Act3_group = pygame.sprite.Group()

time = datetime.datetime.now()
x, y = 0, 0
rect = Rectangle(20000, 20000, 0, 0, 10, 500, False, "objects/redrect.png")
img = load_image('objects/key.jpg')
img = pygame.transform.scale(img, (50, 50))
sign1 = Sign(120, 20000)
sign2 = Sign(658, 20000)
sign3 = Sign(120, 20000)
sign4 = Sign(658, 20000)
sign5 = Sign(120, 20000)
sign6 = Sign(658, 20000)

loc5 = 0
loc11 = 0
loc14 = 0

runi = -600
camera = Camera()
apples = []
tm = 0
difference = 0
valueMusic = 0.8

wizardRus_2 = WizardRus_2(1970, 20000)
door2 = Door(20000, 20000, 2, 1)
door3 = Door(20000, 20000, 2, 1)
chest = Chest(20000, 20000)
plat = Platform(20000, 20000)
pas = Pass(20000, 20000)
traveler = Traveler(20000, 20000)
idSaves = 0
time_rect = 0
image = ''
background = Background('maps/a1_m1.png', (4000, 2480))
boss_Act1 = Boss_act1(20000, 20000)
boss_Act2 = Boss_act2(20000, 20000)
boss_Act3 = Boss_act3(20000, 20000)

if __name__ == '__main__':  # Запуск программы
    pygame.init()
    pygame.display.set_caption('Entangled Tale')
    size = width, height = 800, 500
    screen = pygame.display.set_mode(size)
    start_screen()

    text1 = pygame.font.Font(os.path.join("data/fonts", "Visitor Rus.ttf"),
                             20).render('', False, (255, 255, 255))
    text2 = pygame.font.Font(os.path.join("data/fonts", "Visitor Rus.ttf"),
                             20).render('', False, (255, 255, 255))
    text3 = pygame.font.Font(os.path.join("data/fonts", "Visitor Rus.ttf"),
                             20).render('', False, (255, 255, 255))
    text4 = pygame.font.Font(os.path.join("data/fonts", "Visitor Rus.ttf"),
                             20).render('', False, (255, 255, 255))
    i = 0
    running = True
    while running:  # Основной цикл
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    menu([], '')
                if event.key == pygame.K_e and runi == -600:
                    runi = 300
            if event.type == pygame.KEYUP:
                player.stop()

        pygame.mixer.music.set_volume(valueMusic)
        if runi != -600:
            player.run = 9
        if runi < 0:
            player.run = 5
        if player.loc <= 5:
            screen.fill((2, 0, 0))
        elif 5 < player.loc <= 12:
            screen.fill((34, 177, 76))
        else:
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
        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)
        camera.update(player)
        wizardRus.update()
        all_sprites.draw(screen)
        if player.loc == 7:
            screen.blit(task_text, (x - player.x + 780, y - player.y + 160))
        if not player.key and pygame.sprite.collide_mask(player, chest):
            # Взаимодействие с сундуком
            font_path = os.path.join("data/fonts", "Visitor Rus.ttf")
            font = pygame.font.Font(font_path, 40)
            task_text = font.render("Нужен ключ!", False, (255, 255, 255))
            screen.blit(task_text, (300, 0))
        if pygame.sprite.collide_mask(player,
                                      traveler):  # Взаимодействие с нпс
            font_path = os.path.join("data/fonts", "Visitor Rus.ttf")
            font = pygame.font.Font(font_path, 25)
            if player.apples not in [5, 6]:
                task_text = font.render("Принеси мне 5 яблок, в обмен на инфор"
                                        "мацию.", False, (255, 255, 255))
                task_text2 = font.render('Они находятся рядом с 3-мя яблонями',
                                         False, (255, 255, 255))
            else:
                task_text = font.render(
                    "Выпей воды из речки, и ты станешь невидимым.", False,
                    (255, 255, 255))
                task_text2 = font.render(
                    'Это поможет тебе скрыться от стражника', False,
                    (255, 255, 255))
                player.apples = 6
            screen.blit(task_text, (180, 0))
            screen.blit(task_text2, (180, 40))
        if (not player.pas and pygame.sprite.collide_mask(player, pas) and
                player.loc == 6):  # Взаимодействие с автоматом
            font_path = os.path.join("data/fonts", "Visitor Rus.ttf")
            font = pygame.font.Font(font_path, 40)
            task_text = font.render("Нужна монета!", False, (255, 255, 255))
            screen.blit(task_text, (300, 0))
        player_group.draw(screen)
        if runi > -600:
            runi -= 1

        if player.loc == 2:
            i += 1
            if i % 40 == 0:
                letter = Letters(x - player.x + 2500,
                                 random.randint(y - player.y + 450,
                                                y - player.y + 660))
                word_group.add(letter)
            word_group.update()
            word_group.draw(screen)

        screen.blit(pygame.transform.scale(load_image("camera-player/run.png"),
                                           (40, 40)),
                    (5, 5))
        font_path = os.path.join("data/fonts", "Visitor Rus.ttf")
        if runi == -600:  # Активация ускорения
            txt = pygame.font.Font(font_path, 35).render("active", True,
                                                         (255, 0, 0))
            screen.blit(txt, (50, 0))
        else:
            txt = pygame.font.Font(font_path, 30).render(
                f"{(runi + 660) // 60}", True, (255, 0, 0))
            screen.blit(txt, (50, 5))

        if player.key:
            screen.blit(img, (750, 0))

        if player.apples != 6:
            for i in range(player.apples):
                screen.blit(img, (770 - i * 30, 0))

        if player.loc == 4:  # Босс 1 акта
            if 200 <= loc5 <= 1000 and loc5 % 200 == 0:
                try:
                    n = random.randint(-1, 3) * 200
                    while n == m:
                        n = random.randint(-1, 3) * 200
                    m = n
                except Exception:
                    m = random.randint(-1, 3) * 200
                rect.rect.x = 20000
                rect = Rectangle(x - player.x + m,
                                 y - player.y - 78, 0, 0, 450,
                                 519, False, "objects/warning rect.png")

            if 320 <= loc5 <= 1000 and loc5 % 200 == 130:
                boss_Act1.image = pygame.transform.scale(load_image('npc/wizard_physics_1.png'), (300, 200))
            if 340 <= loc5 <= 1000 and loc5 % 200 == 140:
                rect.rect.x = 20000
                rect = Rectangle(x - player.x + m,
                                 y - player.y - 95, 0, 0, 450,
                                 519, True, "objects/grayrect_1.png")
                image = 'objects/grayrect_1.png'
                time_rect = 0
            if image == 'objects/grayrect_1.png':
                if time_rect == 10:
                    rect.image = pygame.transform.scale(load_image('objects/grayrect_2.png'), (450, 519))
                    image = 'objects/grayrect_2.png'
                    time_rect = 0
            if image == 'objects/grayrect_2.png':
                if time_rect == 10:
                    rect.image = pygame.transform.scale(load_image('objects/grayrect_3.png'), (450, 519))
                    image = 'objects/grayrect_3.png'
                    time_rect = 0
            if image == 'objects/grayrect_3.png':
                if time_rect == 10:
                    rect.image = pygame.transform.scale(load_image('objects/grayrect_4.png'), (450, 519))
                    image = 'objects/grayrect_4.png'
                    time_rect = 0
            if 340 <= loc5 <= 1000 and loc5 % 200 == 150:
                boss_Act1.image = pygame.transform.scale(load_image('npc/wizard_physics.png'), (300, 200))

            if 980 <= loc5 <= 3000 and loc5 % 100 == 80:
                boss_Act1.image = pygame.transform.scale(load_image('npc/wizard_physics_2.png'), (300, 200))
            if 1000 <= loc5 <= 3000 and loc5 % 100 == 0:
                rect.rect.x = 20000
                Rectangle(x - player.x + 800,
                          y - player.y + random.randint(-100, 150), -3, 0, 100,
                          366, True, "objects/redrect.png")
            if 1000 <= loc5 <= 3005 and loc5 % 100 == 5:
                boss_Act1.image = pygame.transform.scale(load_image('npc/wizard_physics.png'), (300, 200))

            if 3180 <= loc5 <= 4140 and loc5 % 200 == 130:
                boss_Act1.image = pygame.transform.scale(load_image('npc/wizard_physics_4.png'), (300, 200))
            if 3200 <= loc5 <= 4000 and loc5 % 200 == 0:
                n = random.randint(-1, 3) * 200
                while n == m:
                    n = random.randint(-1, 3) * 200
                m = n
                rect.rect.x = 20000
                rect = Rectangle(x - player.x + m,
                                 y - player.y - 78, 0, 0, 450,
                                 519, False, "objects/warning rect.png")
            if 3200 <= loc5 <= 4140 and loc5 % 200 == 140:
                rect.rect.x = 20000
                rect = Rectangle(x - player.x + m,
                                 y - player.y - 95, 0, 0, 450,
                                 519, True, "objects/grayrect_1.png")
                time_rect = 0
                image = 'objects/grayrect_1.png'
            if 3200 <= loc5 <= 4150 and loc5 % 200 == 150:
                boss_Act1.image = pygame.transform.scale(load_image('npc/wizard_physics_3.png'), (300, 200))
            if loc5 == 4200:
                rect.rect.x = 20000
            if loc5 == 4400:
                boss_Act1.rect.x = 20000
                door = Door(x - player.x + 350, y - player.y + 150, 1, 1)
                player.loc = 5
            loc5 += 1
            time_rect += 1
            rectangle_group.update()
        if player.loc == 11:  # Босс 2 акта
            if loc11 <= 2000 and loc11 % 100 == 85:
                boss_Act2.image = pygame.transform.scale(load_image('npc/wizard_nature.png'), (200, 300))
            if loc11 <= 2000 and loc11 % 100 == 0:
                boss_Act2.image = pygame.transform.scale(load_image('npc/wizard_nature.png'), (200, 300))
                Rectangle(x - player.x + 800,
                          y - player.y + random.randint(-100, 200), -3, 0,
                          240, 60, True, "objects/greenrect2.png")
                Rectangle(x - player.x + 800,
                          y - player.y + random.randint(200, 450), -3, 0,
                          240, 60, True, "objects/greenrect2.png")
            if loc11 <= 2010 and loc11 % 100 == 10:
                boss_Act2.image = pygame.transform.scale(load_image('npc/wizard_nature_1.png'), (200, 300))

            if 2200 <= loc11 <= 3400 and loc11 % 100 == 85:
                boss_Act2.image = pygame.transform.scale(load_image('npc/wizard_nature_2.png'), (200, 300))
            if 2300 <= loc11 <= 3400 and loc11 % 100 == 0:
                Rectangle(x - player.x + random.randint(-100, 300),
                          y - player.y - 400, 0, 1, 60,
                          240, True, "objects/greenrect1.png")
                Rectangle(x - player.x + random.randint(300, 800),
                          y - player.y - 400, 0, 1, 60,
                          240, True, "objects/greenrect1.png")
            if 2300 <= loc11 <= 3410 and loc11 % 100 == 10:
                boss_Act2.image = pygame.transform.scale(load_image('npc/wizard_nature_3.png'), (200, 300))

            if 3700 <= loc11 <= 5400 and loc11 % 100 and loc11 % 100 == 85:
                boss_Act2.image = pygame.transform.scale(load_image('npc/wizard_nature.png'), (200, 300))
            if 3800 <= loc11 <= 5400 and loc11 % 100 == 0:
                boss_Act2.image = pygame.transform.scale(load_image('npc/wizard_nature.png'), (200, 300))
                Rectangle(x - player.x + 800,
                          y - player.y + random.randint(-100, 200), -3, 0,
                          240, 60, True, "objects/greenrect2.png")
                Rectangle(x - player.x - 300,
                          y - player.y + random.randint(200, 450), 3, 0,
                          240, 60, True, "objects/greenrect2.png")
            if 3800 <= loc11 <= 5410 and loc11 % 100 == 10:
                boss_Act2.image = pygame.transform.scale(load_image('npc/wizard_nature_1.png'), (200, 300))

            if loc11 == 5800:
                boss_Act2.rect.x = 20000
                door = Door(x - player.x + 350, y - player.y + 150, 1, 1)
                player.loc = 12
            loc11 += 1
            rectangle_group.update()

        if player.loc == 15:  # Босс 3 акта
            if loc14 == 1:
                boss_Act3 = Boss_act3(380, -220)
                boss_Act3_group.add(boss_Act3)
            if loc14 == 200:
                p = [random.randint(0, 600),
                     random.randint(0, 300)]
                background.update('maps/a3_m3.1.png', (2210, 1300))
                plat = Platform(x - player.x + p[0], y - player.y + p[1])
            elif loc14 == 400:
                boss_Act3.image = pygame.transform.scale(load_image('npc/wizard_1.png'), (200, 200))
                plat.rect.x = 20000
                background.update('maps/a3_m3.png', (2210, 1300))
                rect = Rectangle(-200, -200, 0, 0, 2000, 2000, True,
                                 "objects/damage_platform.jpg")
                plat = Platform(x - player.x + p[0], y - player.y + p[1])
            elif loc14 == 500:
                boss_Act3.image = pygame.transform.scale(load_image('npc/wizard.png'), (200, 200))
                plat.rect.x = 20000
                rect.rect.x = 20000
            elif loc14 == 600:
                act3_buttons()
            if 600 <= loc14 <= 780:
                tm -= 1
                font_path = os.path.join("data/fonts", "Visitor Rus.ttf")
                font = pygame.font.Font(font_path, 50)
                screen.blit(task_text, (300, 0))
                screen.blit(font.render(str(tm // 60 + 1), False, (0, 0, 0)),
                            (650, 0))
            if loc14 == 780:
                boss_Act3.image = pygame.transform.scale(load_image('npc/wizard.png'), (200, 200))
                for j in buttons:
                    if pygame.sprite.collide_mask(player,
                                                  j) and j.tip == difference:
                        for k in buttons:
                            k.rect.x = 20000
                            buttons = []
                        break
                else:
                    end_screen(32, False)
            if loc14 == 800:
                boss_Act3.image = pygame.transform.scale(load_image('npc/wizard.png'), (200, 200))

            if loc14 == 1000:
                p = [random.randint(0, 600),
                     random.randint(0, 300)]
                background.update('maps/a3_m3.1.png', (2210, 1300))
                plat = Platform(x - player.x + p[0], y - player.y + p[1])
            elif loc14 == 1200:
                boss_Act3.image = pygame.transform.scale(load_image('npc/wizard_1.png'), (200, 200))
                plat.rect.x = 20000
                background.update('maps/a3_m3.png', (2210, 1300))
                rect = Rectangle(-200, -200, 0, 0, 2000, 2000, True,
                                 "objects/damage_platform.jpg")
                plat = Platform(x - player.x + p[0], y - player.y + p[1])
            elif loc14 == 1300:
                boss_Act3.image = pygame.transform.scale(load_image('npc/wizard.png'), (200, 200))
                plat.rect.x = 20000
                rect.rect.x = 20000

            if 1400 <= loc14 <= 2000 and loc14 % 100 == 0:
                Rectangle(x - player.x + 1000,
                          y - player.y + random.randint(-50, 200), -3, 0,
                          random.randint(100, 300),
                          10, True, "objects/damage_platform.jpg")
                Rectangle(x - player.x - 500,
                          y - player.y + random.randint(200, 450), 3, 0,
                          random.randint(100, 300),
                          10, True, "objects/damage_platform.jpg")

            if loc14 == 2300:
                p = [random.randint(0, 600),
                     random.randint(0, 300)]
                background.update('maps/a3_m3.1.png', (2210, 1300))
                plat = Platform(x - player.x + p[0], y - player.y + p[1])
            elif loc14 == 2500:
                boss_Act3.image = pygame.transform.scale(load_image('npc/wizard_1.png'), (200, 200))
                plat.rect.x = 20000
                background.update('maps/a3_m3.png', (2210, 1300))
                rect = Rectangle(-200, -200, 0, 0, 2000, 2000, True,
                                 "objects/damage_platform.jpg")
                plat = Platform(x - player.x + p[0], y - player.y + p[1])
            elif loc14 == 2600:
                boss_Act3.image = pygame.transform.scale(load_image('npc/wizard.png'), (200, 200))
                plat.rect.x = 20000
                rect.rect.x = 20000
            elif loc14 == 2700:
                act3_buttons()
            if 2700 <= loc14 <= 2880:
                tm -= 1
                font_path = os.path.join("data/fonts", "Visitor Rus.ttf")
                font = pygame.font.Font(font_path, 50)
                screen.blit(task_text, (300, 0))
                screen.blit(font.render(str(tm // 60 + 1), False, (0, 0, 0)),
                            (650, 0))
            if loc14 == 2880:
                boss_Act3.image = pygame.transform.scale(load_image('npc/wizard.png'), (200, 200))
                for j in buttons:
                    if pygame.sprite.collide_mask(player,
                                                  j) and j.tip == difference:
                        for k in buttons:
                            k.rect.x = 20000
                            buttons = []
                        break
                else:
                    end_screen(32, False)
            if loc14 == 2900:
                boss_Act3.image = pygame.transform.scale(load_image('npc/wizard.png'), (200, 200))

            if 3200 <= loc14 <= 3700 and loc14 % 100 == 0:
                Rectangle(x - player.x + 1000,
                          y - player.y + random.randint(-50, 200), -3, 0,
                          random.randint(100, 300),
                          10, True, "objects/damage_platform.jpg")
                Rectangle(x - player.x - 500,
                          y - player.y + random.randint(200, 450), 3, 0,
                          random.randint(100, 300),
                          10, True, "objects/damage_platform.jpg")

            if 3700 <= loc14 <= 4200 and loc14 % 100 == 0:
                Rectangle(x - player.x - 500,
                          y - player.y + random.randint(-50, 200), 3, 0,
                          random.randint(100, 300),
                          10, True, "objects/damage_platform.jpg")
                Rectangle(x - player.x + 1000,
                          y - player.y + random.randint(200, 450), -3, 0,
                          random.randint(100, 300),
                          10, True, "objects/damage_platform.jpg")

            if loc14 == 4500:
                p = [random.randint(0, 600),
                     random.randint(0, 300)]
                background.update('maps/a3_m3.1.png', (2210, 1300))
                plat = Platform(x - player.x + p[0], y - player.y + p[1])
            elif loc14 == 4700:
                boss_Act3.image = pygame.transform.scale(load_image('npc/wizard_1.png'), (200, 200))
                plat.rect.x = 20000
                background.update('maps/a3_m3.png', (2210, 1300))
                rect = Rectangle(-200, -200, 0, 0, 2000, 2000, True,
                                 "objects/damage_platform.jpg")
                plat = Platform(x - player.x + p[0], y - player.y + p[1])
            elif loc14 == 4800:
                boss_Act3.image = pygame.transform.scale(load_image('npc/wizard.png'), (200, 200))
                plat.rect.x = 20000
                rect.rect.x = 20000
            elif loc14 == 4900:
                act3_buttons()
            if 4900 <= loc14 <= 5080:
                tm -= 1
                font_path = os.path.join("data/fonts", "Visitor Rus.ttf")
                font = pygame.font.Font(font_path, 50)
                screen.blit(task_text, (300, 0))
                screen.blit(font.render(str(tm // 60 + 1), False, (0, 0, 0)),
                            (650, 0))
            if loc14 == 5080:
                boss_Act3.image = pygame.transform.scale(load_image('npc/wizard.png'), (200, 200))
                for j in buttons:
                    if pygame.sprite.collide_mask(player,
                                                  j) and j.tip == difference:
                        for k in buttons:
                            k.rect.x = 20000
                            buttons = []
                        break
                else:
                    end_screen(32, False)
            if loc14 == 5100:
                boss_Act3.image = pygame.transform.scale(load_image('npc/wizard.png'), (200, 200))
            if 5400 <= loc14 <= 5900 and loc14 % 100 == 0:
                Rectangle(x - player.x + 1000,
                          y - player.y + random.randint(-50, 200), -3, 0,
                          random.randint(100, 300),
                          13, True, "objects/damage_platform.jpg")
                Rectangle(x - player.x - 500,
                          y - player.y + random.randint(200, 450), 3, 0,
                          random.randint(100, 300),
                          13, True, "objects/damage_platform.jpg")
            if 5900 <= loc14 <= 6400 and loc14 % 100 == 0:
                Rectangle(x - player.x - 500,
                          y - player.y + random.randint(-50, 200), 3, 0,
                          random.randint(100, 300),
                          13, True, "objects/damage_platform.jpg")
                Rectangle(x - player.x + 1000,
                          y - player.y + random.randint(200, 450), -3, 0,
                          random.randint(100, 300),
                          13, True, "objects/damage_platform.jpg")
            if loc14 == 6800:
                boss_Act3.rect.x = 20000
                door = Door(x - player.x + 100, y - player.y + 150, 3, 3)
                player.loc = 16

            loc14 += 1
            rectangle_group.update()
            boss_Act3_group.draw(screen)
            player_group.draw(screen)

        if player.loc == 3:  # Таблички 1 акта
            sign_group.update()
            for i in sign_group:
                if pygame.sprite.collide_mask(player, i):
                    screen.blit(
                        pygame.transform.scale(
                            load_image("objects/text_window.png"),
                            (600, 150)), (100, 0))
            screen.blit(text1, (110, 10))
            screen.blit(text2, (110, 40))
            screen.blit(text3, (110, 70))
            screen.blit(text4, (110, 100))
        button_group.update()
        door_group.draw(screen)
        if player.loc == 13:
            defense_group.draw(screen)
            apple_trees_group.draw(screen)
            apple_group.draw(screen)
        if player.task_text:
            screen.blit(player.task_text, (300, 0))
        pygame.display.flip()
        clock.tick(FPS)
