import RPi.GPIO as GPIO
import time 
import datetime
import cv2
import numpy as np
from video_recorder import VideoRecorder
from utils import GlobalUtils
from faces_detection_moc import FacesDetectorMoc
from surveillance_db_api import SurveillanceDbAPI
from storage_api.azure_uploader_files import AzureUploaderFiles
from system_mode_manager import SystemModeManager
from face_recognition.surveillance_class import FaceDetection
import sklearn
import os
from github_pusher import GithubPusher
from result_recognizer import ResultUsersRecognizer
from module_text_to_speech import TextToSpeech
from response_random_provider import ResponseRandomProvider
class IntrusionDetector:
    def __init__(self):
        # GPIO module, dynamically loaded depending on config
        self.GPIO = GPIO
        self.videoRecorder = VideoRecorder()
        self.facesDetectorMoc = FacesDetectorMoc()
        #self.sceneDescriptorMoc = SceneDescriptorMoc()
        self.surveillanceDbAPI = SurveillanceDbAPI()
        self.systemModeManager = SystemModeManager()
        self.faceDetection = FaceDetection()
        self.azureUploaderFiles = AzureUploaderFiles()
        self.githubPusher = GithubPusher()
        self.usersRecognizer = ResultUsersRecognizer()
        self.textToSpeech = TextToSpeech()
        self.responseRandomProvider = ResponseRandomProvider()
    
    def my_callback(self, channel): #Fonction appelé dès lors détection d'un mouvement
        print('Mouvement detecte') #Affichage dans le terminal
        #date = datetime.datetime.now() #Récupération de la date et de l'heure actuelle
        #print(date.strftime("%d-%m-%Y %H:%M:%S")) #Affichage de la date et l'heure du mouvement
        
        dir_path = "intrusion_videos/"
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print("videos folder created")
        
        video_recorder_file = dir_path + GlobalUtils.randomString() + ".avi"
        #video_recorder_file = "videos/aqcenzraeh.avi"
        #record for 1 minutes
        print("recording video...")
        self.videoRecorder.record(video_recorder_file)

        #UPLOAD video
        print("faces detection...")
        users_list = self.faceDetection.run_video(video_recorder_file)
        code_result,users_list = self.usersRecognizer.get_recognized_result(users_list)
        if code_result == 3:
            self.textToSpeech.speak(self.responseRandomProvider.get_intrusion_and_reidentification())
            #call reidentification video method
            #todo
            
        seperator = ', '
        users_list_str = seperator.join(users_list)

        print("adding intrusion on databse...")
        result =  self.surveillanceDbAPI.add_new_intrusion("Intrusion", "-", users_list_str, "-")
        #print("_id :", result.inserted_id)
        #self.systemModeManager.set_system_mode(EnumModules.CONTROLLER)

        print("uploading to azure storage...")
        azure_file_name = "{0}{1}.avi".format(dir_path, result.inserted_id)
        os.rename(video_recorder_file,azure_file_name)
        #self.azureUploaderFiles.upload(azure_file_name)
        print("push to github")
        self.githubPusher.push(azure_file_name)

        print("wait 20 minutes before continue checking")
        time.sleep(1200)
        

    def check(self):
        gpio = 7
        
        self.GPIO.setmode(self.GPIO.BCM)
        
        self.GPIO.setup(gpio, self.GPIO.IN)
        
        try:
            self.GPIO.add_event_detect(gpio , self.GPIO.RISING, callback=self.my_callback) #Essaye de détecter un événement (mouvement) sur le pin, s'il y a une impultion électrique alors on appelle la fonction my_callback
            while True:
                time.sleep(10)
        except KeyboardInterrupt:
            print ("Finish...") #Affiche dès lors du "crt+C"
        self.GPIO.cleanup()
        return 0
    
if __name__ == "__main__":
    app  = IntrusionDetector()
    print("check...")
    app.check()