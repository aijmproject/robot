import time
from client_db_api.surveillance_db_api import SurveillanceDbAPI

class BabyCryDetectorMoc:
    def __init__(self):
        self.surveillanceDbAPI = SurveillanceDbAPI()


    def launch_specific_task(self):
        print("BabyCryDetectorMoc")

    """
    def check(self):
        while True:
            time.sleep(60)


            self.surveillanceDbAPI.add_new_intrusion("bebe", "pleurer","bebe","-" )
    """
    
