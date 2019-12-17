#https://www.framboise314.fr/i-a-realisez-un-systeme-de-reconnaissance-dobjets-avec-raspberry-pi/ in case xd
# tuto face recognition (18 images xd ) : https://www.pyimagesearch.com/2018/09/24/opencv-face-recognition/


#check only personne if first time
#see how mutch tolerence i want 
import cv2
import numpy as np
import dlib
import json
import operator
# other py file 
from client_db_api.surveillance_db_api import SurveillanceDbCreator
from face_comparator import FaceComparator
from module_text_to_speech import TextToSpeech



def landmarktesting(landmarks_input, allusers):
    """
    ladtesters dois resemblé à une base de donnée mongodb
    """
    resemblance = {}
    for item in allusers:
        
        item['landmarks']  = json.loads(item['landmarks'])
        results =  faceComparator.face_distance(np.asarray(item['landmarks']),np.asarray(landmarks_input))
        results = np.array(results)
        # pourcentage True dans mon résultat APRES le choix de la tolérance, il vas faloir y réflechir plus à ce sujet.
        accruacy_detection = (np.sum(results)/results.size)*100
        resemblance[item['name']] =  round(accruacy_detection)
    best_result = max(resemblance.items(), key=operator.itemgetter(1))
    return resemblance, best_result







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
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)

        landmarks = predictor(gray, face)
        landmarks_to_saved = []
        for n in range(0, 68):
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            cv2.circle(frame, (x, y), 4, (255, 0, 0), -1)
            landmarks_to_saved.append([x,y])

        allusers_live = surveillance.get_all_live_users()
        allusers_live = list(allusers_live)
        if allusers_live != [] :


            _,best_result = landmarktesting(landmarks_to_saved, allusers_live)
            print(best_result)
            if best_result[1] < 60 :
                print('true')
                surveillance.add_new_live_user(str(len(list(allusers_live))+1),str(landmarks_to_saved))
                new = 1
            else :
                print('false')
                new = 0 
        else :
            print('first')
            surveillance.add_new_live_user('1',str(landmarks_to_saved))
            new = 1
            

        
        if  new == 1 :
            landmarks_input = json.loads('[' + ','.join([str(x) for x in landmarks_to_saved]) + ']')
            allusers = surveillance.get_all_users()
            _, best_result = landmarktesting(landmarks_input, allusers)
            
            if 80 >  best_result[1] > 60:
                textToSpeech.speak("Bonjour Je pense que tu es "+ best_result[0] + " a " + str(best_result[1]))
            elif best_result[1] > 80 :
                textToSpeech.speak("Bonjour tu es "+ best_result[0] + " a " + str(best_result[1]))
            else:
                textToSpeech.speak("Désolé, je ne vous reconnais pas!")
                #ajout du module de junior
                #textToSpeech.speak("Voulez être ajouter à la base de donnée? Oui ou non.")
                
            break

    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        surveillance.drop_live()
        break