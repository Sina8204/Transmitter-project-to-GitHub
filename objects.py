import subprocess

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if stderr:
        print(f">>>  {stderr.decode()}")
    return [stdout.decode() , process]

class ready_command ():
    def __init__(self):
        self.branch = ''
    def git_init (self):
        return run_command("git init")[0]
    #
    def delet_origin (self):
        return run_command("git remote remove origin")[0]
    #
    def add_origin (self , gitHub_address : str):
        self.gitHub_address = gitHub_address
        return run_command(f"git remote add origin {self.gitHub_address}")[0]
    #
    def git_pull (self , branch : str = "master" ):
        self.branch = branch
        return run_command (f"git pull origin {self.branch} --allow-unrelated-histories")[0]
        #after pulling , creat local branch to name self.branch in your VS code at Source Control
    #
    def creat_LocalBranch (self):
        return run_command (f'git checkout -b {self.branch}')[0]

    def git_add (self):
        return run_command("git add .")[0]
    #
    def git_commit (self , message : str):
        self.message = message
        return run_command (f'git commit -m "{self.message}"')[0]
    #
    def git_push (self):
        return run_command (f"git push -u origin {self.branch}")