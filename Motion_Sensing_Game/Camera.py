import math
import random
import cvzone
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

def collect(center):
    print("Camera Begin!!!")
    cap = cv2.VideoCapture(0)
    cap.set(3, 1080)  # 将宽设置为1080
    cap.set(4, 720)  # 将高设置为720

    detector = HandDetector(detectionCon=0.8, maxHands = 1)

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)

        hands, img = detector.findHands(img, flipType=False)
        if hands:
            center[0] = hands[0]['center']
#             print(center)
        img = cv2.resize(img, (960, 960))  # 将图像调整为720 x 720
        img = img[0:1080, 180:960]  # 将图像裁剪为720 x 720
        cv2.imshow("Image", img)
        if cv2.waitKey(1) == ord('r'):
            game.gameOver = False

if __name__ == '__main__':
    
    collect([None])











'''
import math
import random
import cvzone
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

def collect():
    cap = cv2.VideoCapture(0)
    cap.set(3, 1080)  # 将宽设置为1080
    cap.set(4, 720)  # 将高设置为720

    detector = HandDetector(detectionCon=0.8, maxHands = 1)

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)

        hands, img = detector.findHands(img, flipType=False)
        if hands:
            center = hands[0]['center']
#             lmList = hands[0]['lmList']
#             pointIndex = lmList[8][0:2]
            print(center)
        img = cv2.resize(img, (720, 960))  # 将图像调整为720 x 960
        cv2.imshow("Image", img)
        if cv2.waitKey(1) == ord('r'):
            game.gameOver = False

if __name__ == '__main__':
    collect()
'''