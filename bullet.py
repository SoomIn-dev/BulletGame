import pygame


class Bullet:
    def __init__(self, x, y, to_x, to_y, type_text):
        self.pos = [x, y]
        self.to = [to_x, to_y]
        self.radius = 8
        self.color = (190, 0, 0)
        self.type = type_text

    def update_and_draw(self, dt, screen):
        width, height = screen.get_size()
        self.pos[0] = (self.pos[0] + dt * self.to[0]) % width
        self.pos[1] = (self.pos[1] + dt * self.to[1]) % height

        if self.type == "circle":
            pygame.draw.circle(screen, self.color, self.pos, self.radius)
        elif self.type == "polygon":
            pygame.draw.polygon(screen, self.color,
                                [(self.pos[0], self.pos[1]), (self.pos[0] - self.radius * 2, self.pos[1]),
                                 (self.pos[0] - self.radius, self.pos[1] - self.radius * 2)], 0)
        elif self.type == "rect":
            pygame.draw.rect(screen, self.color, [self.pos[0], self.pos[1], self.radius * 2, self.radius * 2], 0)

