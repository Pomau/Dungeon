import pygame
import sys
import os
import random
from math import floor
import time
FPS = 50
# размеры окна:
x, y = 800, 500
size = width, height = x, y
clock = pygame.time.Clock()
toch = []
kol_mobov = 0
on = 0
kol_m = 3


def terminate():
    pygame.quit()
    sys.exit()


# Загрузка изображений
def load_image(name, colorkey=None):
    fullname = name
    image = pygame.image.load(fullname).convert()
    # colorkey цвет заднего фона
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# Загрузка уровня
def load_level(filename):
    filename = filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('W')
    return list(map(lambda x: x.ljust(max_width, 'W'), level_map))


# Заставка
def start_screen():
    intro_text = []

    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


# Генерация уровня
def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                # Дорога
                Tile('road', x, y)
                if (level[y][x + 1] != '#' and level[y][x - 1] != '#' and
                    level[y + 1][x] != '#' and level[y - 1][x] != '#'):
                    toch.append((x, y))
            elif level[y][x] == '#':
                # Стены
                id = 0
                if y == 12:
                    y = 12
                if y > 0 and level[y - 1][x] == '.' and level[y][x - 1] == '.':
                    id = 9
                elif y > 0 and level[y - 1][x] == '.' and level[y][x+ 1] == '.':
                    id = 8
                elif y > 0 and level[y - 1][x] == '.':
                    id = 0
                elif level[y + 1][x] == '.' and level[y][x + 1] == '.':
                    id = 10
                elif level[y + 1][x] == '.' and level[y][x - 1] == '.':
                    id = 11
                elif y < len(level) - 1 and level[y + 1][x] == '.':
                    id = 1
                elif x > 0 and y > 0 and level[y][x -1] == '#' and level[y - 1][x] == '#':
                    id = 2
                elif x > 0 and y < len(level) - 1 and level[y + 1][x] == '#' and level[y][x - 1] == '#':
                    id = 4
                elif x > 0 and level[y][x - 1] == '.':
                    id = 3
                elif x < len(
                        level[y]
                ) - 1 and y > 0 and level[y][x +
                                             1] == '#' and level[y -
                                                                 1][x] == '#':
                    id = 5
                elif x < len(level[y]) - 1 and y < len(
                        level
                ) - 1 and level[y + 1][x] == '#' and level[y][x + 1] == '#':
                    id = 7
                elif x < len(level[y]) - 1 and level[y][x + 1] == '.':
                    id = 6
                else:
                    id = 12
                Tile('block', x, y, id)
            elif level[y][x] == '@':
                # Человек
                Tile('road', x, y)
                x1 = x
                y1 = y
            else:
                # Пустота
                Tile('black', x, y)
    # вернем игрока, а также размер поля в клетках
    return x, y


# Блоки
class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, index=-1):
        if tile_type != 'block':
            super().__init__(tiles_group, all_sprites)
        else:
            super().__init__(tiles_group, all_sprites, blocker)
        if index == -1:
            index = random.randint(0, len(tile_images[tile_type]) - 1)
        self.image = tile_images[tile_type][index]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(tile_width * pos_x,
                                               tile_height * pos_y)
        self.type1 = tile_type


# Игрок
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image[0]
        self.mask = pygame.mask.from_surface(player_image[5])
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15,
                                               tile_height * pos_y + 5)
        self.nx = tile_width * pos_x + 15
        self.ny = tile_height * pos_y + 5
        self.x = tile_width * pos_x + 15
        self.y = tile_height * pos_y + 5
        self.zd = 5
        self.ub = 0


# Монстр
class Mob(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(mobs_group, all_sprites)
        self.image = mob_image[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15,
                                               tile_height * pos_y + 5)
        self.x = tile_width * pos_x
        self.y = tile_height * pos_y
        self.play_x = self.x
        self.play_y = self.y
        self.ind = 0
        self.pol = 0
        self.zd = 3
        self.online = 0

# Камера
class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy


    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)

# Вывод здоровья
def zdorovie(player):
    for i in range(player.zd):
        fon = pygame.transform.scale(bonus_image[0], (21, 20))
        screen.blit(fon, (i * 21, 0))


shag1 = 1
shag_mob = 1

