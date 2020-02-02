from github_pusher import GithubPusher
import shutil
import sys
import time
import os
from video_recorder import VideoRecorder
class BabyCryPusher:
    
    def __init__(self):
        self.githubPusher = GithubPusher()
        self.videoRecorder = VideoRecorder()
    
    def push(self, intrusion_id):
        
        print("pusing the sound of the baby's crying")
        
        dir_path = "baby_predictor/temp1/"
        
        src_recorded_file = dir_path + "record.wav"
        print("src_recorded_file :", src_recorded_file)
        dst_recorded_file = dir_path + intrusion_id + ".wav"
        if os.path.isfile(src_recorded_file) == False:
            print("File doesn't exist")
        else:
            shutil.copy(src_recorded_file,dst_recorded_file)
            print("push file to github")
            self.githubPusher.push(dst_recorded_file)
            print("delete intrusion duplicated file")
            os.remove(dst_recorded_file)
        
        print("pusing the video of the baby's crying")
        dir_path = "intrusion_videos/"
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print("videos folder created")
        
        video_recorder_file = dir_path + intrusion_id + ".avi"
        
        print("recording video...")
        self.videoRecorder.record(video_recorder_file)
        
        print("push to github")
        self.githubPusher.push(video_recorder_file)
        
if __name__ == "__main__":
    #print("sys.argv[1] :", sys.argv[1])
    if len(sys.argv) < 2:
        print('baby_intrusion_error must be provided')
        sys.exit('Error: Incorrect Usage.')
    try:
        app  = BabyCryPusher()
        print("push...")
        app.push(sys.argv[1])
        #app.push("5e371df2d3f9a77999a082c9")
    except Exception as e:
        print(e)
        
    
    
            
        
    