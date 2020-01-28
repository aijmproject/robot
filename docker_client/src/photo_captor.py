#import pyb
#from VideoCapture import Device
from system_mode_manager import SystemModeManager
from storage_api.azure_uploader_files import AzureUploaderFiles
import sched, time
import cv2
#from cv2 import cv
import time
import os
class PhotoCaptor:
    def __init__(self):
        self.systemModeManager = SystemModeManager()
        self.azureUploaderFiles = AzureUploaderFiles()
        self.sched = sched.scheduler(time.time, time.sleep)
        self.sched.enter(30, 30, self.tick, (self.sched,))
        self.sched.run()

    def tick(self,sched):
        #print("tick")
        current_mode = self.systemModeManager.get_current_mode()
        #current_mode = 1

        dir_path = "screenshot_temp/"
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        file_name = ""
        if current_mode == 1:
            file_name = dir_path + 'bebe.jpg'
        elif current_mode == 2:
            file_name = dir_path + 'intrusion.jpg'
        
        if len(file_name) == 0:
            return
        
        vidcap = cv2.VideoCapture(0)
        success,image = vidcap.read()
        cv2.imwrite(file_name, image)
        vidcap.release()

        self.azureUploaderFiles.upload_photo(file_name)
        self.sched.enter(30, 30, self.tick, (sched,))

if __name__ == "__main__":
    app  = PhotoCaptor()
    print("check...")
    #app.check()