import itertools
import cv2
import mediapipe as mp
import time
from facedetection import face_detection

class handDetector():
    def __init__(self, mode = False, maxHands = 2, detectionCon = 0.7, trackCon = 0.4):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        
    def findcoords(self,img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        self.faces = face_detection(img)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, draw = True):

        lmlist = [[],[],list(self.faces)]         #2 hands 1 face
        if self.results.multi_hand_landmarks:
            for ind, i in enumerate(self.results.multi_hand_landmarks):
                if(ind>1):
                    break
                for id, lm in enumerate(i.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmlist[ind].append([cx, cy])
        if(lmlist[-1]==[]):
            lmlist[-1] = [0, 0, 0, 0]
        if(lmlist[0]==[]):
            lmlist[0] = [0 for i in range(42)]
        else:
            lmlist[0] = list(itertools.chain(*lmlist[0]))
        if(lmlist[1]==[]):
            lmlist[1] = [0 for i in range(42)]
        else:
            lmlist[1] = list(itertools.chain(*lmlist[1]))
        lmlist=lmlist[0]+lmlist[1]+lmlist[2]
        return lmlist

def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()

    while True:
        success, img = cap.read()
        img = detector.findcoords(img)
        lmlist = detector.findPosition(img)
        if len(lmlist) != 0:
            print(len(lmlist[0]))

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()