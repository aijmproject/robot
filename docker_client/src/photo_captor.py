#import pyb
#from VideoCapture import Device
from system_mode_manager import SystemModeManager
from storage_api.azure_uploader_files import AzureUploaderFiles
import sched, time
import cv2
#from cv2 import cv
import time
import os
from github_pusher import GithubPusher
class PhotoCaptor:
    def __init__(self):
        self.systemModeManager = SystemModeManager()
        self.azureUploaderFiles = AzureUploaderFiles()
        self.sched = sched.scheduler(time.time, time.sleep)
        self.githubPusher = GithubPusher()
        
    def run(self):
        self.sched.enter(30, 30, self.tick, (self.sched,))
        self.sched.run()
        
    def tick(self,sched):
        current_mode = self.systemModeManager.get_current_mode()
        current_mode = 1

        dir_path = "intrusion_photos/"
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        
        if current_mode == 3:
            return
        
        file_name = "snapshot.jpg"
        
        print("video capture... ")
        vidcap = cv2.VideoCapture(-1)
        success,image = vidcap.read()
        cv2.imwrite(file_name, image)
        vidcap.release()
        #print("upload to azure... ")    
        #self.azureUploaderFiles.upload_photo(file_name)
        print("push to github")
        self.githubPusher.push(file_name)
        self.sched.enter(30, 30, self.tick, (sched,))

if __name__ == "__main__":
    app  = PhotoCaptor()
    print("run...")
    app.run()
    #app.check()