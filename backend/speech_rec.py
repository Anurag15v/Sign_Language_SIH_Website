import os
import speech_recognition as sr  
import os

# get audio from the microphone                                                                       
r = sr.Recognizer()                                                                                   
with sr.Microphone() as source:                                                                       
    print("Speak:")                                                                                   
    audio = r.listen(source)   

try:
    text = (r.recognize_google(audio))
    print(text)
    splitted_text = text.split(' ')
    for i in splitted_text:
        for j in os.listdir('./sign_images/'):
            if j[:-4] == i:
                os.system('./sign_images/'+j)
except sr.UnknownValueError:
    print("Could not understand audio")
except sr.RequestError as e:
    print("Could not request results; {0}".format(e))