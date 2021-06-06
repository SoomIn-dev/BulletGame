import time
import math

import pygame
import random as rnd

from bullet import Bullet
from player import Player


def collision(obj1, obj2):
    dist = math.sqrt((obj1.pos[0] - obj2.pos[0]) ** 2 + (obj1.pos[1] - obj2.pos[1]) ** 2)
    return dist < 20


def draw_text(txt, size, pos, color):
    font = pygame.font.Font('freesansbold.ttf', size)
    r = font.render(txt, True, color)
    screen.blit(r, pos)


pygame.init()
WIDTH, HEIGHT = 1000, 800

clock = pygame.time.Clock()
FPS = 60

pygame.display.set_caption("총알 피하기")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

player = Player(WIDTH / 2, HEIGHT / 2)

bg_image = pygame.image.load('bg.jpg')
bg_x = 0
bg_y = 0

bullets = []
time_for_adding_bullets = 0
time_for_invincible = 0
playtime = 0

for i in range(10):
    bullets.append(Bullet(0, rnd.random() * HEIGHT, rnd.random() - 0.5, rnd.random() - 0.5, "circle"))

gameover = False

# 총알에 맞았을 때 효과음 객체 생성
hit_sound = pygame.mixer.Sound('hit.wav')

pygame.mixer.music.load('bgm.wav')
pygame.mixer.music.play(-1)

time.sleep(3)
clock.tick(FPS)


invincible_cnt = 12
x = 0
running = True
while running:

    dt = clock.tick(FPS)

    if not gameover:
        playtime += dt
        time_for_adding_bullets += dt
        time_for_invincible += dt
        if time_for_adding_bullets > 3000:
            percent = rnd.randrange(1, 101)
            type_text = "circle"

            if 1 <= percent <= 30:
                type_text = "polygon"
            elif 31 <= percent <= 50:
                type_text = "rect"

            bullets.append(Bullet(0, rnd.random() * HEIGHT, rnd.random() - 0.5, rnd.random() - 0.5, type_text))
            time_for_adding_bullets -= 3000

        if time_for_invincible > 250:
            # 1초마다 실행
            if player.is_invincible:
                # 플레이어가 무적일 때 무적 카운트 1개씩 제거
                invincible_cnt -= 1

                # 무적상태일 때 플레이어 반짝이는 모션
                if invincible_cnt % 2 == 0:
                    player.set_image(pygame.transform.scale(pygame.image.load('player.png'), (64, 64)))
                else:
                    player.set_image(pygame.transform.scale(pygame.image.load('player_glow.png'), (64, 64)))

                # 무적 카운트가 0개일 때 무적상태 해제
                if invincible_cnt == 0:
                    player.is_invincible = False
                    invincible_cnt = 12

            time_for_invincible -= 250

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.goto(-1, 0)
            elif event.key == pygame.K_RIGHT:
                player.goto(1, 0)
            elif event.key == pygame.K_UP:
                player.goto(0, -1)
            elif event.key == pygame.K_DOWN:
                player.goto(0, 1)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.goto(1, 0)
            elif event.key == pygame.K_RIGHT:
                player.goto(-1, 0)
            elif event.key == pygame.K_UP:
                player.goto(0, 1)
            elif event.key == pygame.K_DOWN:
                player.goto(0, -1)

    screen.fill((0, 0, 0))
    screen.blit(bg_image, (bg_x, bg_y))
    bg_x -= dt * 0.02 * player.to[0]
    bg_y -= dt * 0.02 * player.to[1]

    player.update(dt, screen)
    player.draw(screen)

    for b in bullets:
        b.update_and_draw(dt, screen)

    txt = f"Time: {playtime / 1000:.1f}, Bullets: {len(bullets)}, Life: {player.life_count} / 100"
    draw_text(txt, 32, (10, 10), (255, 255, 255))

    if gameover:
        txt = "GAME OVER"
        draw_text(txt, 100, (WIDTH / 2 - 300, HEIGHT / 2 - 10), (255, 255, 255))

    pygame.display.update()

    for b in bullets:
        if collision(player, b):
            # 플레이어가 무적이 아닐 때 실행
            if not player.is_invincible:

                # 비행기가 총알에 맞았을 때 효과음 추가
                pygame.mixer.Sound.play(hit_sound)

                # 플레이어의 생명령이 0 이상일 때
                if player.life_count > 0:
                    # 플레이어 생명력 총알의 모양에 따라 차감
                    cnt = 0

                    if b.type == "circle":
                        cnt = 10
                    elif b.type == "polygon":
                        cnt = 20
                    elif b.type == "rect":
                        cnt = 40

                    # 무적상태 활성화
                    if player.life_count >= cnt:
                        player.life_count -= cnt
                    else:
                        player.life_count = 0

                    player.is_invincible = True

                if player.life_count <= 0:
                    gameover = True
                    # 우주선이 터지는 느낌의 이미지로 플레이어 이미지 변경
                    player.set_image(pygame.transform.scale(pygame.image.load('player_bomb.png'), (64, 64)))
                    pygame.mixer.music.stop()

time.sleep(2)
