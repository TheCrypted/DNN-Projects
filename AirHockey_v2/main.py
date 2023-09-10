import pygame
import pygame.camera
import cv2
import numpy as np
from ultralytics import YOLO
from AirHockey_v2.chars import Ball, Paddle
from AirHockey_v2.helper_func import iou_box_filtering

pygame.init()
pygame.camera.init()

cameras = pygame.camera.list_cameras()
camera = pygame.camera.Camera(cameras[0])
# camera.resolution = (20, 20)
camera.start()
model = YOLO("best2.pt")
SCREEN_WIDTH = 1028
SCREEN_HEIGHT = 720
FPS = 60
run = True
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
color_rgb = {"red": (255, 0, 0), "green": (0, 255, 0), "blue": (0, 0, 255), "yellow": (255, 255, 0), "cyan": (0, 255, 255), "magenta": (255, 0, 255), "white": (255, 255, 255), "black": (0, 0, 0), "orange": (255, 165, 0), "purple": (128, 0, 128), "pink": (255, 192, 203)}
clock = pygame.time.Clock()

background_mute = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
ball = Ball(20, (5, 5), (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
paddle_1 = Paddle((48, SCREEN_HEIGHT//2), 7)
paddle_2 = Paddle((SCREEN_WIDTH - 60, SCREEN_HEIGHT//2), 7)
paddles = [paddle_1, paddle_2]
background_mute.fill((0, 0, 0, 208))



while run:
    screen.fill(color_rgb["black"])

    # key = pygame.key.get_pressed()
    # pygame.draw.circle(screen, color_rgb["white"], (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), 20)
    frame = camera.get_image()
    resized_frame = pygame.transform.scale(frame, (SCREEN_WIDTH, SCREEN_HEIGHT))
    frame_arr = np.asarray(pygame.surfarray.array3d(frame))
    frame_arr = frame_arr[:, :, ::-1]
    results = model.predict(frame_arr)
    result_arr = iou_box_filtering([x.tolist() for x in results[0].boxes.data], threshold=0.1)

        # print("Found hand")

    screen.blit(resized_frame, (0, 0))
    screen.blit(background_mute, (0, 0))
    for result in result_arr:
        int_res = [int(x) for x in result]
        x1, y1, x2, y2, conf, label = int_res
        bounding_rect = pygame.Rect(x1, y1, x2-x1, y2-y1)
        # bounding_rect = pygame.Rect(20, 20, 100, 100)
        pygame.draw.rect(screen, (255, 255, 255), bounding_rect)
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
    # pygame.display.flip()
    pygame.display.update()
    clock.tick(FPS)
