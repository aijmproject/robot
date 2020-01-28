import os
class GithubPusher:
    #def __init__(self):
    
    def push(self, file):
        
        print("pull")
        os.system("git pull")
        print("add file...")
        os.system("git add {0}".format(file))
        print("commit...")
        os.system("git commit -m 'automation commit'")
        print("push")
        os.system("git push -u origin master")
    