# Генерация монстров
def mobs_ran(toch, player):
    global kol_mobov, kol_m
    kol_mobov = kol_m
    for i in range(kol_m):
        x = random.randint(0, len(toch) - 1)
        e = Mob(toch[x][0], toch[x][1])

# Основная функция
def run():
    global toch, kol_mobov, on
    # Генерация уровня
    level = load_level('one.txt')
    max1 = len(level[0])
    for i in range(5):
        level.insert(0, 'W' * max1)
    for i in range(5):
        level.insert(len(level), 'W' * max1)
    for i in range(len(level)):
        level[i] = 'W' * 5 + level[i] + 'W' * 5
    level_x, level_y = generate_level(level)
    x = random.randint(0, len(toch) - 1)
    player = Player(toch[x][0], toch[x][1])
    camera.update(player)
    # обновляем положение всех спрайтов
    mobs_ran(toch, player)
    for sprite in all_sprites:
        camera.apply(sprite)
    all_sprites.draw(screen)
    zdorovie(player)
    pygame.display.flip()
    running = True
    d = 0
    p = 0
    op1 = []
    inr = 0
    imob = 0
    zdorov = 0
    shagat = 0
    najat = 0
    while running:
        screen.fill((0,0,0))
        # Управление
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                on = 1
            if event.type == pygame.KEYUP:
                if op1.count(event.key) != 0:
                    op1.remove(event.key)
            if event.type == pygame.KEYDOWN:
                op1.append(event.key)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if najat < 100:
                    continue
                for mob in mobs_group:
                    najat = 0
                    if (abs(mob.x / 50 - player.x / 50) <= 0.5
                        and abs(mob.y / 50 - player.y / 50) <= 0.5):
                        mob.zd -= 1
                    if mob.online == 0 and mob.zd == 0:
                        mob.online = 1
                        player.ub += 1
                        kol_mobov -= 1
                        if player.ub % 3 == 0:
                            player.zd = min(5, player.zd + 1)
                        mob.image = mob_image[4]
                        all_sprites.draw(screen)
                        all_sprites.update()
                        zdorovie(player)
                        pygame.display.flip()
        zdorov = (zdorov + 1) % 400
        najat += 1
        if kol_mobov == 0:
            running = False
            break
        # Нажатые команды игроком
        for op in op1:
            if op in [100, 97, 119, 115] and inr == 0:
                shagat += 1
                if shagat % 50 == 0:
                    d = (d + 1) % 2
                shag = shag1
                if op == 100:
                    player.rect.x += shag
                    player.x += shag
                    p = 0
                    os = 0
                    for sprite in blocker:
                        if pygame.sprite.collide_mask(sprite, player):
                            os = 1
                    if os == 1:
                        player.rect.x -= shag
                        player.x -= shag
                elif op == 97:
                    p = 2
                    os = 0
                    player.rect.x -= shag
                    player.x -= shag
                    for sprite in blocker:
                        if pygame.sprite.collide_mask(sprite, player):
                            os = 1
                    if os == 1:
                        player.rect.x += shag
                        player.x += shag
                elif op == 119:
                    os = 0
                    player.rect.y -= shag
                    player.y -= shag
                    for sprite in blocker:
                        if pygame.sprite.collide_mask(sprite, player):
                            os = 1
                    if os == 1:
                        player.rect.y += shag
                        player.y += shag
                elif op == 115:
                    os = 0
                    player.rect.y += shag
                    player.y += shag
                    for sprite in blocker:
                        if pygame.sprite.collide_mask(sprite, player):
                            os = 1
                    if os == 1:
                        player.rect.y -= shag
                        player.y -= shag

                player.image = player_image[d + p]
                camera.update(player)
                # обновляем положение всех спрайтов
                online = 0
                for sprite in all_sprites:
                    camera.apply(sprite)
        # Мобы реакции
        for mob in mobs_group:
            if mob.online == 1000:
                continue
            if mob.online >= 1:
                mob.online += 1
                if mob.online == 1000:
                    mob.image = mob_image[5]
                    all_sprites.draw(screen)
                    all_sprites.update()
                    zdorovie(player)
                    pygame.display.flip()
                continue
            if abs(mob.x / 50 - player.x / 50) <= 0.5 and abs(
                    mob.y // 50 - player.y // 50) < 5:
                os = 0
                for i in range(
                        min(mob.y // 50, player.y // 50) + 1,
                        max(mob.y // 50, player.y // 50)):
                    if level[i][mob.x // 50] == '#':
                        os = 1
                if os == 0:
                    mob.play_y = player.y
            elif abs(mob.y / 50 - player.y / 50) <= 0.5 and abs(
                    mob.x // 50 - player.x // 50) < 5:
                os = 0
                for i in range(
                        min(mob.x // 50, player.x // 50) + 1,
                        max(mob.x // 50, player.x // 50)):
                    if level[mob.y // 50][i] == '#':
                        os = 1
                if os == 0:
                    mob.play_x = player.x
            if zdorov == 0 and (abs(mob.x / 50 - player.x / 50) <= 0.5
                                and abs(mob.y / 50 - player.y / 50) <= 0.5):
                player.zd -= 1
                if player.zd == 0:
                    player.image = player_image[4]
                    all_sprites.draw(screen)
                    all_sprites.update()
                    fon = pygame.transform.scale(
                        load_image('Lost.png', -1), (width, height))
                    screen.blit(fon, (0, 0))
                    pygame.display.flip()
                if player.zd == 0:
                    time.sleep(5)
                    running = False
                    on = 1
                    break
            if (floor(mob.play_x) != floor(mob.x)
                    or floor(mob.play_y) != floor(mob.y)) and imob == 0:
                if mob.play_x != mob.x:
                    if mob.x > mob.play_x:
                        mob.x -= shag_mob
                        mob.rect.x -= shag_mob
                        mob.pol = 2
                    else:
                        mob.x += shag_mob
                        mob.rect.x += shag_mob
                        mob.pol = 0
                else:
                    if mob.y > mob.play_y:
                        mob.rect.y -= shag_mob
                        mob.y -= shag_mob
                    else:
                        mob.rect.y += shag_mob
                        mob.y += shag_mob
                mob.ind = (mob.ind + 1) % 2
                mob.image = mob_image[mob.ind + mob.pol]
        all_sprites.draw(screen)
        all_sprites.update()
        zdorovie(player)
        pygame.display.flip()


# инициализация Pygame:
pygame.init()

# screen — холст, на котором нужно рисовать:
screen = pygame.display.set_mode(size)

# формирование кадра:
# команды рисования на холсте
# ...

tile_images = {
    # Дорога
    'road': [
        load_image('grass1.png'),
        load_image('grass2.png'),
        load_image('grass3.png'),
        load_image('grass4.png')
    ],
# Пустота
    'black': [load_image('black.png')],
# Границы
    'block': [
        load_image('block_niz.png'),
        load_image('block_verx.png'),
        load_image('sp_niz.png'),
        load_image('sp_ser.png'),
        load_image('sp_verx.png'),
        load_image('sl_niz.png'),
        load_image('sl_ser.png'),
        load_image('sl_verx.png'),
        load_image('block_niz_dor_sl.png'),
        load_image('block_niz_dor_sp.png'),
        load_image('block_verx_dor_sl.png'),
        load_image('block_verx_dor_sp.png'),
        load_image('black.png')
    ]
}
# Игрок
player_image = [
    load_image('mario1.png', -1),
    load_image('mario2.png', -1),
    load_image('mario3.png', -1),
    load_image('mario4.png', -1),
    load_image('mario5.png', -1),
    load_image('mask1.png', -1),
    load_image('mask2.png', -1)
]
# Моб
mob_image = [
    load_image('ad1.png', -1),
    load_image('ad2.png', -1),
    load_image('ad3.png', -1),
    load_image('ad4.png', -1),
    load_image('ad5.png', -1),
    load_image('ad6.png', -1)
]

# Жизни
bonus_image = [load_image('zdoro.png', -1)]

# Размер блока
tile_width = tile_height = 50

start_screen()
# Уровень
while on == 0:
    print(kol_m)
    # основной персонаж
    player = None

    # группы спрайтов
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    mobs_group = pygame.sprite.Group()
    blocker = pygame.sprite.Group()

    camera = Camera()
    run()
    kol_m += 1
# завершение работы:
pygame.quit()
