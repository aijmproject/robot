import time
from client_db_api.surveillance_db_api import SurveillanceDbAPI
from system_mode_manager import SystemModeManager 
from baby_predictor.cry_predictor import BabyCryPredictor
from system_mode_manager import SystemModeManager
from enum_modules import EnumModules

class BabyCryDetectorMoc():
    def __init__(self):
        self.surveillanceDbAPI = SurveillanceDbAPI()
        self.systemModeManager = SystemModeManager()
        self.babyCryPredictor = BabyCryPredictor()

    def listen(self):
        while True:
            pred = self.babyCryPredictor.predict()
            if pred == True:
                self.surveillanceDbAPI.add_new_intrusion("BABY", "-", "BABY", "-")
                self.systemModeManager.set_system_mode(EnumModules.CONTROLLER)
                break
            else:
                time.sleep(10)

if __name__ == "__main__":
    app  = BabyCryDetectorMoc()
    print("à l'écoute")
    app.listen()