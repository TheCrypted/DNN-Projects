import pygame


class Ball:
    def __init__(self, rad, velocity, pos):
        self.rad = rad
        self.vel_x, self.vel_y = velocity
        self.pos_x, self.pos_y = pos
        self.acc = (2, 3)

    def update(self):
        # self.vel_x += self.acc[0]
        # self.vel_y += self.acc[1]

        self.pos_x += self.vel_x
        self.pos_y += self.vel_y

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (self.pos_x, self.pos_y), self.rad)