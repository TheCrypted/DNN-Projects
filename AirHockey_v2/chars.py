import math

import pygame


class Ball:
    def __init__(self, rad, velocity, pos):
        self.rad = rad
        self.vel_x, self.vel_y = velocity
        self.original_vel = velocity
        self.pos_x, self.pos_y = pos
        self.acc = (2, 3)

    def update(self, screen_dim, paddles):
        self.pos_x += self.vel_x
        self.pos_y += self.vel_y
        self.handle_collision(screen_dim, paddles)

    def handle_collision(self, screen_dim, paddles):
        s_width, s_height = screen_dim
        if self.pos_x + self.rad >= s_width or self.pos_x - self.rad <= 0:
            self.pos_y = s_height//2
            self.pos_x = s_width//2
            self.vel_x = 2
            self.vel_y = 2
        if self.pos_y + self.rad >= s_height or self.pos_y - self.rad <= 0:
            self.vel_y = -self.vel_y

        for paddle in paddles:
            paddle_left = paddle.pos_x < s_width//2
            reflection = self.pos_x - self.rad < paddle.pos_x + paddle.width if paddle_left else self.pos_x + self.rad > paddle.pos_x
            if paddle.pos_y < self.pos_y < paddle.pos_y + paddle.height and reflection:
                self.vel_x += self.vel_x/abs(self.vel_x) * self.acc[0]
                self.vel_y += self.vel_y/abs(self.vel_y) * self.acc[1]
                self.vel_x = self.vel_x/abs(self.vel_x) * min([self.original_vel[0], abs(self.vel_x)])
                self.vel_y = self.vel_y/abs(self.vel_y) * min([self.original_vel[1], abs(self.vel_y)])
                self.vel_x = -self.vel_x

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (self.pos_x, self.pos_y), self.rad)


class Paddle:
    def __init__(self, pos, vel):
        self.pos_x, self.pos_y = pos
        self.height = 65
        self.width = 12
        self.vel = vel

    def draw(self, screen):
        rect = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)
        pygame.draw.rect(screen, (255, 255, 255), rect)

    def update(self, move_down):
        if move_down:
            self.pos_y += self.vel
        else:
            self.pos_y -= self.vel

