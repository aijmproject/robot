import time
from client_db_api.surveillance_db_api import SurveillanceDbAPI
from module_main import Listener
class BabyCryDetectorMoc(Listener):
    def __init__(self):
        Listener.__init__(self)
        self.surveillanceDbAPI = SurveillanceDbAPI()


    def launch_specific_task(self):
        print("BabyCryDetectorMoc --")

    #def check(self):
    #    print("BabyCryDetectorMoc : test")
    #    time.sleep(30)
    #    return 1
    """
    def check(self):
        while True:
            time.sleep(60)
            self.surveillanceDbAPI.add_new_intrusion("bebe", "pleurer","bebe","-" )
    """
    
