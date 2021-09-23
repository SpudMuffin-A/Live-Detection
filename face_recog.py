import cv2 as cv
import numpy as np
haar_cascade = cv.CascadeClassifier('haar_face.xml')

people = ['Tom Cruise', 'Ben Afflek', 'Jerry Seinfeld', 'Madonna', 'Scarlett Johansson', 'Aryan', 'Aarav']

face_recognizer = cv.face.LBPHFaceRecognizer_create()
face_recognizer.read('face_trained.yml')

# img = cv.imread('photos/ im1.jpeg')
cap = cv.VideoCapture(0)
while True:
    _, img = cap.read()
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    faces_rect = haar_cascade.detectMultiScale(gray, 1.1, 1)

    for (x,y,w,h) in faces_rect:
        faces_roi = gray[y:y+h, x:x+w]

        label, confidence = face_recognizer.predict(faces_roi)
        print(f'Label = {people[label]} with a confidence of {confidence}')

        cv.putText(img, str(people[label]), (20,20), cv.FONT_HERSHEY_COMPLEX, 1.0, (0,255,0), thickness=2)
        cv.rectangle(img, (x,y), (x+w, y+h), (0,255,0), thickness=2)

    cv.imshow('Detected Face', img)
    k = cv.waitKey(30) & 0xff
    if k==27:
        break

cap.release()  

