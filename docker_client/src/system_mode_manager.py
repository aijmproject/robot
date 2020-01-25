
from client_db_api.surveillance_db_api import SurveillanceDbAPI

#bebe 1
#intrusion 2
#controller 3

class SystemModeManager:
    def __init__(self):
        self.surveillancedb  = SurveillanceDbAPI()
        self.current_mode = self.surveillancedb.get_last_system_mode()["mode"]
        self.local_id = self.surveillancedb.get_last_system_mode()["_id"] 
    
    def is_current_mode(self):
        return self.surveillancedb.get_last_system_mode()["mode"] == self.current_mode
    
    def set_system_mode(self, mode):
        print("set_system_mode :---", mode)
        self.surveillancedb.update_system_mode(self.local_id, mode)
        self.current_mode = self.surveillancedb.get_last_system_mode()["mode"]

    def get_current_mode(self):
        return self.surveillancedb.get_last_system_mode()["mode"]