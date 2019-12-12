#https://www.framboise314.fr/i-a-realisez-un-systeme-de-reconnaissance-dobjets-avec-raspberry-pi/ in case xd
# tuto face recognition (18 images xd ) : https://www.pyimagesearch.com/2018/09/24/opencv-face-recognition/

import cv2
import numpy as np
import dlib
import json
from client_db_api.surveillance_db_api import SurveillanceDbCreator
from face_comparator import FaceComparator
from module_text_to_speech import TextToSpeech

cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

surveillance = SurveillanceDbCreator()
faceComparator = FaceComparator()
textToSpeech = TextToSpeech()
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
        landmarks_to_saved = []
        for n in range(0, 68):
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            cv2.circle(frame, (x, y), 4, (255, 0, 0), -1)
            landmarks_to_saved.append([x,y])
        
        
        landmarks_input = json.loads('[' + ','.join([str(x) for x in landmarks_to_saved]) + ']')
        allusers = surveillance.get_all_users()
        for item in allusers:
            item['landmarks']  = json.loads(item['landmarks'])
            results =  faceComparator.face_distance(np.asarray(item['landmarks']),np.asarray(landmarks_input))
            print(results)
            if results[0] == True:
                textToSpeech.speak("Bonjour "+ item['name'])
            else:
                textToSpeech.speak("Désolé, je ne vous reconnais pas!")
            break

        break    
        
        user = surveillance.get_user_by_landmarks(landmarks_input)

        if user != None:
            print("Bonjour", user.name)
            break
        else:
            f=open("face_reco_junior_landmarks.txt", "w+")
            f.write(';'.join([str(x) for x in landmarks_to_saved]))
            f.close()
            break

        #print(landmarks_to_saved, "------end")

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break