import pygame

from AirHockey_v2.Ball import Ball

pygame.init()

SCREEN_WIDTH = 1028
SCREEN_HEIGHT = 720
FPS = 60
run = True
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
color_rgb = {"red": (255, 0, 0), "green": (0, 255, 0), "blue": (0, 0, 255), "yellow": (255, 255, 0), "cyan": (0, 255, 255), "magenta": (255, 0, 255), "white": (255, 255, 255), "black": (0, 0, 0), "orange": (255, 165, 0), "purple": (128, 0, 128), "pink": (255, 192, 203)}

ball = Ball(20, (0.25, 0.25), (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))

while run:
    screen.fill(color_rgb["black"])

    # key = pygame.key.get_pressed()
    # pygame.draw.circle(screen, color_rgb["white"], (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), 20)
    ball.draw(screen)


    key = pygame.key.get_pressed()
    if key[pygame.K_q]:
        run = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    ball.update()
    pygame.display.update()
