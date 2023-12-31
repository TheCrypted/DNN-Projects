from ultralytics import YOLO
import time
import cv2

from AirHockey_v2.chars_cv2 import Ball, Paddle, Referee
from AirHockey_v2.helper_func import iou_box_filtering

model = YOLO("best2.pt")

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
cap = cv2.VideoCapture(0)

# Define char objects
ball = Ball([SCREEN_WIDTH//2, SCREEN_HEIGHT//2], [10, 15], 15)
paddle = Paddle((30, 40))
referee = Referee((SCREEN_WIDTH, SCREEN_HEIGHT))
prev_pos = 40
movement_thresh = 7
FPS = 45


while True:
    ret, frame = cap.read()
    start_time = time.time()
    if not ret:
        print("Error reading frame")
        break
    try:
        referee.draw(frame)
        ball.draw(frame)
        paddle.draw(frame)
        results = model.predict(frame)
        resized_frame = cv2.resize(frame, (SCREEN_WIDTH, SCREEN_HEIGHT))
        result_arr = iou_box_filtering([x.tolist() for x in results[0].boxes.data], threshold=0.1)
        for result in result_arr:
            # Get results in integer format and destructure the array
            int_res = [int(x) for x in result]
            x1, y1, x2, y2, conf, label = int_res
            y_pos = (y1+y2)//2
            cv2.circle(frame, ((x1+x2)//2, y_pos), 4, (0, 0, 0), -1)
            # Update paddle Y position if the change in detection position is more than threshold (To reduce noise)
            if abs(y_pos - prev_pos) > movement_thresh:
                paddle.update(y_pos)
                prev_pos = y_pos
            # cv2.rectangle(frame, (x1, y1), (x2, y2), (120, label / 60 * 255, (1 - label) / 60 * 255), 5)
        ball.update((SCREEN_WIDTH, SCREEN_HEIGHT), paddle)
        referee.update(ball)

    except Exception as e:
        print("Error occurred while making prediction", e)
    cv2.imshow("Live Camera Feed", frame)
    # Calculate time to frame end and wait accordingly
    elapsed_time = time.time() - start_time
    overflow_time = max(0, 1 / (FPS - elapsed_time))
    if cv2.waitKey(int(overflow_time * 1000)) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()