import cv2
import numpy as np
import os
import speech_recognition as sr  # recognise speech
import keyboard


class play:
    def __init__(self):
        self.r = sr.Recognizer()                                                                                   
    def show(self, x):
        cap = cv2.VideoCapture('./sign_images/{}'.format(x))
        
        # Check if camera opened successfully
        if (cap.isOpened()== False): 
            print("Error opening video  file")
        
        # Read until video is completed
        while(cap.isOpened()):
            
            # Capture frame-by-frame
            ret, frame = cap.read()
            if ret == True:
            
                # Display the resulting frame
                try:
                    ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
                    frame = buffer.tobytes()
                    yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                except Exception as e:
                    pass
            # Break the loop
            else: 
                pass
        
        # When everything done, release 
        # the video capture object
        cap.release()
    
    # Closes all the frames
    # cv2.destroyAllWindows()

    # get audio from the microphone                                                                       
    def recognize(self):
        r = self.r
        with sr.Microphone() as source:                                                                       
            print("Speak:")                                                                                   
            # audio = r.listen(source)   

        try:
            # text = (r.recognize_google(audio))
            text = "how are you"
            print(text)
            splitted_text = text.split(' ')
            for i in splitted_text:
                for j in os.listdir('./sign_images/'):
                    if j[:-4] == i:
                        self.show(j)
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))