
from client_db_api.surveillance_db_api import SurveillanceDbAPI
#controller 0
#bebe 1
#intrusion 2
class SystemModeManager:
    def __init__(self):
        self.surveillancedb  = SurveillanceDbAPI()
        self.current_mode = self.surveillancedb.get_last_system_mode()["mode"]
    
    def is_current_mode(self):
        return self.surveillancedb.get_last_system_mode()["mode"] == self.current_mode
    
    def set_system_mode(self, mode):
        self.surveillancedb.add_new_system_mode(mode)
        self.current_mode = self.surveillancedb.get_last_system_mode()["mode"]

    def get_current_mode(self):
        return self.surveillancedb.get_last_system_mode()["mode"]