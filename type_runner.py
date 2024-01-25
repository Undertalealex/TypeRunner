# ### Developer: Shamaev Aleksandr Evgenievich

import string
import random
import pygame
import pygame._freetype

# Props
map_size = (16, 16)  # (x,y) - map size ### default: (22,14)

tick_rate = 0.05  # 20 times per sec ### default: 0.1

wind_pixel = 20
wind_pixel_border = 4

# Props evaluated
wind_width = (map_size[0] + 2) * wind_pixel
wind_height = (map_size[1] + 2) * wind_pixel
wind_fps = int(1 / tick_rate)

# Pygame
pygame.init()

color_black = (0, 0, 0)
color_white = (255, 255, 255)
color_green = (0, 255, 0)
color_blue = (0, 0, 255)
color_yellow = (255, 255, 0)

game_font = pygame.freetype.SysFont("Courier", 24)

wind = pygame.display.set_mode((wind_width, wind_height))
pygame.display.set_caption("Pixel-Pong")
wind.fill(color_black)
clock = pygame.time.Clock()


def colorize(x: int, y: int, color: tuple = color_white):
    pygame.draw.rect(wind, color,
                     [x * wind_pixel + wind_pixel_border, y * wind_pixel + wind_pixel_border,
                      wind_pixel - wind_pixel_border,
                      wind_pixel - wind_pixel_border], 0)


def color_at(x: int, y: int):
    global wind
    return wind.get_at((x * wind_pixel + wind_pixel_border, y * wind_pixel + wind_pixel_border))


for x in range(map_size[0] + 2):
    for y in range(map_size[1] + 2):
        # grid borders colorize
        if (x == 0 or x == map_size[0] + 1) or (y == 0 or y == map_size[1] + 1):
            colorize(x, y, color=color_yellow)

clearer = dict()


def text(msg: str, x, y):
    if (x, y) in clearer:
        last = clearer[(x, y)]
        pygame.draw.rect(wind, color_black, [last[0], last[1], last[2], last[3]], 0)
    clearer[(x, y)] = game_font.render_to(wind, (x, y), msg, color_white)


def colorize_rect(x0, y0, lx: int, ly: int, **ps):
    if lx == 0 and ly == 0:
        return
    for x in range(lx):
        colorize(x0 + x, y0, **ps)
        colorize(x0 + x, y0 + (ly - 1), **ps)
    for y in range(ly):
        colorize(x0, y0 + y, **ps)
        colorize(x0 + (lx - 1), y0 + y, **ps)


end = False
center = (map_size[0] // 2, map_size[1] // 2)
p = list(center)
colorize(*p, color_green)

target = []
possible = list(string.ascii_lowercase)


def update():
    global target
    random.shuffle(possible)
    target = possible[0:4]
    text(target[0], center[0] * wind_pixel, wind_pixel)
    text(target[1], map_size[0] * wind_pixel, center[1] * wind_pixel)
    text(target[2], center[0] * wind_pixel, map_size[1] * wind_pixel)
    text(target[3], wind_pixel, center[1] * wind_pixel)


update()


def can_move(idx: int) -> bool:
    global p
    if idx == 0:
        new_pos = (p[0], p[1] - 1)
    elif idx == 1:
        new_pos = (p[0] + 1, p[1])
    elif idx == 2:
        new_pos = (p[0], p[1]+1)
    elif idx == 3:
        new_pos = (p[0] - 1, p[1])
    else:
        raise Exception('WHAT')
    return color_at(*new_pos) != (*color_blue, 255)


def move(idx: int):
    global p
    if idx == 0:
        colorize(*p, color_blue)
        p[1] = p[1] - 1
        colorize(*p, color_green)
    elif idx == 1:
        colorize(*p, color_blue)
        p[0] = p[0] + 1
        colorize(*p, color_green)
    elif idx == 2:
        colorize(*p, color_blue)
        p[1] = p[1] + 1
        colorize(*p, color_green)
    elif idx == 3:
        colorize(*p, color_blue)
        p[0] = p[0] - 1
        colorize(*p, color_green)


while not end:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end = True
        if event.type == pygame.KEYDOWN:
            if chr(event.key) in target:
                idx = target.index(chr(event.key))
                if can_move(idx):
                    move(idx)
                    update()

    # render
    pygame.display.flip()
    ms = clock.tick(wind_fps)

pygame.quit()
