# -*- coding: gbk -*-

import cv2
import mediapipe as mp
import pandas as pd
import time
from threading import Thread ,current_thread
import multiprocessing as mpool
ptime , ctime = 0 , 0

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
mpDraws = mp.solutions.drawing_styles

cap = cv2.VideoCapture(0)
def datasend(Palm):
    lingshi=[]
    while True:
        success , img = cap.read()
        img = cv2.flip(img, 1)
        img = cv2.resize(img, (950, 1000)) #1080*1440

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        Hand_res = []
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                H = []
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y *h)
                    H.append([cx,cy])
                    cv2.circle(img, (cx, cy), 3, (255, 0, 255), cv2.FILLED)
                Hand_res.append(H)
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS, mpDraws.get_default_hand_landmarks_style(), mpDraws.get_default_hand_connections_style())
        
        lingshi=[]
            
        for i in Hand_res:
            px , py = (i[0][0]+i[5][0]+i[9][0]+i[13][0]+i[17][0])//5, (i[0][1]+i[5][1]+i[9][1]+i[13][1]+i[17][1])//5
            pl = 'l'
            if px > 1080//2: #540
                pl = 'r'
            lingshi.append([px, py, pl])

        if len(lingshi) == 2 and lingshi[0][0] > lingshi[1][0]:
            lingshi[0] , lingshi[1] = lingshi[1] , lingshi[0]
        if(lingshi and len(lingshi)<=2):    Palm.put(lingshi)

        global ctime, ptime
        ctime = time.time()
        if(ctime-ptime!=0):fps = 1/(ctime-ptime)
        ptime = ctime
        fps = int(fps)
        if fps < 20:    cv2.putText(img, str(fps), (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
        elif fps <25:   cv2.putText(img, str(fps), (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 3)
        else:   cv2.putText(img, str(fps), (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)

        cv2.imshow('frame', img)
        cv2.moveWindow("frame", 0, 0)
        cv2.waitKey(1)


if(__name__=='__main__'):
    manager = mpool.Manager()
    Palm = manager.Queue()
    Po=mpool.Pool()
    One=Po.apply_async(datasend,args=(Palm,))
    Po.close()
    Po.join()