import time 
import datetime
from video_recorder import VideoRecorder
from utils import GlobalUtils
from faces_detection_moc import FacesDetectorMoc
from scene_descriptor_moc import SceneDescriptorMoc
from client_db_api.surveillance_db_api import SurveillanceDbAPI
from listener import Listener
import time

class IntrusionDetectorMoc(Listener):
    def __init__(self):
        # GPIO module, dynamically loaded depending on config
        self.GPIO = None
        self.videoRecorder = VideoRecorder()
        self.facesDetectorMoc = FacesDetectorMoc()
        self.sceneDescriptorMoc = SceneDescriptorMoc()
        self.surveillanceDbAPI = SurveillanceDbAPI()

    def launch_specific_task(self):
        print("IntrusionDetectorMoc")

    """
    def check(self):
        
        time.sleep(30)

        video_recorder_file = GlobalUtils.randomString() + ".wav"
        #record for 1 minutes
        self.videoRecorder.record(video_recorder_file)

        users_list = self.facesDetectorMoc.detect_faces(video_recorder_file)
        print(users_list)

        description = self.sceneDescriptorMoc.describe(video_recorder_file)

        self.surveillanceDbAPI.add_new_intrusion("intrusion", description,users_list,"-")
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
    
    """
    
            
            