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


is_saved = False
rank = []

# rank.txt 파일을 읽기 모드로 열어 파일 안의 점수들을 리스트 형태로 가져오기
with open("rank.txt", "r") as f:
    for line in f:
        rank.append(float(line))

# 점수 리스트 정렬
rank.sort(reverse=True)

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

# 시작 전 3초 딜레이
time.sleep(3)
clock.tick(FPS)

invincible_cnt = 12
x = 0
# 순위에 랭크되었는지 확인하는 변수
ranked = False
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

            # random 을 이용하여 총알 모양 설정
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
    # 플레이어의 x, y 좌표에 따라 배경 이동
    bg_x -= dt * 0.02 * player.to[0]
    bg_y -= dt * 0.02 * player.to[1]

    pygame.draw.rect(screen, (255, 0, 0), [620, 10, 300, 30])
    # 플레이어의 생명력을 막대로 초록색 막대로 표시
    pygame.draw.rect(screen, (0, 255, 0), [620, 10, player.life_count * 3, 30])

    player.update(dt, screen)
    player.draw(screen)

    for b in bullets:
        b.update_and_draw(dt, screen)

    txt = f"Time: {playtime / 1000:.1f}, Bullets: {len(bullets)}, Life: {player.life_count} / 100"
    draw_text(txt, 32, (10, 10), (255, 255, 255))

    if gameover:
        time_txt = str(playtime / 1000)
        # 랭크가 저장되지 않았다면 랭크를 10위까지 저장
        if not is_saved:
            rank.append(playtime / 1000)
            rank.sort(reverse=True)
            print(rank)
            is_saved = True
            with open("rank.txt", "w") as f:
                for i in range(len(rank)):
                    if i < 10:
                        f.write(str(rank[i]) + "\n")
                        if rank[i] == playtime / 1000:
                            print('test')
                            ranked = True
        txt = "GAME OVER"
        draw_text(txt, 100, (WIDTH / 2 - 300, HEIGHT / 2 - 10), (255, 255, 255))
        color = (255, 255, 255)
        # 플레이타임이 순위에 랭크되었다면 플레이타임 표시 색깔을 노란색으로 변경
        if ranked:
            color = (190, 190, 0)
        draw_text(time_txt, 70, (WIDTH / 2 - 150, HEIGHT / 2 + 100), color)

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

                    # 총알의 모양에 따라 깎이는 생명력이 다르게
                    if b.type == "circle":
                        cnt = 10
                    elif b.type == "polygon":
                        cnt = 20
                    elif b.type == "rect":
                        cnt = 40

                    # 플레이어의 생명력을 깎을 점수만큼 깎는다.
                    if player.life_count >= cnt:
                        player.life_count -= cnt
                    # 플레이어의 생명력이 0 밑으로 떨어지면 0으로 설정
                    else:
                        player.life_count = 0

                    # 무적상태 활성화
                    player.is_invincible = True

                if player.life_count <= 0:
                    gameover = True
                    # 우주선이 터지는 느낌의 이미지로 플레이어 이미지 변경
                    player.set_image(pygame.transform.scale(pygame.image.load('player_bomb.png'), (64, 64)))
                    # 배경음악 중지
                    pygame.mixer.music.stop()
