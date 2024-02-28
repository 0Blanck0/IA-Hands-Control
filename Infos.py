import cv2
import time
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

pTime = 0


class Infos:
    def __init__(self, wCam, hCam, fpsm=False, hc=None):
        self.pTime = 0
        self.fpsm = []
        self.hc = hc
        self.fpsm_enable = fpsm,
        self.wCam = wCam,
        self.hCam = hCam

    def drawInfos(self, img):
        self.drawFPS(img)
        self.drawFPSm(img)
        self.drawAttention(img)
        self.drawVolume(img)

    def drawFPS(self, img):
        cTime = time.time()
        fps = 1 / (cTime - self.pTime)

        if self.fpsm_enable:
            self.fpsm.append(fps)

            if len(self.fpsm) > 50:
                self.fpsm = self.fpsm[-50:]

        self.pTime = cTime
        cv2.putText(img, "FPS: " + str(int(fps)), (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))

    def drawFPSm(self, img):
        if self.fpsm_enable:
            result = 0
            values = self.fpsm[-50:]

            for value in values:
                result += value

            moy = result / len(values)
            cv2.putText(img, "FPSm: " + str(int(moy)), (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))

    def drawAttention(self, img):
        if self.hc is not None:
            cv2.circle(img, (30, 80), 15, ((255, 0, 0) if self.hc.attention else (0, 255, 0)), cv2.FILLED)

    def drawVolume(self, img):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        vol = volume.GetMasterVolumeLevel()
        inMin, inMax, step = volume.GetVolumeRange()

        length = self.hc.mapping(vol, inMin, inMax + 20, 0, 280)
        p1 = (10, int(self.hCam - 465))
        p2 = (30, int(self.hCam - 250))
        p3 = (10, int((self.hCam - 250) - length))

        cv2.rectangle(img, p1, p2, (0, 0, 255), 2)
        cv2.rectangle(img, p2, p3, (0, 0, 255), cv2.FILLED)
