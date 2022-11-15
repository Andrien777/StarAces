import pygame as pg
from random import randint
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--width', default=800, help="Width of the screen", type=int)
parser.add_argument('--height', default=600, help="Height of the screen", type=int)
wh = parser.parse_args(sys.argv[1:])
WIDTH = wh.width
HEIGHT = wh.height
FPS = 60
cld = 0
clk = randint(100, 500)
pg.init()
pg.key.set_repeat(1000 // FPS)
scr = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Space Aces")
clock = pg.time.Clock()
score = 0
mode = 1
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (200, 200, 255)
running = True
end = False
inv = False
targ = [1500, 3000, 4500, 10000]
start = False
got = []
show = True
invclk = 0
invper = 30
background = BLACK
font = pg.font.Font("ModeX-LeB3.ttf", 46)
title = pg.font.Font("ModeX-LeB3.ttf", 120)
scr.fill(background)
pg.display.flip()
lives = 3
enemies = []
x = 0
y = (HEIGHT - 100) / 2
bullets = []
en_bull = []
while running:
    scr.fill(background)
    scr.blit(title.render("SPACE ACES", True, (255, 0, 0)), (50, 30))
    if show:
        scr.blit(font.render("PRESS SPACE TO START", True, (255, 0, 0)), (120, HEIGHT - 200))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                start = True
    if start:
        break
    if invper == 0:
        show = not show
        invper = 50
    invper -= 1
    pg.display.flip()
    clock.tick(FPS)
show = True
invper = 0
while running:
    scr.fill(background)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_r:
                lives = 3
                enemies = []
                bullets = []
                en_bull = []
                x = 0
                y = (HEIGHT - 100) / 2
                inv = False
                show = True
                invclk = 0
                invper = 0
                cld = 0
                clk = randint(500, 2000)
                end = False
                got = []
                score = 0
                mode = 1
            if event.key in (pg.K_w, pg.K_UP) and not end:
                y -= 6
                if y < 0:
                    y = 0
            if event.key in (pg.K_s, pg.K_DOWN) and not end:
                y += 6
                if y > HEIGHT - 115:
                    y = HEIGHT - 115
            if event.key in (pg.K_a, pg.K_LEFT) and not end:
                x -= 6
                if x < 0:
                    x = 0
            if event.key in (pg.K_d, pg.K_RIGHT) and not end:
                x += 6
                if x > WIDTH / 2 - 75:
                    x = WIDTH / 2 - 75
            if event.key == pg.K_SPACE and not end:
                if cld == 0:
                    if mode in (1, 3):
                        bullets.append({'x': x + 30, 'y': y + 7, 'y_v': 0})
                    elif mode == 2:
                        bullets.append({'x': x + 30, 'y': y, 'y_v': 0})
                    else:
                        bullets.append({'x': x + 30, 'y': y + 7, 'y_v': 0})
                    cld = (5 - mode) * 10
                    if mode == 3:
                        bullets.append({'x': x + 30, 'y': y + 7, 'y_v': 10})
                        bullets.append({'x': x + 30, 'y': y + 7, 'y_v': -10})
                    elif mode == 4:
                        bullets.append({'x': x + 30, 'y': y + 7, 'y_v': 5})
                        bullets.append({'x': x + 30, 'y': y + 7, 'y_v': -5})
                        bullets.append({'x': x + 30, 'y': y + 7, 'y_v': 15})
                        bullets.append({'x': x + 30, 'y': y + 7, 'y_v': -15})
    if clk == 0 and not end:
        enemies.append({'x': WIDTH, 'y': randint(0, HEIGHT - 140), 'x_v': -1 * randint(1, 5), 'y_v': randint(0, 5),
                        'frt': randint(20, 100), 'clk': 100})
        clk = randint(50, 500)
    for blt in bullets:
        if not end:
            blt['x'] += 50
            blt['y'] += blt['y_v']
        if mode != 2:
            pg.draw.rect(scr, WHITE, (blt['x'], blt['y'], 10, 2))
        else:
            pg.draw.rect(scr, WHITE, (blt['x'], blt['y'], 15, 15))
        if blt['x'] > WIDTH + 10:
            bullets.remove(blt)
    for i in enemies:
        if not end:
            i['x'] += i['x_v']
        if i['x'] <= 0:
            i['x'] = 0
            i['x_v'] *= -1
        elif i['x'] >= WIDTH - 40:
            i['x'] = WIDTH - 40
            i['x_v'] *= -1
        if not end:
            i['y'] += i['y_v']
        if i['y'] <= 0:
            i['y'] = 0
            i['y_v'] *= -1
        elif i['y'] >= HEIGHT - 140:
            i['y'] = HEIGHT - 140
            i['y_v'] *= -1
        if not end:
            i['clk'] -= 1
        if ((x <= i['x'] <= x + 50) or (x <= i['x'] + 40 <= x + 50)) and ((y <= i['y'] <= y + 15) or (
                y <= i['y'] + 40 <= y + 15)) and not inv:
            lives -= 1
            inv = True
            invclk = 100
            invper = 5
            show = True
        if i['clk'] == 0:
            en_bull.append({'x': i['x'], 'y': i['y'] + 20})
            i['clk'] = i['frt']
        for blt in bullets:
            if mode in (1, 3):
                if blt['x'] + 10 >= i['x'] and blt['x'] <= i['x'] + 40 and blt['y'] >= i['y'] and blt['y'] + 2 <= i['y'] + 40:
                    score += 100
                    bullets.remove(blt)
                    enemies.remove(i)
            elif mode == 4:
                if blt['x'] + 10 >= i['x'] and blt['x'] <= i['x'] + 40 and blt['y'] >= i['y'] and blt['y'] + 2 <= i['y'] + 40:
                    score += 100
                    enemies.remove(i)
            else:
                if blt['x'] + 15 >= i['x'] and blt['x'] <= i['x'] + 40 and blt['y'] >= i['y'] and blt['y'] + 15 <= i['y'] + 40:
                    score += 100
                    enemies.remove(i)
        pg.draw.rect(scr, (255, 255, 0), (i['x'], i['y'], 40, 40))
    for blt in en_bull:
        if not end:
            blt['x'] -= 7
        pg.draw.rect(scr, (230, 230, 0), (blt['x'], blt['y'], 10, 10))
        if blt['x'] < -10:
            en_bull.remove(blt)
        if blt['x'] >= x and blt['x'] + 5 <= x + 50 and blt['y'] >= y and blt['y'] + 5 <= y + 15 and not inv:
            lives -= 1
            inv = True
            invclk = 100
            invper = 5
            show = True
    if cld != 0:
        cld -= 1
    clk -= 1
    if score > 0 and score % 1000 == 0 and score not in got:
        lives += 1
        got.append(score)
    if lives == 0:
        end = True
    if show:
        pg.draw.rect(scr, RED, (x, y, 50, 15))
    if mode < 4:
        if not end and score >= targ[mode - 1]:
            mode += 1
    if inv and not end:
        invclk -= 1
        invper -= 1
        if invper == 0:
            show = not show
            invper = 5
        if invclk == 0:
            inv = False
            show = True
    pg.draw.rect(scr, (200, 200, 200), (0, HEIGHT - 100, WIDTH, 100))
    for i in range(lives):
        pg.draw.rect(scr, RED, (10 + i * 20, HEIGHT - 75, 15, 40))
    if mode == 1:
        pg.draw.rect(scr, WHITE, (WIDTH / 2, HEIGHT - 75, 5, 40))
    elif mode == 2:
        pg.draw.rect(scr, WHITE, (WIDTH / 2 - 15, HEIGHT - 75, 30, 30))
    elif mode == 3:
        pg.draw.rect(scr, WHITE, (WIDTH / 2 - 7, HEIGHT - 75, 5, 40))
        pg.draw.rect(scr, WHITE, (WIDTH / 2, HEIGHT - 75, 5, 40))
        pg.draw.rect(scr, WHITE, (WIDTH / 2 + 7, HEIGHT - 75, 5, 40))
    else:
        pg.draw.rect(scr, WHITE, (WIDTH / 2 - 14, HEIGHT - 75, 5, 40))
        pg.draw.rect(scr, WHITE, (WIDTH / 2 - 7, HEIGHT - 75, 5, 40))
        pg.draw.rect(scr, WHITE, (WIDTH / 2, HEIGHT - 75, 5, 40))
        pg.draw.rect(scr, WHITE, (WIDTH / 2 + 14, HEIGHT - 75, 5, 40))
        pg.draw.rect(scr, WHITE, (WIDTH / 2 + 7, HEIGHT - 75, 5, 40))
    scr.blit(font.render(str(score), False, BLACK), (WIDTH - 100, HEIGHT - 80))
    if end:
        scr.blit(font.render("Game Over!", False, RED), (WIDTH / 2 - 100, HEIGHT / 2 - 50))
    clock.tick(FPS)
    pg.display.flip()
