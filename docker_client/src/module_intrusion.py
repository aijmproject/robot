import RPI.GIPO as GPIO
import time 
import datetime
import cv2
import numpy as np
from video_recorder import VideoRecorder
from utils import GlobalUtils
from faces_detection_moc import FacesDetectorMoc
from client_db_api.surveillance_db_api import SurveillanceDbAPI
from storage_api.azure_uploader_files import AzureUploaderFiles
from system_mode_manager import SystemModeManager
class IntrusionDetector(Listener):
    def __init__(self):
        # GPIO module, dynamically loaded depending on config
        self.GPIO = None
        self.videoRecorder = VideoRecorder()
        self.facesDetectorMoc = FacesDetectorMoc()
        self.sceneDescriptorMoc = SceneDescriptorMoc()
        self.surveillanceDbAPI = SurveillanceDbAPI()
        self.systemModeManager = SystemModeManager()
        #self.faceDetection = FaceDetection()
        self.azureUploaderFiles = AzureUploaderFiles()


    def check(self):
        gpio = 26
        self.GPIO.setmode(self.GPIO.BOARD)
        self.GPIO.setup(gpio, self.GPIO.IN)
        while True:
            pir = self.GPIO.input(gpio)
            if pir == 0:
                # no motion detected
                time.sleep(1)
                continue
            
            video_recorder_file = "videos/" + GlobalUtils.randomString() + ".avi"
            #record for 1 minutes
            print("recording video...")
            self.videoRecorder.record(video_recorder_file)

            #UPLOAD video
            print("faces detection...")
            #users_list = self.faceDetection.(video_recorder_file)
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