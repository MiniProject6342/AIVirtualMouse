import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy
import pyautogui as py

wCam,hCam=700,480
# wCam,hCam=autopy.screen.size()
frameR=1
ptime=0
smoothening=8

plocX,plocY=0,0
clocX,clocY=0,0
cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
hmin = 50
hmax = 200
tipIds = [4, 8, 12, 16, 20]
py.FAILSAFE = False

detector=htm.HandDetector(maxHands=2,detectionCon=0.85, trackCon=0.8)
wScr,hScr=py.size()
# wScr,hScr=autopy.screen.size()
while True:
    success,img=cap.read()
    # img=cv2.flip(img,1)
    img=detector.findHands(img)
    lmList,bbox=detector.findPosition(img)
    if len(lmList)!=0:
        x1,y1=lmList[8][1:]
        x2,y2=lmList[12][1:]
        fingers=detector.fingersUp()
        cv2.rectangle(img,(frameR,frameR),(wCam-frameR,hCam-frameR),(255,0,255),2)
        #cursor
        if fingers==[0,1,1,0,0]:
            x3=np.interp(x1,(frameR,wCam-frameR),(0,wScr))
            y3=np.interp(y1,(frameR,hCam-frameR),(0,hScr))
            clocX=plocX+(x3-plocX)/smoothening
            clocY=plocY+(y3-plocY)/smoothening
            # autopy.mouse.move(wScr-clocX,clocY)
            py.moveTo(wScr - clocX, clocY)
            # cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
            plocX,plocY=clocX,clocY
        #drag
        if fingers==[0,0,0,0,0]:
            py.mouseDown()
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
            py.moveTo(wScr - clocX, clocY, duration=0.1)
            plocX, plocY = clocX, clocY

        #click operation
        if fingers==[0,0,1,0,0]:
            # length,img,lineInfo=detector.findDistance(8,12,img)
            # if length<40:
            #     cv2.circle(img,(lineInfo[4],lineInfo[5]),15,(0,255,0),cv2.FILLED)
            py.click()
        #right click
        if fingers==[0,1,0,0,0]:
            # length, img, lineInfo = detector.findDistance(4, 8, img)
            # if length<30:
            #     cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
            autopy.mouse.click(autopy.mouse.Button.RIGHT)
        #scroll up
        if fingers==[1,1,1,0,0]:
            py.scroll(300)
        #scroll down    
        if fingers==[0,1,1,1,0]:
            py.scroll(-300)
        #double click    
        if fingers==[1,1,0,0,0]:
            length, img, lineInfo = detector.findDistance(4, 8, img)
            if length<30:
                py.doubleClick()


    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime
    cv2.putText(img, str(int(fps)), (28, 58), cv2.FONT_HERSHEY_PLAIN, 3, (255, 8, 8), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
