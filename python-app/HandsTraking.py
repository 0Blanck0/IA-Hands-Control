import cv2
import mediapipe as mp
import math


class HandDetector:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.lmList, self.results = None, None
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, 1, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20, 24, 28, 32, 36, 40]
        self.handsCount, self.plocX, self.plocY = 0, 0, 0

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, draw=True):
        bbox = []
        self.lmList = []

        if self.results.multi_hand_landmarks:
            myHands = self.results.multi_hand_landmarks

            for myHand in myHands:
                xList = []
                yList = []

                for id, lm in enumerate(myHand.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    xList.append(cx)
                    yList.append(cy)
                    self.lmList.append([id, cx, cy])

                    if draw:
                        cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

                xmin, xmax = min(xList), max(xList)
                ymin, ymax = min(yList), max(yList)
                bbox.append([xmin, ymin, xmax, ymax])

            if draw:
                for box in bbox:
                    cv2.rectangle(img, (box[0] - 28, box[1] - 20), (box[2] + 20, box[3] + 20), (0, 255, 0), 2)

        self.handsCount = len(bbox)
        return self.lmList, bbox

    def isRightHand(self):
        return self.lmList[self.tipIds[1]][1] > self.lmList[self.tipIds[4]][1]

    def fingersUp(self):
        fingers = []

        for id in range(1, (5 * self.handsCount)):
            if id != 5:
                if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

        if not self.isRightHand():
            handRight = fingers[4:]
            handLeft = fingers[:4]
        else:
            handRight = fingers[:4]
            handLeft = fingers[4:]

        if self.handsCount == 2:
            if not self.isRightHand() and self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
                handLeft.insert(0, 0)
            else:
                handLeft.insert(0, 1)

            if not self.isRightHand() and self.lmList[self.tipIds[5]][1] > self.lmList[self.tipIds[5] - 1][1]:
                handRight.insert(0, 1)
            else:
                handRight.insert(0, 0)
        else:
            if not self.isRightHand():
                if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
                    handLeft.insert(0, 0)
                else:
                    handLeft.insert(0, 1)
            else:
                if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
                    handRight.insert(0, 1)
                else:
                    handRight.insert(0, 0)

        print(handRight, handLeft)
        fingers = handLeft + handRight
        return fingers

    def findDistance(self, p1, p2, img, draw=True, r=15, t=3):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (255, 8, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 8, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (8, 8, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)
        return length, img, [x1, y1, x2, y2, cx, cy]

    def moveTo(self, p1):
        x1, y1 = self.lmList[p1][1:]
        moveAxe = []

        if self.plocX == 0 and self.plocY == 0:
            self.plocX = x1
            self.plocY = y1

        if x1 > self.plocX + 100:
            moveAxe.append(-1)
        elif x1 < self.plocX - 100:
            moveAxe.append(1)
        else:
            moveAxe.append(0)

        if y1 > self.plocY + 100:
            moveAxe.append(1)
        elif y1 < self.plocY - 100:
            moveAxe.append(-1)
        else:
            moveAxe.append(0)

        return moveAxe