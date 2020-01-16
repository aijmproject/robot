

from system_mode_manager import SystemModeManager 
from intrusion_module_moc import IntrusionDetectorMoc
from baby_module_moc import BabyCryDetectorMoc
from listener import Listener
class ModuleManager:
    def __init__(self):
        self.systemModeManager = SystemModeManager()
        self.babyCryDetectorMoc = BabyCryDetectorMoc()
        self.intrusionDetectorMoc = IntrusionDetectorMoc()
        self.listener = Listener()
    
    def change_module(self):
        return self.systemModeManager.is_current_mode() 

    def switch_to_module(self, mode):
        self.systemModeManager.set_system_mode(mode)
        self._launch_module(mode)
        print("current module loaded")

    def _launch_module(self, code):
        if code == 0:
            self.listener.listen()
        elif code == 1:
            self.babyCryDetectorMoc.check()
        elif code == 2:
            self.intrusionDetectorMoc.check()        

    def load_module(self):
        mode = self.systemModeManager.get_current_mode()
        self._launch_module(mode)
        print("current module loaded")

