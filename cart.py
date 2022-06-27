import cv2
import numpy as np

cv2.setUseOptimized(onoff=True)
blur = 3
k = 0
linesize = 7
webcam = cv2.VideoCapture(0)
while webcam.isOpened():
    _, frame = webcam.read()
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grayBlur = cv2.medianBlur(gray, blur)
    edges = cv2.adaptiveThreshold(grayBlur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, linesize, blur)

    if k % 3 == 0:
        data = np.float32(frame).reshape((-1, 3))
        crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)
        ret, label, center = cv2.kmeans(data, 20, None, crit, 10, cv2.KMEANS_PP_CENTERS)
        center = np.uint8(center)
        result = center[label.flatten()]
        result = result.reshape(frame.shape)
        cv2.imshow("color plate", result)
        cv2.imshow("h", edges)
        cv2.imshow("foinal", cv2.bitwise_and(result, result, mask=edges))
    print(k)
    k += 1

    cv2.waitKey(1)
