import math
import os
import sys
import threading
import time
import  redis
c = os.getcwd()

import cv2
import mediapipe as mp
import numpy as np
from numpy import ceil

webcam = cv2.VideoCapture(0)

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

count = 0
time_begin = time.perf_counter()
right_pointer_x = 0
right_pointer_y = 0
left_pointer_x = 0
left_pointer_y = 0
left_angle = 0
right_angle = 0
im = ""
right_closed = False
left_closed = False
left_edit = True
right_edit = True
speed = 0
tm = ""
height, width = 720, 1280


def angle(li_st, points):
    x1, y1 = li_st[points[0]].x, li_st[points[0]].y
    x2, y2 = li_st[points[1]].x, li_st[points[1]].y
    x3, y3 = li_st[points[2]].x, li_st[points[2]].y

    return math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))


def pre_wok():
    while webcam.isOpened():
        success, frame = webcam.read()

        with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
            t1 = threading.Thread(target=work, args=[holistic, frame])
            t1.start()
            t1.join()
            cv2.imshow("dh", im)
            cv2.imshow("h", tm)
            k = cv2.waitKey(1)
            if k == 27:
                webcam.release()
                cv2.destroyAllWindows()


def work(holistic, frame):
    lineSPEC = mp_drawing.DrawingSpec(thickness=30)
    global height, width, right_closed, left_closed, left_edit, right_edit, speed, time_begin, tm

    global count, left_angle, right_angle, right_pointer_x, right_pointer_y, left_pointer_x, left_pointer_y, im
    # Recolor Feed
    mask = np.zeros(frame.shape, np.uint8)
    cx = 0
    cy = 0

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = cv2.flip(image, 1)
    # Make Detections
    results = holistic.process(image)
    # print(results.face_landmarks)
    # face_landmarks, pose_landmarks, left_hand_landmarks, right_hand_landmarks
    # Recolor image back to BGR for rendering

    # Draw face landmarks
    # mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS)
    circ = mp_drawing.DrawingSpec(circle_radius=10)
    h, w, c = height, width, image.shape[-1]
    mp_drawing.draw_landmarks(mask, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS, None, lineSPEC)
    r = results.right_hand_landmarks

    mp_drawing.draw_landmarks(mask, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, circ, lineSPEC)
    if results.right_hand_landmarks:
        # 5,9,13,17

        if r.landmark[9].y >= r.landmark[12].y:
            right_closed = False



        else:

            right_closed = True
        if right_closed and right_edit:
            x, y = [], []
            for i in [0, 5, 9, 13, 17]:
                x.append(r.landmark[i].x * w)
                y.append(r.landmark[i].y * h)
            cx = sum(x) / len(x)
            cy = sum(y) / len(y)
            right_pointer_x = cx
            right_pointer_y = cy
        print("right:", right_closed)

        cv2.circle(image, [int(cx), int(cy)], 3, (204, 34, 55), -1)

    mp_drawing.draw_landmarks(mask, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, circ, lineSPEC)

    l = results.left_hand_landmarks
    if results.left_hand_landmarks:
        # 5,9,13,17

        if l.landmark[9].y >= l.landmark[12].y:
            left_closed = False
        else:

            left_closed = True
        if left_closed and left_edit:
            x, y = [], []
            for i in [0, 5, 9, 13, 17]:
                x.append(l.landmark[i].x * w)
                y.append(l.landmark[i].y * h)
            cx = sum(x) / len(x)
            cy = sum(y) / len(y)
            cv2.circle(image, [int(cx), int(cy)], 3, (204, 34, 55), -1)
            left_pointer_x = cx
            left_pointer_y = cy
        print("left", left_closed)

    # Pose Detections
    p = results.pose_landmarks
    mp_drawing.draw_landmarks(mask, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS, circ, lineSPEC)

    if p:
        left = abs(angle(p.landmark, [14, 12, 24]))
        right = angle(p.landmark, [13, 11, 23])
        print("left:", int(left))
        print("RIGHT:", int(right))
        speed1 = (left - left_angle) / (time.perf_counter() - time_begin)
        if speed1 < 0: speed1 = 0
        speed2 = (right - right_angle) / (time.perf_counter() - time_begin)
        if speed2 < 0: speed2 = 0
        print(speed)
        speed = speed1 + speed2
        print("speed", speed)
        left_angle = left
        right_angle = right
        time_begin = time.perf_counter()
    im = mask

    tm = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


def onrelease():
    global left_pointer_y, left_pointer_x, right_pointer_y, right_pointer_x, left_closed, right_closed, left_edit
    global right_edit

    if not (int(left_pointer_x) == 0 and int(left_pointer_y) == 0):

        if not left_closed:
            left_edit = False

    if not (int(right_pointer_x) == 0 and int(right_pointer_y) == 0):

        if not right_closed:
            right_edit = False


t = threading.Thread(target=pre_wok)
t.start()
score = 0
