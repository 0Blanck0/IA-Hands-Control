import cv2
import HandsTraking as ht
import HandsCommand as hc
import Infos as inf
import time
import pyautogui


def ia_run():
    wCam, hCam = 640 * 2, 480 * 2
    wScr, hScr = pyautogui.size()
    cTime = time.time()
    pTime = 0

    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)

    detector = ht.HandDetector(maxHands=1, detectionCon=0.9, trackCon=0.6)
    commands = hc.HandsCommand(detector, wScr, hScr, wCam, hCam)
    infos = inf.Infos(wCam, hCam, True, commands)

    while True:
        # Video and Hands
        success, img = cap.read()
        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img)

        # Get fingers cord
        if len(lmList) != 0:
            cords = []

            for i in range(0, (5 * detector.handsCount)):
                cords.append(lmList[detector.tipIds[i]][1:])

            fingers = detector.fingersUp()

            # Get move command
            commands.getCommand(fingers, cords, img)
            cTime = time.time()
            pTime = cTime
        else:
            if cTime - pTime >= 3.5:
                commands.attention = False
                commands.pTime = 0
                cTime = time.time()
                pTime = cTime
            else:
                cTime = time.time()

        # Reverse image
        img = cv2.flip(img, 1)

        # Frame Rate
        infos.drawInfos(img)

        # Display
        cv2.imshow("Move Control", img)
        cv2.waitKey(1)
