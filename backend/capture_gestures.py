import time
import cv2
from coordinates import handDetector
import pickle
import numpy as np
def main():
    gesture = input("Enter gesture: ")
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    to_save = []
    ctr = 0
    time.sleep(10)
    while True:
        ctr+=1
        if ctr==600:
            break
        print(ctr)
        success, img = cap.read()
        img = detector.findcoords(img)
        lmlist = detector.findPosition(img)


        if len(lmlist) != 0:
            to_save.append(lmlist)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)
    with open("./gestures/{}.pkl".format(gesture), "wb") as f:
        pickle.dump(to_save, f)


if __name__ == '__main__':
    main()
