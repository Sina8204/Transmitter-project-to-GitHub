import tkinter as tk
from objects import ready_command as rc
import subprocess

pos_x = 10
pos_y = 100
distance = 35

cmd_ob = rc()

def git_init():
    answer = cmd_ob.git_init()
    Termina_textBox.insert(tk.END , str(answer) + '\n')
    return str(answer)

def delet_origin():
    answer = cmd_ob.delet_origin()
    Termina_textBox.insert(tk.END , str(answer) + '\n')
    return str(answer)

def add_origin ():
    address = str(entry_address.get())
    answer = cmd_ob.add_origin(address) #
    Termina_textBox.insert(tk.END , str(answer) + '\n')
    return str(answer)

def git_pull ():
    Branch = str(entry_branch.get())
    answer = cmd_ob.git_pull(Branch) #Branch is master at default
    Termina_textBox.insert(tk.END , str(answer) + '\n')
    answer = cmd_ob.creat_LocalBranch()
    return str(answer)

def git_add():
    answer = cmd_ob.git_add()
    Termina_textBox.insert(tk.END , str(answer) + '\n')
    return str(answer)

def git_commit():
    Message = str (entry_CommitMessage.get())
    answer = cmd_ob.git_commit(Message) # 
    Termina_textBox.insert(tk.END , str(answer) + '\n')
    return str(answer)

def git_push(): 
    #Branch = str(entry_branch.get())
    answer = cmd_ob.git_push()
    if answer[1].returncode == 0:
        print("Push operation was successful :)")
        Termina_textBox.insert(tk.END , str(answer[1]) + f'\n\nPush to "{cmd_ob.branch}" branch operation was successful :)\n')
    else:
        print("we take an error")
        print (answer[0])
        Termina_textBox.insert(tk.END , str(answer[1]) + '\n')
    return str(answer)


def set_window_size(root, width_ratio, height_ratio): # this take our monitor siza and make a window with our monitor details 
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    window_width = int(screen_width * width_ratio)
    window_height = int(screen_height * height_ratio)

    root.geometry(f"{window_width}x{window_height}")

root = tk.Tk()
root.title("Transmitter to GitHub")

set_window_size(root, width_ratio=0.385, height_ratio=0.8)

entry_address = tk.Entry (root, width=50) #text box to enter files adress
entry_address.place (x = pos_x , y = pos_y - 90)

entry_branch = tk.Entry (root, width=50) #text box to enter files adress
entry_branch.place (x = pos_x , y = pos_y - 60)

entry_CommitMessage = tk.Entry (root, width=50) #text box to enter files adress
entry_CommitMessage.place (x = pos_x , y = pos_y - 30)

button_GitInit = tk.Button (root, text=" git init          ", command=git_init)
button_GitInit.place (x = pos_x , y = pos_y)

button_DeletOrigin = tk.Button (root, text="Delete origin", command=delet_origin)
button_DeletOrigin.place (x = pos_x , y = pos_y + distance)

button_AddOrigin = tk.Button (root, text="Add origin    ", command=add_origin)
button_AddOrigin.place (x = pos_x , y = pos_y + (distance * 2))

button_GitPull = tk.Button (root, text="git pull          ", command=git_pull)
button_GitPull.place (x = pos_x , y = pos_y + (distance * 3))

button_GitAdd = tk.Button (root, text="git add          ", command=git_add)
button_GitAdd.place (x = pos_x , y = pos_y + (distance * 4))

button_GitCommit = tk.Button (root, text=" git commit  ", command=git_commit)
button_GitCommit.place (x = pos_x , y = pos_y + (distance * 5))

button_GitPush = tk.Button (root, text=" git push       ", command=git_push)
button_GitPush.place (x = pos_x , y = pos_y + (distance * 6))

Termina_textBox = tk.Text(root, width=70 , height=20)
Termina_textBox.place (x = pos_x , y = pos_y + (distance * 7))





root.mainloop()