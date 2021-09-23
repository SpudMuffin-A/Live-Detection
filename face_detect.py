import cv2 as cv

face_cascade = cv.CascadeClassifier('haar_face.xml')
cap = cv.VideoCapture(0)

while True:
    _, img = cap.read()
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 2)

    for (x, y, w, h) in faces:
        cv.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

    cv.imshow('Video', img)

    k = cv.waitKey(30) & 0xFF
    if k==27:
        break

cap.release()    