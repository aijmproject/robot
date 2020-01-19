import time
from client_db_api.surveillance_db_api import SurveillanceDbAPI
from system_mode_manager import SystemModeManager 
class BabyCryDetectorMoc():
    def __init__(self):
        #Listener.__init__(self)
        self.surveillanceDbAPI = SurveillanceDbAPI()
        self.systemModeManager = SystemModeManager()

    def launch_specific_task(self):
        print("BabyCryDetectorMoc --")

    def listen(self):

        print("IntrusionDetectorMoc : test")
        for i in range(0,1000):
            #if self.systemModeManager.is_current_mode() == False:
            #    self.moduleManager.load()
            time.sleep(1)
            print(i, "---")
        time.sleep(30)

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
    

if __name__ == "__main__":
    app  = BabyCryDetectorMoc()
    print("à l'écoute")
    app.listen()