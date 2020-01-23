import time 
import datetime
from video_recorder import VideoRecorder
from utils import GlobalUtils
from faces_detection_moc import FacesDetectorMoc
from scene_descriptor_moc import SceneDescriptorMoc
from client_db_api.surveillance_db_api import SurveillanceDbAPI
from system_mode_manager import SystemModeManager
from enum_modules import EnumModules
#from  import 
#from face-recognition.surveillance_class import FaceDetection
from storage_api.azure_uploader_files import AzureUploaderFiles
#from module_main import Listener
import time
import os
class IntrusionDetectorMoc():
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
        while True:
            f = open("PIR.txt", "r")
            detect = f.read()
            if detect == "1":
                
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

if __name__ == "__main__":
    app  = IntrusionDetectorMoc()
    print("check...")
    app.check()