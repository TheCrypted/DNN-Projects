import copy

import cv2


def display_text(text, frame, position):
    x, y = position
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    font_color = (255, 255, 255)  # White color
    font_thickness = 2
    text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
    width, height = text_size
    cv2.rectangle(frame, (x, y - 8 - height), ((x + 10 + width), y), (0, 0, 0), thickness=cv2.FILLED)
    cv2.putText(frame, text, (x + 6, y - height + 4), font, font_scale, font_color, font_thickness)


def iou_calc(box_dim_a, box_dim_b):
    x1, y1, x2, y2, conf, label = box_dim_a
    _x1, _y1, _x2, _y2, _conf, _label = box_dim_b
    mid_x_a, mid_x_b = (x1 + x2) / 2, (_x1 + _x2) / 2
    mid_y_a, mid_y_b = (y1 + y2) / 2, (_y1 + _y2) / 2
    if abs(mid_x_a - mid_x_b) >= ((x2 - x1) / 2 + (_x2 - _x1) / 2) or abs(mid_y_a - mid_y_b) >= ((y2 - y1) / 2 + (_y2 - _y1) / 2):
        intersection = 0
    else:
        width = min(x2, _x2) - max(x1, _x1)
        height = min(y2, _y2) - max(y1, _y1)
        intersection = width * height
    union = (x2 - x1) * (y2 - y1) + (_x2 - _x1) * (_y2 - _y1) - intersection
    return intersection / union


def iou_box_filtering(boxes, threshold=0.7):
    sorted_boxes = sorted(boxes, key=lambda x: x[4], reverse=True)
    sorted_copy = copy.deepcopy(sorted_boxes)
    removal_idc = []
    for i, box in enumerate(sorted_boxes):
        if i in removal_idc:
            continue
        for j, other_box in enumerate(sorted_boxes):
            if i >= j:
                continue
            iou = iou_calc(box, other_box)
            # print(iou, i, j)
            if iou > threshold and j not in removal_idc:
                removal_idc.append(j)
                # print("appended: ", j)
    return [x for i, x in enumerate(sorted_boxes) if i not in removal_idc]


def main():
    box1 = [50, 50, 150, 150, 0.9, "car"]
    box2 = [100, 100, 200, 200, 0.85, "person"]
    box3 = [75, 75, 175, 175, 0.92, "car"]
    box4 = [1000, 1000, 1050, 1050, 0.87, "hello"]
    boxes = [box1, box2, box3, box4]
    print(iou_box_filtering(boxes, threshold=0.1))

