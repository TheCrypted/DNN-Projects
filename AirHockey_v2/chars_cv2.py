import cv2

from AirHockey_v2.helper_func import display_text_dynamic


class Referee:
    def __init__(self, screen_dim):
        self.rect_width = 30
        self.rect_pos_color = (9, 104, 61)
        self.rect_neg_color = (0, 0, 61)
        self.s_width, self.s_height = screen_dim
        self.player_score = 0
        self.best_score = None

    def draw(self, screen):
        cv2.rectangle(screen, (self.s_width - self.rect_width, 0), (self.s_width, self.s_height), self.rect_pos_color, -1)
        cv2.rectangle(screen, (0, 0), (self.rect_width, self.s_height), self.rect_neg_color, -1)
        display_text_dynamic(f'Score: {self.player_score}', screen, (170, 20), 30)
        if self.best_score is not None:
            display_text_dynamic(f'Best Score: {self.best_score}', screen, (170, self.s_height - 30), 15)

    def update(self, ball):
        if ball.pos[0] + ball.rad >= self.s_width:
            self.player_score += 1
        if ball.pos[0] - ball.rad <= 10:
            if self.best_score is None or self.player_score > self.best_score:
                self.best_score = self.player_score
            self.player_score = 0

        if ball.pos[0] > self.s_width - self.rect_width:
            self.rect_pos_color = (0, 255, 0)
        else:
            self.rect_pos_color = (9, 104, 61)

        if ball.pos[0] < self.rect_width:
            self.rect_neg_color = (0, 0, 255)
        else:
            self.rect_neg_color = (0, 0, 61)


class Ball:
    def __init__(self, pos, vel, rad):
        self.pos = pos
        self.rad = rad
        self.vel = vel
        self.color = (0, 0, 0)

    def draw(self, screen):
        s_width, s_height = 640, 480
        cv2.circle(screen, self.pos, self.rad, self.color, -1)

    def update(self, screen_dim, paddle):
        for i, pos in enumerate(self.pos):
            self.pos[i] += self.vel[i]
        self.handle_collision(screen_dim, paddle)

    def handle_collision(self, screen_dim, paddle):
        for i in range(2):
            if self.pos[i] + self.rad > screen_dim[i] or self.pos[i] - self.rad < i:
                self.vel[i] = - self.vel[i]
                if i == 0 and self.vel[i] > 0:
                    self.pos = [screen_dim[0]//2, screen_dim[1]//2]
        if (paddle.pos_y < self.pos[1] < paddle.pos_y + paddle.height) and (self.pos[0] - self.rad < paddle.pos_x + paddle.width):
            self.vel[0] = -self.vel[0]


class Paddle:
    def __init__(self, pos):
        self.pos_x, self.pos_y = pos
        self.height = 55
        self.width = 12

    def draw(self, screen):
        cv2.rectangle(screen, (self.pos_x, self.pos_y), (self.pos_x + self.width, self.pos_y + self.height), (0, 0, 0), -1)

    def update(self, p_y):
        self.pos_y = p_y
