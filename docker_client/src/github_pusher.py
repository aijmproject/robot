import os
class GithubPusher:
    def __init__(self):
        self.username = "KIBASSA"
        self.password = "Justforgithub130589_"
        self.repo = "aijmproject/robot.git"
        
    def push(self, file):
        os.system("git config remote.origin.url https://{0}:{1}@github.com/{2}".format(self.username, self.password,self.repo))
        print("pull")
        os.system("git pull")
        print("add file...")
        os.system("git add {0}".format(file))
        print("commit...")
        os.system("git commit -m 'automation commit'")
        print("push")
        os.system("git push -u origin master")
    