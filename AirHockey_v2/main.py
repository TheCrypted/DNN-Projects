import pygame

from AirHockey_v2.chars import Ball, Paddle

pygame.init()

SCREEN_WIDTH = 1028
SCREEN_HEIGHT = 720
FPS = 60
run = True
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
color_rgb = {"red": (255, 0, 0), "green": (0, 255, 0), "blue": (0, 0, 255), "yellow": (255, 255, 0), "cyan": (0, 255, 255), "magenta": (255, 0, 255), "white": (255, 255, 255), "black": (0, 0, 0), "orange": (255, 165, 0), "purple": (128, 0, 128), "pink": (255, 192, 203)}
clock = pygame.time.Clock()

ball = Ball(20, (5, 5), (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
paddle_1 = Paddle((48, SCREEN_HEIGHT//2), 7)
paddle_2 = Paddle((SCREEN_WIDTH - 60, SCREEN_HEIGHT//2), 7)
paddles = [paddle_1, paddle_2]
while run:
    screen.fill(color_rgb["black"])

    # key = pygame.key.get_pressed()
    # pygame.draw.circle(screen, color_rgb["white"], (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), 20)
    ball.draw(screen)
    paddle_1.draw(screen)
    paddle_2.draw(screen)

    key = pygame.key.get_pressed()
    if key[pygame.K_q]:
        run = False
    if key[pygame.K_w] and paddle_1.pos_y > 0:
        paddle_1.update(False)
    elif key[pygame.K_s] and paddle_1.pos_y + paddle_1.height < SCREEN_HEIGHT:
        paddle_1.update(True)
    if key[pygame.K_UP] and paddle_2.pos_y > 0:
        paddle_2.update(False)
    elif key[pygame.K_DOWN] and paddle_2.pos_y + paddle_2.height < SCREEN_HEIGHT:
        paddle_2.update(True)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    ball.update((SCREEN_WIDTH, SCREEN_HEIGHT), paddles)
    pygame.display.update()
    clock.tick(FPS)
