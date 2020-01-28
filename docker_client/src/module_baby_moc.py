# coding=utf-8
import time
from surveillance_db_api import SurveillanceDbAPI
from system_mode_manager import SystemModeManager 
from baby_predictor.cry_predictor import BabyCryPredictor
from system_mode_manager import SystemModeManager
from enum_modules import EnumModules

class BabyCryDetectorMoc():
    def __init__(self):
        self.surveillanceDbAPI = SurveillanceDbAPI()
        self.systemModeManager = SystemModeManager()
        self.babyCryPredictor = BabyCryPredictor("baby_predictor/")

    def listen(self):
        while True:
            try:
                pred = self.babyCryPredictor.predict()
                print("pred:", pred)
                if pred == True:
                    self.surveillanceDbAPI.add_new_intrusion("Bébé", "-", "Bébé", "-")
                    print("baby cry loading module....")
                    self.systemModeManager.set_system_mode(EnumModules.CONTROLLER)
                    break
                    #time.sleep(1200)
                else:
                    time.sleep(10)
            except Exception as e:
                print(e)
        
            
if __name__ == "__main__":
    app  = BabyCryDetectorMoc()
    print("à l'écoute")
    app.listen()
    