import time 
import datetime
from video_recorder import VideoRecorder
from utils import GlobalUtils
from faces_detection_moc import FacesDetectorMoc
from scene_descriptor_moc import SceneDescriptorMoc
from client_db_api.surveillance_db_api import SurveillanceDbAPI
from system_mode_manager import SystemModeManager
#from module_main import Listener
import time

class IntrusionDetectorMoc():
    def __init__(self):
        # GPIO module, dynamically loaded depending on config
        self.GPIO = None
        self.videoRecorder = VideoRecorder()
        self.facesDetectorMoc = FacesDetectorMoc()
        self.sceneDescriptorMoc = SceneDescriptorMoc()
        self.surveillanceDbAPI = SurveillanceDbAPI()
        self.systemModeManager = SystemModeManager()

    def check(self):
        while True:
            f = open("PIR.txt", "r")
            detect = f.read()
            if detect == "1":
                time.sleep(5)

                video_recorder_file = "videos/" + GlobalUtils.radnomString() + ".avi"
                #record for 1 minutes
                self.videoRecorder.record(video_recorder_file)

                #UPLOAD video
                users_list = self.facesDetectorMoc.detect_faces(video_recorder_file)
                seperator = ', '
                users_list_str = seperator.join(users_list)

                self.surveillanceDbAPI.add_new_intrusion("INTRUSION", "-", users_list_str, "-")
                self.systemModeManager.set_system_mode(EnumModules.CONTROLLER)
                
                break

if __name__ == "__main__":
    app  = IntrusionDetectorMoc()
    print("check...")
    app.check()