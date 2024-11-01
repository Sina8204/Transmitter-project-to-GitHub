# import os
# import subprocess

import objects

# def run_command(command):
#     process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     stdout, stderr = process.communicate()
#     if stderr:
#         print(f"Error: {stderr.decode()}")
#     return stdout.decode()

# def main():
#     # تنظیمات کاربر
#     repository_url = input("آدرس ریپازیتوری گیت‌هابت رو وارد کن: ")
#     branch_name = input("نام شاخه مورد نظر رو وارد کن: ")
#     commit_message = input("پیام کامیت رو وارد کن: ")
#     file_path = input("مسیر فایل‌ها رو وارد کن (مثل path/to/your/files): ")

#     # بررسی و سوئیچ کردن به شاخه یا ایجاد شاخه جدید
#     print(f"Checking out branch {branch_name}...")
#     branches = run_command("git branch")
#     if branch_name not in branches:
#         print(f"Branch {branch_name} does not exist. Creating new branch...")
#         run_command(f"git checkout -b {branch_name}")
#     else:
#         result = run_command(f"git checkout {branch_name}")
#         if "Already on" in result:
#             print(f"Already on branch {branch_name}")

#     # تأیید وجود پوشه مقصد
#     if not os.path.exists(branch_name):
#         os.makedirs(branch_name)

#     # انتقال فایل‌ها
#     print(f"Moving files to {branch_name} folder...")
#     if os.path.exists(file_path):
#         if os.name == 'nt':  # ویندوز
#             run_command(f"move {file_path}\\* {branch_name}\\")
#         else:  # مک یا لینوکس
#             run_command(f"mv {file_path}/* {branch_name}/")
#     else:
#         print("Error: مسیر فایل‌ها یافت نشد.")
#         return

#     # مرحله‌بندی تغییرات
#     print("Staging changes...")
#     run_command("git add .")

#     # کامیت تغییرات
#     print("Committing changes...")
#     run_command(f'git commit -m "{commit_message}"')

#     # اضافه کردن remote در صورت نیاز
#     remotes = run_command("git remote -v")
#     if "origin" not in remotes:
#         print("Adding remote origin...")
#         run_command(f"git remote add origin {repository_url}")

#     # کشیدن تغییرات
#     print("Pulling changes from remote...")
#     result = run_command(f"git pull origin {branch_name} --allow-unrelated-histories")
#     if "fatal: refusing to merge unrelated histories" in result:
#         print("Resolving unrelated histories issue...")
#         run_command(f"git pull origin {branch_name} --allow-unrelated-histories")
    
#     # پوش کردن تغییرات
#     print("Pushing changes to remote...")
#     result = run_command(f"git push origin {branch_name}")
#     if "non-fast-forward" in result:
#         print("Handling non-fast-forward issue...")
#         run_command(f"git pull origin {branch_name} --allow-unrelated-histories")
#         run_command("git add .")
#         run_command(f'git commit -m "{commit_message}"')
#         run_command(f"git push origin {branch_name}")

# if __name__ == "__main__":
#     main()

# ob = objects.ready_command ()
# ob.git_init()
# ob.delet_origin()

# def git_push(): 
#     #Branch = str(entry_branch.get())
#     answer = cmd_ob.git_push()
#     if answer.returncode == 0:
#         print("Finished")
#     else:
#         print("we take an error")
#         print (answer.stderr.decode())
#     Termina_textBox.insert(tk.END , str(answer) + '\n')
#     return str(answer)

import tkinter as tk
from tkinter import ttk

def on_select (event) :
    selected = combobox.get()#listbox.get (listbox.curselection())
    print (f"Selected item {selected}")

root = tk.Tk()
root.title()

# listbox = tk.Listbox(root)
# listbox.pack()

# items = ["Item 1" , "Item 2" , "Item 3"]
# for item in items:
#     listbox.insert(tk.END , item)

# listbox.bind("<<ListboxSelect>>" , on_select)

# style = ttk.Style() #map('TCombobox' , selectbackground = [('readonly') , ('SystemWindow')] , selectforeground = [('readonly') , ('SystemWindowText')])
# style.configure ('TCombobox' , selectbackground = 'SystemButtonFace' , selectforeground = 'SystemButtonFace')
# combobox = ttk.Combobox(root , values= ["Item 1" , "Item 2" , "Item 3"] , state='readonly')
# combobox.pack()

# combobox.bind ("<<ComboboxSelected>>" , on_select)

# root.mainloop()

# def x (n):
#     def b ():
#         print ("I am b")
#     def c ():
#         print ('I am c')
    
#     if n == 1 :
#         return b()
#     else :
#         return c()

# q = x(10)

# from datetime import datetime

# print (str(datetime.now()))

s = 'https://github.com/SinaRostami0482/Akhlaghe-Herfe-ei.git'
print (s.split('/'))
d = s.split('/').pop()
d = d.replace('.git', '')
print (d)

# def write_dateTime ():
#     day = str(datetime.now()).split(' ')
#     clock = day[1].split('.')
#     text_date = f"{entry_CommitMessage.get()} ({day[0]}) ({clock[0]})"
#     if entry_CommitMessage.get() != default_entery_commitMessage_text :
#         entry_CommitMessage.delete(0 , tk.END)
#         entry_CommitMessage.insert(0 , text_date)

# def write_repository_name ():
#     rep_name = rep_ob.repName(entry_address.get())
#     if 'https://github.com/' in entry_address.get() or '.git' in entry_address.get():
#         entry_CommitMessage.insert(tk.END , rep_name)

