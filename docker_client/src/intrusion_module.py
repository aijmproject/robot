import RPI.GIPO as GPIO
import time 
import datetime
import cv2
import numpy as np
from video_recorder import VideoRecorder
from utils import GlobalUtils
from faces_detection_moc import FacesDetectorMoc
from client_db_api.surveillance_db_api import SurveillanceDbAPI
class IntrusionDetector:
    def __init__(self):
        # GPIO module, dynamically loaded depending on config
        self.GPIO = None
        self.videoRecorder = VideoRecorder()
        self.facesDetectorMoc = FacesDetectorMoc()


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
            
            video_recorder_file = GlobalUtils.randomString() + ".wav"
            #record for 1 minutes
            self.videoRecorder.record(video_recorder_file)

            users_list = self.facesDetectorMoc.detect_faces(video_recorder_file)
            print(users_list)

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