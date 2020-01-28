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
class IntrusionDetector:
    def __init__(self):
        print("sklearn.__version__", sklearn.__version__)
        # GPIO module, dynamically loaded depending on config
        self.GPIO = GPIO
        self.videoRecorder = VideoRecorder()
        self.facesDetectorMoc = FacesDetectorMoc()
        #self.sceneDescriptorMoc = SceneDescriptorMoc()
        self.surveillanceDbAPI = SurveillanceDbAPI()
        self.systemModeManager = SystemModeManager()
        self.faceDetection = FaceDetection()
        self.azureUploaderFiles = AzureUploaderFiles()
        
    def my_callback(self, channel): #Fonction appelé dès lors détection d'un mouvement
        print('Mouvement detecte') #Affichage dans le terminal
        #date = datetime.datetime.now() #Récupération de la date et de l'heure actuelle
        #print(date.strftime("%d-%m-%Y %H:%M:%S")) #Affichage de la date et l'heure du mouvement
        
        dir_path = "videos/"
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print("videos folder created")
        
        video_recorder_file = "videos/" + GlobalUtils.randomString() + ".avi"
        #video_recorder_file = "videos/aqcenzraeh.avi"
        #record for 1 minutes
        print("recording video...")
        self.videoRecorder.record(video_recorder_file)

        #UPLOAD video
        print("faces detection...")
        users_list = self.faceDetection.run_video(video_recorder_file)
        print(users_list)
        #break
        return 0
        users_list = ["inconnu"]
        seperator = ', '
        users_list_str = seperator.join(users_list)

        print("adding intrusion on databse...")
        result =  self.surveillanceDbAPI.add_new_intrusion("Intrusion", "-", users_list_str, "-")
            #print("_id :", result.inserted_id)
            #self.systemModeManager.set_system_mode(EnumModules.CONTROLLER)

        print("uploading to azure storage...")
        azure_file_name = "videos/{0}.avi".format(result.inserted_id)
        os.rename(video_recorder_file,azure_file_name)
        self.azureUploaderFiles.upload(azure_file_name)

        print("wait 20 minutes before continue checking")
        time.sleep(1200)
        

    def check(self):
        time.sleep(4)
        gpio = 7
        
        self.GPIO.setmode(self.GPIO.BCM)
        
        self.GPIO.setup(gpio, self.GPIO.IN)
        
        try:
            self.GPIO.add_event_detect(gpio , self.GPIO.RISING, callback=self.my_callback) #Essaye de détecter un événement (mouvement) sur le pin, s'il y a une impultion électrique alors on appelle la fonction my_callback
            while True:
                time.sleep(100)
        except KeyboardInterrupt:
            print ("Finish...") #Affiche dès lors du "crt+C"
        self.GPIO.cleanup()
        return 0
    
        #while True:
        #    pir = self.GPIO.input(gpio)
        #    print("pir :", pir)
        #    if pir == 1:
        #        # no motion detected
        #        time.sleep(1)
        #        print("time.sleep(1)")
        #        continue gpio = 7
            
            
            #break

            #self.logger.info('PIR: motion detected')
            #if self.config['buzzer']['enable'] and len(buzzer_sequence) > 0:
            #    self.playSequence(buzzer_sequence)
            #args = shlex.split(self.config['pir']['capture_cmd'])

            #try:
            #    subprocess.call(args)
            #except Exception as e:
            #    self.logger.warn(str(e))
            #    self.logger.warn(traceback.format_exc())
            #    message.reply_text('Error: Capture failed: %s' % str(e))
if __name__ == "__main__":
    app  = IntrusionDetector()
    print("check...")
    app.check()