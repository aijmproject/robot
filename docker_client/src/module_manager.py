from system_mode_manager import SystemModeManager 
#from module_intrusion_moc import IntrusionDetectorMoc
#from module_baby_moc import BabyCryDetectorMoc
#from module_main import Listener
import subprocess
from enum_modules import EnumModules
import os
import signal
from platform import python_version
class ModuleManager:
    def __init__(self):
        self.code =  0
        self.systemModeManager = SystemModeManager()
        self.current_process = None
        
    def switch_to_module(self, code):
        self.code = code
        self.systemModeManager.set_system_mode(code)
        self.load()

    def _get_python_commandd(self):
        if python_version().startswith("2"):
            return "python3"
        return "python"

    def load(self):moduleManager
        python_command = self._get_python_commandd()
        if self.current_process != None:
            self.current_process.kill()
        if self.code == EnumModules.BABY:
           #self.current_process = subprocess.Popen('{0} module_baby_moc.py'.format(python_command), creationflags=subprocess.CREATE_NEW_CONSOLE)
           #self.current_process = subprocess.Popen('python3 module_baby_moc.py'.format(python_command), shell=True)
           #os.system("x-terminal-emulator -e python3 module_baby_moc.py;".format(python_command))
           self.current_process = subprocess.call(['x-terminal-emulator', '-e', 'python3 module_baby_moc.py'])
        elif self.code == EnumModules.INTRUSION:
          #self.current_process =  subprocess.Popen('{0} module_intrusion_moc.py'.format(python_command), creationflags=subprocess.CREATE_NEW_CONSOLE)
          #self.current_process =  subprocess.Popen('python3 module_intrusion_moc.py'.format(python_command), shell=True)
          #os.system("x-terminal-emulator -e python3 module_intrusion_moc.py;".format(python_command))
          self.current_process = subprocess.call(['x-terminal-emulator', '-e', 'python3 module_intrusion.py'])
        #elif self.code == EnumModules.CONTROLLER:
        #    self.current_process.kill()
        #elif self.code == 3:
       

if __name__ == "__main__":
    app  = ModuleManager()
    #app.code = 2
    #app.switch_to_module(2)
    app.load()
