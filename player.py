import pygame


class Player:
    def __init__(self, width, height):
        self.image = pygame.image.load('player.png')
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.pos = [width, height]
        self.to = [0, 0]
        self.angle = 0
        self.life_count = 100
        self.is_invincible = False

    def goto(self, x, y):
        self.to[0] += x
        self.to[1] += y
        print(self.to)

    def draw(self, screen):
        if self.to == [-1, -1]:
            self.angle = 45
        elif self.to == [-1, 0]:
            self.angle = 90
        elif self.to == [-1, 1]:
            self.angle = 135
        elif self.to == [0, 1]:
            self.angle = 180
        elif self.to == [1, 1]:
            self.angle = -135
        elif self.to == [1, 0]:
            self.angle = -90
        elif self.to == [1, -1]:
            self.angle = -45
        elif self.to == [0, -1]:
            self.angle = 0

        rotated_image = pygame.transform.rotate(self.image, self.angle)
        calibpos = (self.pos[0] - rotated_image.get_width() / 2, self.pos[1] - rotated_image.get_height() / 2)
        screen.blit(rotated_image, calibpos)

    def update(self, dt, screen):
        width, height = screen.get_size()
        self.pos[0] = (self.pos[0] + self.to[0] * dt)  # x좌표
        self.pos[1] = (self.pos[1] + self.to[1] * dt)  # y좌표

        self.pos[0] = min(max(self.pos[0], 32), width - 32)
        self.pos[1] = min(max(self.pos[1], 32), height - 32)

    def set_image(self, image):
        self.image = image
