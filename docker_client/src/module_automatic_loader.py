from system_mode_manager import SystemModeManager
from module_manager import ModuleManager
import time
class ModuleAutoLoader:
    def __init__(self):
        self.systemModeManager = SystemModeManager()
        self.moduleManager = ModuleManager()
        self.memory_code = 3
    
    def run(self):
        while True:
            try:
                time.sleep(10) #10 secondes
                self.load()
            except Exception as e:
                print("error :",e)
            
    def load(self):
        current_mode = int(self.systemModeManager.get_current_mode())
        if current_mode != self.memory_code and current_mode != 3:
            self.memory_code = current_mode
            print("switch to current module...")
            self.moduleManager.switch_to_module(current_mode)

if __name__ == "__main__":
    app  = ModuleAutoLoader()
    print("run...")
    app.run()
    #app.check()
        
    