# -*- coding: gbk -*-

import pygame
import random
import time
from threading import Thread ,current_thread
import multiprocessing as mpool

from CameraCollection import *

def game(Palm):

    #?????

    pygame.init()
    doub=1.4

    swid=540*doub
    shigh=720*doub

    # screen = pygame.display.set_mode((swid, shigh))
    # pygame.display.set_caption('Double_Pinball')
    clock = pygame.time.Clock()  

    speed = 5*doub  # ��???????????
    b_speed=15

    fuhao=[-1,1]
    x, y = speed*fuhao[random.randint(0,1)], speed*fuhao[random.randint(0,1)]

    ball = pygame.Rect((0, 0), (10, 10))  # ��???��????
    ball.center = swid//2,shigh//2

    board1 = pygame.Rect((0, 0), (15, 150))  # ?????��????
    board2 = pygame.Rect((0, 0), (15, 150))  # ?????��????

    board1.center = 30*doub,shigh//2
    board2.center = swid-30*doub, shigh//2

    #pygame.mouse.set_visible(False)

    gameDisplay = pygame.display.set_mode((swid,shigh))
    pygame.display.set_caption('Double_Pinball')
    
    Gicon = pygame.image.load("Gicon.png")
    pygame.display.set_icon(Gicon)
    background = pygame.image.load('./Double_Pinball/image/0.png').convert()
    background = pygame.transform.smoothscale(background, gameDisplay.get_size())
    gameDisplay.blit(background, (0, 0))
    score=0
    
    LeftH=0
    RightH=0


    #???????

    r = False
    while True:
        
        if(r==False):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    r = False
                    
            if(Palm.qsize()>0):
                control=Palm.get(True)
                for kkk in control:
                    if(kkk[2]=='l'):
                        LeftH=kkk[1]
                    if(kkk[2]=='r'):
                        RightH=kkk[1]
            
            
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                score=0
                speed=5
                x, y = speed*fuhao[random.randint(0,1)], speed*fuhao[random.randint(0,1)]
                
                ball = pygame.Rect((0, 0), (10, 10))  # ��???��????
                ball.center = swid//2,shigh//2

                board1 = pygame.Rect((0, 0), (15, 150))  # ?????��????
                board2 = pygame.Rect((0, 0), (15, 150))  # ?????��????

                board1.center = 30*doub,shigh//2
                board2.center = swid-30*doub, shigh//2
                r=True
                
                now_pic=3
                begin_time=pygame.time.get_ticks()
                while(pygame.time.get_ticks()-begin_time<=3000):
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            r = False
                    if(pygame.time.get_ticks()-begin_time>=1000):now_pic=2
                    if(pygame.time.get_ticks()-begin_time>=2000):now_pic=1
                    background = pygame.image.load(f'./Double_Pinball/image/{now_pic}.png').convert()
                    background = pygame.transform.smoothscale(background, gameDisplay.get_size())
                    gameDisplay.blit(background, (0, 0))
                    
                    
                    if pygame.key.get_pressed()[pygame.K_w]:
                        board1.center = 30*doub,max(board1.center[1]-b_speed,24*doub+75)
                    if pygame.key.get_pressed()[pygame.K_s]:
                        board1.center = 30*doub,min(board1.center[1] + b_speed,shigh-24*doub-75)
                    if pygame.key.get_pressed()[pygame.K_UP]:
                        board2.center = swid-30*doub,max(board2.center[1]-b_speed,24*doub+75)
                    if pygame.key.get_pressed()[pygame.K_DOWN]:
                        board2.center = swid-30*doub,min(board2.center[1] + b_speed,shigh-24*doub-75)
                    if(LeftH>0):
                        board1.center = 30*doub,min(max(LeftH,24*doub+75),shigh-24*doub-75)
                    if(RightH>0):
                        board2.center = swid-30*doub,min(max(RightH,24*doub+75),shigh-24*doub-75)
                    
                    
                    pygame.draw.circle(screen, (243, 160, 49), ball.center, 10)  # ???????��??��????????

                    pygame.draw.rect(screen, (70, 130, 253), board1)  # ??????????��??????????
                    pygame.draw.rect(screen, (211, 53, 78), board2)  # ??????????��??????????
                    

                    if(Palm.qsize()>0):
                        control=Palm.get(True)
                        for kkk in control:
                            if(kkk[2]=='l'):
                                LeftH=kkk[1]
                            if(kkk[2]=='r'):
                                RightH=kkk[1]
                    
                    
                    clock.tick(50)  # ???30??
                    pygame.display.update()

            
            clock.tick(50)  # ???30??

            pygame.draw.circle(screen, (243, 160, 49), ball.center, 10)  # ???????��??��????????
            pygame.draw.rect(screen, (70, 130, 253), board1)  # ??????????��??????????
            pygame.draw.rect(screen, (211, 53, 78), board2)  # ??????????��??????????
        
            pygame.display.update()
        
        
        
        else:
            
            gameDisplay.blit(background, (0, 0))
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    r = False

            
            if ball.colliderect(board1):  # ��?????????��?????????????
                speed += 0.5
                x = speed
                score +=1
            if ball.colliderect(board2):  # ��?????????��?????????????
                speed +=0.5
                x = -speed
                score +=1
                
            if ball.bottom > shigh-24*doub-speed:  # ��???��????��???????
                y = -speed
            if ball.top <= 24*doub+speed:
                y = speed
            if ball.left<=20*doub-speed:
                r=False
            if ball.right>=swid-20*doub+speed:
                r=False

            ball.move_ip(x, y)  # ???????��???��???????

            
            if pygame.key.get_pressed()[pygame.K_w]:
                board1.center = 30*doub,max(board1.center[1]-b_speed,24*doub+75)
            if pygame.key.get_pressed()[pygame.K_s]:
                board1.center = 30*doub,min(board1.center[1] + b_speed,shigh-24*doub-75)
            if pygame.key.get_pressed()[pygame.K_UP]:
                board2.center = swid-30*doub,max(board2.center[1]-b_speed,24*doub+75)
            if pygame.key.get_pressed()[pygame.K_DOWN]:
                board2.center = swid-30*doub,min(board2.center[1] + b_speed,shigh-24*doub-75)
            
            if(LeftH>0):
                board1.center = 30*doub,min(max(LeftH,24*doub+75),shigh-24*doub-75)
            if(RightH>0):
                board2.center = swid-30*doub,min(max(RightH,24*doub+75),shigh-24*doub-75)
            
            if(Palm.qsize()>0):
                control=Palm.get(True)
                for kkk in control:
                    if(kkk[2]=='l'):
                        LeftH=kkk[1]
                    if(kkk[2]=='r'):
                        RightH=kkk[1]


            clock.tick(50)  # ???30??
            background = pygame.image.load(f'./Double_Pinball/image/{score}.png').convert()
            background = pygame.transform.smoothscale(background, gameDisplay.get_size())
            gameDisplay.blit(background, (0, 0))
            pygame.draw.circle(screen, (243, 160, 49), ball.center, 10)  # ???????��??��????????
            pygame.draw.rect(screen, (70, 130, 253), board1)  # ??????????��??????????
            pygame.draw.rect(screen, (211, 53, 78), board2)  # ??????????��??????????
        
            pygame.display.update()


if(__name__=='__main__'):
    manager = mpool.Manager()
    Palm = manager.Queue()
    Po=mpool.Pool()
    Two=Po.apply_async(game,args=(Palm,))
    time.sleep(0.5)
    One=Po.apply_async(datasend,args=(Palm,))

    
    Po.close()
    Po.join()