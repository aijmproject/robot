from system_mode_manager import SystemModeManager 
from module_intrusion_moc import IntrusionDetectorMoc
from module_baby_moc import BabyCryDetectorMoc
from module_main import Listener

class ModuleManager:
    def __init__(self):
        self.code =  0
        self.systemModeManager = SystemModeManager()
        self.babyCryDetectorMoc = BabyCryDetectorMoc()
        self.intrusionDetectorMoc = IntrusionDetectorMoc()
        self.listener = Listener()
    
    def load(self):
        while True:
            if self.code == 0:
                self.code = self.listener.check()
            elif self.code == 1:
                self.code = self.babyCryDetectorMoc.check()
            elif self.code == 2:
                self.code = self.intrusionDetectorMoc.check()

if __name__ == "__main__":
    app  = ModuleManager()
    app.load()
