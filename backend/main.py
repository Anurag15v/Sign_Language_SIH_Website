import time
import tensorflow as tf
import numpy as np
import pickle
import cv2
from coordinates import handDetector
import keyboard
import statistics
import openai
import pyttsx3
import os
openai.api_key = "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"
# initialise the pyttsx3 engine 
engine = pyttsx3.init() 
os.environ['lastword'] = ''



def make_sentence():
    global blackboard

    response = openai.Completion.create(
            engine="text-davinci-002",
            prompt="Correct this to standard English: {}".format(' '.join(blackboard)+'.'),
            temperature=0,
            max_tokens=60,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
    sentence = response["choices"][0]["text"]
    print(sentence)
    return sentence


def say(text):


    # convert text to speech 
    engine.say(text) 
    engine.runAndWait()




prediction_stack = ['-' for i in range(5)]
blackboard = []
l = 10


def display():
    global prediction_stack
    global blackboard
    global l
    try:
        if(len(prediction_stack) > l):
            word = statistics.mode(prediction_stack[-l:])
            if(len(blackboard) == 0 or word!=blackboard[-1]):
                blackboard.append(word)
                os.environ['lastword'] = word
    except:
        pass
    print(blackboard)




def predict_show():
    global prediction_stack, l
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    model = tf.keras.models.load_model("./my_model")
    pTime = 0

    with open("labels.pkl", "rb") as f:
        labels = pickle.load(f)
    while True:
        if keyboard.is_pressed('enter'):
            say(make_sentence())
        if keyboard.is_pressed('backspace'):
            if(len(blackboard)==0):continue
            w = blackboard.pop()
            prediction_stack = ['-' for i in range(5)]
            print(blackboard)
        success, img = cap.read()
        img = detector.findcoords(img)
        lmlist = detector.findPosition(img)
        if(lmlist[0] != 0):         #no hands detected          
            y = model.predict(np.array(lmlist).reshape(1, -1))
            result = labels[np.argmax(y.flatten())]
            prediction_stack.append(result)
            display()
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, os.getenv('lastword'), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)
        if keyboard.is_pressed('q'):
            break




if __name__ == '__main__':
    predict_show()