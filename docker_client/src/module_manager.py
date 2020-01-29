from system_mode_manager import SystemModeManager 
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
    
    def _kill_process(self):
        if self.current_process != None:
            self.current_process.kill()
            
    def load(self):
        #python_command = self._get_python_commandd()
        self._kill_process()
        
        if self.code == EnumModules.BABY:
           self.current_process = subprocess.call(['x-terminal-emulator', '-e', 'python3 module_baby.py'])
        elif self.code == EnumModules.INTRUSION:
          self.current_process = subprocess.call(['x-terminal-emulator', '-e', 'python3 module_intrusion.py'])
        

if __name__ == "__main__":
    app  = ModuleManager()
    app.load()
