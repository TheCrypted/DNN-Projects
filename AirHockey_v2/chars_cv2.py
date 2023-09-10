import cv2


class Ball:
    def __init__(self, pos, vel, rad):
        self.pos = pos
        self.rad = rad
        self.vel = vel
        self.color = (0, 0, 0)

    def draw(self, screen):
        cv2.circle(screen, self.pos, self.rad, self.color, -1)

    def update(self, screen_dim):
        for i, pos in enumerate(self.pos):
            self.pos[i] += self.vel[i]
        self.handle_collision(screen_dim)

    def handle_collision(self, screen_dim):
        for i in range(2):
            if self.pos[i] + self.rad > screen_dim[i] or self.pos[i] - self.rad < i:
                self.vel[i] = - self.vel[i]


class Paddle:
    def __init__(self, pos):
        self.pos_x, self.pos_y = pos
        self.height = 40
        self.width = 12

    def draw(self, screen):
        cv2.rectangle(screen, (self.pos_x, self.pos_y), (self.pos_x + self.width, self.pos_y + self.height), (0, 0, 0), -1)

    def update(self, p_y):
        self.pos_y = p_y
