#https://www.framboise314.fr/i-a-realisez-un-systeme-de-reconnaissance-dobjets-avec-raspberry-pi/ in case xd
# tuto face recognition (18 images xd ) : https://www.pyimagesearch.com/2018/09/24/opencv-face-recognition/

"""
import numpy as np
import cv2 #pip install opencv-python
import dlib #conda install -c conda-forge dlib
xml_path = 'opencv_models/'
face_cascade = cv2.CascadeClassifier(xml_path+'haarcascade_frontalface_alt2.xml')
eye_cascade = cv2.CascadeClassifier(xml_path+'haarcascade_eye.xml')
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

cap = cv2.VideoCapture(0) #change number by file if want to use video file

ret = cap.set(3,640+320)
ret = cap.set(4,240+480)
print("hi")
while(cap.isOpened()): # check if my Videocapture is open 
    # Capture frame-by-frame
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors = 5)
    eye = eye_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors = 5)
    for (x,y,w,h) in faces :
        frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)

        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

        landmarks = predictor(gray, (x,y,w,h))

        #authent_users = mongo_api.get_users()
        #if len(authent_users) > 0:
        #

        if cv2.waitKey(0) == 27:
            print(landmarks)
            break

    # Display the resulting frame
    #cv2.imshow('gray',gray)
    cv2.imshow('frame',frame)
    
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
"""
import cv2
import numpy as np
import dlib

cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(gray)
    for face in faces:
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()
        #cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)

        landmarks = predictor(gray, face)
        #print(landmarks)
        for n in range(0, 68):
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            cv2.circle(frame, (x, y), 4, (255, 0, 0), -1)
            print(x,"----",y)


    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break