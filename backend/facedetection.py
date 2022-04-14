import cv2

def face_detection(image):
    '''
    Detects faces in an image and returns the bounding boxes [x, y, w, h]
    if not found, returns []
    '''
    if image is not None:
        # Convert image to grayscale
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Create Cascade Classifiers
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        
        # Detect faces using the classifiers
        detected_faces = face_cascade.detectMultiScale(image=image, scaleFactor=1.3, minNeighbors=4)

        if len(detected_faces)>0:
            detected_faces[0][2] += detected_faces[0][0]
            detected_faces[0][3] += detected_faces[0][1]
            return  detected_faces[0]           #returns x, y, w, h
        else:
            return []