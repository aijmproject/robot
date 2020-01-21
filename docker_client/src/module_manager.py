from system_mode_manager import SystemModeManager 
#from module_intrusion_moc import IntrusionDetectorMoc
#from module_baby_moc import BabyCryDetectorMoc
#from module_main import Listener
import subprocess
from enum_modules import EnumModules
import os
import signal
class ModuleManager:
    def __init__(self):
        self.code =  0
        self.systemModeManager = SystemModeManager()
        self.current_process = None
        
    
    def switch_to_module(self, code):
        self.code = code
        self.systemModeManager.set_system_mode(code)
        self.load()

    def load(self):
        if self.current_process != None:
            self.current_process.kill()
        if self.code == EnumModules.BABY:
           self.current_process = subprocess.Popen('python module_baby_moc.py', creationflags=subprocess.CREATE_NEW_CONSOLE)
        elif self.code == EnumModules.INTRUSION:
          self.current_process =  subprocess.Popen('python module_intrusion_moc.py', creationflags=subprocess.CREATE_NEW_CONSOLE)
        #elif self.code == EnumModules.CONTROLLER:
        #    self.current_process.kill()
        #elif self.code == 3:


        
        """
         while True:
            if self.code == 0:
                self.code = self.listener.check()
            elif self.code == 1:
                self.code = self.babyCryDetectorMoc.check()
            elif self.code == 2:
                self.code = self.intrusionDetectorMoc.check()
        """
       

if __name__ == "__main__":
    app  = ModuleManager()
    app.load()