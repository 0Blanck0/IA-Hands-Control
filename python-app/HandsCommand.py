import cv2
import numpy as np
import pyautogui
import time
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


class HandsCommand:
    def __init__(self, detector, wScr, hScr, wCam, hCam):
        self.attention, self.acted = False, False
        self.mode = None
        self.detector = detector
        self.att_cooldown = 1.5
        self.rest_cooldown = 1.15
        self.switch_cooldown = 0.7
        self.inact_cooldown = 10
        self.pTime, self.dTime = 0, 0
        self.plocX, self.plocY, self.clocX, self.clocY = 0, 0, 0, 0
        self.cTime = time.time()
        self.wScr, self.hScr = wScr, hScr
        self.wCam, self.hCam = wCam, hCam
        self.framR = 150

    def mapping(self, value, inMin, inMax, outMin, outMax):
        output = (value - inMin) * ((outMax - outMin) / (inMax - inMin)) + outMin
        return output

    def moveMouse(self, cords, img, smoothening=1):
        cv2.rectangle(img, (self.wCam - self.framR, 0 + self.framR), (0 + self.framR, self.hCam - (self.framR + 250)),
                      (255, 0, 255), 2)
        x3 = np.interp(cords[1][0], (0 + self.framR, self.wCam - self.framR), (0, self.wScr))
        y3 = np.interp(cords[1][1], (0 + self.framR, self.hCam - (self.framR + 250)), (0, self.hScr))
        self.clocX = self.plocX + (x3 - self.plocX) / smoothening
        self.clocY = self.plocY + (y3 - self.plocY) / smoothening
        self.plocX, self.plocY = self.clocX, self.clocY

        if self.clocX < 0:
            self.clocX = 0
        elif self.clocX > self.wScr:
            self.clocX = self.wScr

        if self.clocY < 0:
            self.clocY = 0
        elif self.clocY > self.hScr:
            self.clocY = self.hScr

        pyautogui.moveTo(self.wScr - self.clocX, self.clocY, duration=0)
        cv2.circle(img, (cords[1][0], cords[1][1]), 10, (0, 0, 255), cv2.BORDER_REFLECT)

    def volumeLevelControl(self, img, i1, i2):
        length, img, dist = self.detector.findDistance(i1, i2, img)
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        outMin, outMax, step = volume.GetVolumeRange()

        if length >= 320:
            length = 320
        elif length <= 30:
            length = 0

        length = self.mapping(length, 0, 320, outMin, outMax)
        volume.SetMasterVolumeLevel(length, None)

    def getCommand(self, fingers, cords, img):
        self.cTime = time.time()

        if self.cTime - self.pTime >= self.inact_cooldown:
            self.attention = False
            self.mode = None
            self.pTime = self.cTime

        match fingers:
            case [0, 0, 0, 0, 0]:
                if self.cTime - self.pTime >= self.rest_cooldown:
                    self.attention = False
                    self.mode = None
                    self.pTime = self.cTime
            case [1, 1, 1, 1, 1]:
                if self.pTime == 0:
                    self.pTime = self.cTime

                if self.cTime - self.pTime >= self.att_cooldown:
                    self.attention = True
                    self.mode = None
                    self.pTime = self.cTime
            case [0, 1, 0, 0, 0]:
                if self.attention and self.mode == "Move":
                    self.moveMouse(cords, img)
                    self.pTime = self.cTime
                elif self.attention and self.mode is None:
                    self.mode = "Move"
                else:
                    if self.cTime - self.pTime > self.switch_cooldown:
                        self.mode = "Move"
                        self.pTime = self.cTime
            case [0, 1, 1, 0, 0]:
                if self.attention and self.mode == "Move":
                    length, img, dist = self.detector.findDistance(8, 12, img)
                    self.pTime = self.cTime

                    if length <= 40 and not self.acted:
                        pyautogui.click()
                        self.acted = True
                    elif length >= 75:
                        self.acted = False
                elif self.attention and self.mode == "Med":
                    length, img, dist = self.detector.findDistance(8, 12, img)
                    self.pTime = self.cTime

                    if length <= 40 and not self.acted:
                        pyautogui.press('playpause')
                        self.acted = True
                    elif length >= 75:
                        self.acted = False
            case [1, 1, 1, 0, 0]:
                if self.attention and self.mode == "Med":
                    moveX, moveY = self.detector.moveTo(self.detector.tipIds[2])
                    self.pTime = self.cTime

                    if moveX == 1 and not self.acted:
                        pyautogui.press('nexttrack')
                        self.acted = True
                    elif moveX == -1 and not self.acted:
                        pyautogui.press('prevtrack')
                        self.acted = True
                    elif moveX == 0:
                        self.acted = False
                elif self.attention and self.mode is None:
                    self.mode = "Med"
                else:
                    if self.cTime - self.pTime > self.switch_cooldown:
                        self.mode = "Med"
                        self.pTime = self.cTime
            case [1, 1, 0, 0, 0]:
                i1, i2 = 4, 8

                if self.attention and self.mode == "Vol":
                    self.volumeLevelControl(img, i1, i2)
                    self.pTime = self.cTime
                elif self.attention and self.mode is None:
                    self.mode = "Vol"
                else:
                    if self.cTime - self.pTime > self.switch_cooldown:
                        self.mode = "Vol"
                        self.pTime = self.cTime
            case _:
                if self.cTime - self.pTime >= self.rest_cooldown + (self.rest_cooldown / 2):
                    self.attention = False
                    self.mode = None
                    self.pTime = self.cTime
