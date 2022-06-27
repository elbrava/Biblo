import cv2

# source
import numpy as np
import mediapipe as mp

webcam = cv2.VideoCapture(0)
_, im = webcam.read()
mask = np.zeros(im.shape, np.uint8)
mp_draw = mp.solutions.drawing_utils
webcam = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
han = mp_hands.Hands()
cx = 0
cy = 0
_, image = webcam.read()
thresh_val = 40
while webcam.isOpened():

    main_img = []
    success, im = webcam.read()
    image = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    results = han.process(image)
    r = results.multi_hand_landmarks
    h, w, c = image.shape
    if r:

        mp_draw.draw_landmarks(image, r[0], mp_hands.HAND_CONNECTIONS)
        if r[0].landmark[5].y >= r[0].landmark[8].y:
            closed = False
        else:

            closed = True
        if not closed:

            if cx == 0 and cy == 0:
                cx = int(r[0].landmark[8].x * w)
                cy = int(r[0].landmark[8].y * h)
                xp = int(r[0].landmark[8].x * w)
                yp = int(r[0].landmark[8].y * h)
                print(cx, xp, cy, yp)
                cv2.line(mask, (cx, cy), (cx, cy), (100, 0, 0), 7)

            else:

                cv2.line(mask, (int(cx), int(cy)), (int(r[0].landmark[8].x * w), int(r[0].landmark[8].y * h)),
                         (100, 0, 0), 7)
                cx = r[0].landmark[8].x * w
                cy = r[0].landmark[8].y * h

        print("closed:", closed)

    cv2.imshow("h", image)
    cv2.imshow("j", mask)

    mask1 = np.zeros(im.shape, np.uint8)
    im = cv2.flip(im, 1)
    cv2.imshow("im ", im)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    cv2.imshow("gr", gray)
    rec, thresh = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_TOZERO)
    print(thresh_val)
    #thresh_val += 1
    h, w, c = im.shape
    cont, hie = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    cv2.imshow("main", thresh)
    cv2.drawContours(mask1, cont, -1, (222, 00, 0))
    cv2.imshow("maskn", mask1)
    # cv2.findContours(thresh, cv2.CHAIN_APPROX_NONE)
    cv2.waitKey(1)
import cv2
import mediapipe as mp
import numpy as np

import pytesseract

mp_draw = mp.solutions.drawing_utils
webcam = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
han = mp_hands.Hands()
cx = 0
cy = 0
_, image = webcam.read()

mask = np.zeros(image.shape, np.uint8)


def img_recog(img):
    # Import required packages

    try:
        # Mention the installed location of Tesseract-OCR in your syste
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

        # Read image from which text needs to be extracted

        # Preprocessing the image starts

        # Convert the image to gray scale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imshow("gr0", gray)
        # Performing OTSU threshold
        ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

        # Specify structure shape and kernel size.
        # Kernel size increases or decreases the area
        # of the rectangle to be detected.
        # A smaller value like (10, 10) will detect
        # each word instead of a sentence.
        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

        # Applying dilation on the threshold image
        dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)

        # Finding contours
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_NONE)

        # Creating a copy of image
        im2 = img.copy()

        # A text file is created and flushed

        for cnt in contours:
            x, y, wi, he = cv2.boundingRect(cnt)

            # Drawing a rectangle on copied image
            rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Cropping the text block for giving input to OCR
            cropped = im2[y:y + h, x:x + w]

            # Open the file in append mode
            cv2.imshow("cr", cropped)
            # Apply OCR on the cropped image
            text = pytesseract.image_to_string(cropped)
            print("Fuv", text)
            return text
    except Exception as e:
        print(e)


while False:
    sucess, image = webcam.read()
    image = cv2.flip(image, 1)
    results = han.process(image)
    r = results.multi_hand_landmarks
    h, w, c = image.shape

    if r:

        mp_draw.draw_landmarks(image, r[0], mp_hands.HAND_CONNECTIONS)
        if r[0].landmark[5].y >= r[0].landmark[8].y:
            closed = False
        else:

            closed = True
        if not closed:

            if cx == 0 and cy == 0:
                cx = int(r[0].landmark[8].x * w)
                cy = int(r[0].landmark[8].y * h)
                xp = int(r[0].landmark[8].x * w)
                yp = int(r[0].landmark[8].y * h)
                print(cx, xp, cy, yp)
                cv2.line(mask, (cx, cy), (cx, cy), (100, 0, 0), 7)

            else:

                cv2.line(mask, (int(cx), int(cy)), (int(r[0].landmark[8].x * w), int(r[0].landmark[8].y * h)),
                         (100, 0, 0), 7)
                cx = r[0].landmark[8].x * w
                cy = r[0].landmark[8].y * h

        print("closed:", closed)

    cv2.imshow("h", image)
    cv2.imshow("j", mask)

    k = cv2.waitKey(1)
    if k == 27:  # wait for ESC key to exit
        mask = np.zeros(image.shape, np.uint8)

    elif k == ord('l'):  # wait for 's' key to save and exit
        cv2.putText(mask, "love", (w // 2, h // 2), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 55, 55), 7)
