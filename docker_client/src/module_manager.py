from system_mode_manager import SystemModeManager 
import subprocess
from enum_modules import EnumModules
import os
import signal
from platform import python_version
import psutil, os,signal
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
        print("check if current_process is open")
        if self.current_process != None:
            print("kill current process : ", self.current_process.pid)
            self.infanticide(psutil.Process(self.current_process.pid).ppid())
            #os.kill(self.current_process.pid, signal.SIGKILL)
            #self.current_process.kill()
            
            
    def infanticide(self,pid):
        try:
          parent = psutil.Process(pid)
        except psutil.NoSuchProcess:
          return
        children = parent.children(recursive=True)
        for p in children:
            os.kill(p.pid, signal.SIGKILL)
            os.kill(p.pid, signal.SIGHUP)
            
    def kill_child_processes(self, parent_pid, sig=signal.SIGTERM):
        ps_command = subprocess.Popen("ps -o pid --ppid %d --noheaders" % parent_pid, shell=True, stdout=subprocess.PIPE)
        ps_output = ps_command.stdout.read()
        retcode = ps_command.wait()
        assert retcode == 0, "ps command returned %d" % retcode
        for pid_str in ps_output.split("\n")[:-1]:
                os.kill(int(pid_str), sig)
                
    def load(self):
        #python_command = self._get_python_commandd()
        self._kill_process()
        
        if self.code == EnumModules.BABY:
            print("Chargement du module bébé")
            self.current_process = subprocess.Popen(['x-terminal-emulator', '-e', 'python3 module_baby.py'])
        elif self.code == EnumModules.INTRUSION:
            print("Chargement du module intrusion")
            self.current_process = subprocess.Popen(['x-terminal-emulator', '-e', 'python3 module_intrusion.py'])
        
        #print("current process : ",psutil.Process(self.current_process.pid).ppid())
        

if __name__ == "__main__":
    app  = ModuleManager()
    app.load()
