import cv2
import numpy as np
import face_recognition
import os

# Image to match encoding
path = "Images"
images = []
classNames = []
myList = os.listdir(path)

for cl in myList:
    currentImg = cv2.imread(f'{path}/{cl}')
    images.append(currentImg)
    classNames.append(os.path.splitext(cl)[0])

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodeListKnown = findEncodings(images)

# Camera Initialization
capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FPS, 60) # FPS for the camera

while True:
    success, img = capture.read()
    imgSize = cv2.resize(img, (0,0), None, 0.25, 0.25)
    imgSize = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    facesCurrentFrame = face_recognition.face_locations(imgSize)
    encodesCurrentFrame = face_recognition.face_encodings(imgSize, facesCurrentFrame)

    for encodeFace, faceLoc in zip(encodesCurrentFrame, facesCurrentFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDistance = face_recognition.face_distance(encodeListKnown, encodeFace)
        # print(faceDistance)
        matchIndex = np.argmin(faceDistance)


        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            print(name) # Pwede to tanggalin, pang testing lang
            y1, x2, y2, x1 = faceLoc
            # cv2.rectangle(img, (x1,y1), (x2,y2), (0,255,0), 2)
            # cv2.rectangle(img, (x1, y2-35), (x2,y2), (0,255,0), cv2.FILLED)
            # cv2.putText(img, name, (x1+6,y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)
    
    cv2.imshow('Webcam', img)
    cv2.waitKey(1)

 

