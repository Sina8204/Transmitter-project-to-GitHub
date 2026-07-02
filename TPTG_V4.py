import tkinter as tk
from tkinter.ttk import Combobox
from datetime import datetime
import tkinter as tk
from tkinter import ttk , filedialog , messagebox
import os , subprocess
import os
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
import threading
import queue
import time
import re

default_entery_adress_text = "Enter your Repository adress"
default_entery_branch_text = "Enter your branch name"
default_entery_commitMessage_text = "Enter your commit"
can_write_in_commitEntry = False

class ready_command():
    def __init__(self):
        self.branch = ''
        self.size_project = 0
        self.unit = "Mb"
        self.paw = 1
        self.working_dir = os.getcwd()  # مسیر کاری پیش‌فرض
        self.ssl_was_disabled = False  # برای پیگیری وضعیت SSL

    def _disable_ssl(self):
        """غیرفعال کردن اعتبارسنجی SSL"""
        try:
            # بررسی وضعیت فعلی SSL
            result = subprocess.run(
                "git config --global http.sslVerify", 
                shell=True, 
                capture_output=True, 
                text=True
            )
            
            # اگر SSL فعال بود، آن را غیرفعال کن
            if result.stdout.strip().lower() != 'false':
                subprocess.run(
                    "git config --global http.sslVerify false", 
                    shell=True, 
                    check=True
                )
                self.ssl_was_disabled = True
                print("🔓 SSL verification temporarily disabled")
                return True
            else:
                self.ssl_was_disabled = False
                return True
        except Exception as e:
            print(f"⚠️ Error disabling SSL: {e}")
            return False

    def _enable_ssl(self):
        """فعال کردن مجدد اعتبارسنجی SSL"""
        try:
            if self.ssl_was_disabled:
                subprocess.run(
                    "git config --global http.sslVerify true", 
                    shell=True, 
                    check=True
                )
                self.ssl_was_disabled = False
                print("🔒 SSL verification re-enabled")
                return True
            return True
        except Exception as e:
            print(f"⚠️ Error enabling SSL: {e}")
            return False

    def _check_ssl_status(self):
        """بررسی وضعیت فعلی SSL"""
        try:
            result = subprocess.run(
                "git config --global http.sslVerify", 
                shell=True, 
                capture_output=True, 
                text=True
            )
            return result.stdout.strip()
        except:
            return None

    def run_command(self, command, cwd=None, manage_ssl=False):
        """
        اجرای دستور در دایرکتوری مشخص شده با مدیریت SSL
        
        Args:
            command: دستوری که باید اجرا شود
            cwd: مسیر دایرکتوری اجرا (اختیاری)
            manage_ssl: آیا نیاز به مدیریت SSL دارد؟ (پیش‌فرض: False)
        """
        # اگر نیاز به مدیریت SSL باشد
        if manage_ssl:
            # غیرفعال کردن SSL
            if not self._disable_ssl():
                messagebox.showwarning(title="Failed to disable SSL" , message="⚠️ Failed to disable SSL, continuing anyway...")
                print("⚠️ Failed to disable SSL, continuing anyway...")
        
        try:
            # اجرای دستور اصلی
            process = subprocess.Popen(
                command, 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                cwd=cwd or self.working_dir
            )
            stdout, stderr = process.communicate()
            
            if stderr:
                print(f">>>  {stderr.decode()}")
            
            result = [stdout.decode(), process]
            
            # فعال کردن مجدد SSL (فقط در صورت نیاز)
            if manage_ssl:
                self._enable_ssl()
            
            return result
            
        except Exception as e:
            # در صورت خطا، مطمئن شویم SSL دوباره فعال شود
            if manage_ssl:
                self._enable_ssl()
            raise e

    def check_connection(self):
        """بررسی اتصال به مخزن از راه دور - نیاز به SSL دارد"""
        try:
            # این دستور با مخزن راه دور ارتباط برقرار می‌کند
            result = self.run_command(f"git ls-remote origin {self.branch}", manage_ssl=True)
            if result[1].returncode == 0:
                return [True, "Connection successful ✅", result[0]]
            else:
                return [False, "Connection failed ❌", result[0]]
        except Exception as e:
            return [False, f"Error: {str(e)}", ""]

    def set_working_directory(self, path):
        """تنظیم مسیر کاری برای اجرای دستورات"""
        if os.path.exists(path):
            self.working_dir = path
            return True
        return False

    def git_init(self):
        """ایجاد مخزن محلی - نیازی به SSL ندارد"""
        return self.run_command("git init", manage_ssl=False)[0]

    def delet_origin(self):
        """حذف remote محلی - نیازی به SSL ندارد"""
        return self.run_command("git remote remove origin", manage_ssl=False)[0]

    def add_origin(self, gitHub_address: str):
        """
        تنظیم آدرس مخزن راه دور - نیاز به SSL دارد
        (برای اطمینان از اتصال صحیح)
        """
        self.gitHub_address = gitHub_address
        return self.run_command(f"git remote add origin {self.gitHub_address}", manage_ssl=True)[0]

    def git_pull(self, branch: str = "master"):
        """
        دریافت تغییرات از مخزن راه دور - نیاز به SSL دارد
        """
        self.branch = branch
        return self.run_command(f"git pull origin {self.branch} --allow-unrelated-histories", manage_ssl=True)[0]

    def creat_LocalBranch(self):
        """ایجاد برنچ محلی - نیازی به SSL ندارد"""
        return self.run_command(f'git checkout -b {self.branch}', manage_ssl=False)[0]

    def git_add(self):
        """افزودن فایل‌ها به stage محلی - نیازی به SSL ندارد"""
        return self.run_command("git add .", manage_ssl=False)[0]

    def git_commit(self, message: str):
        """ثبت تغییرات محلی - نیازی به SSL ندارد"""
        self.message = message
        return self.run_command(f'git commit -m "{self.message}"', manage_ssl=False)[0]

    def git_push(self):
        """
        ارسال تغییرات به مخزن راه دور - نیاز به SSL دارد
        """
        return self.run_command(f"git push -u origin {self.branch}", manage_ssl=True)

    def delete_git(self):
        """حذف مخزن محلی - نیازی به SSL ندارد"""
        # برای ویندوز
        if os.name == 'nt':  # ویندوز
            return self.run_command("Remove-Item -Recurse -Force .git", manage_ssl=False)
        else:  # لینوکس/مک
            return self.run_command("rm -rf .git", manage_ssl=False)

    def project_size(self, start_path=None, unit="Mb"):
        """محاسبه سایز پروژه - نیازی به SSL ندارد"""
        if start_path is None:
            start_path = self.working_dir

        self.unit = unit
        match self.unit:
            case "Kb":
                self.paw = 1
            case "Mb":
                self.paw = 2
            case "Gb":
                self.paw = 3
            case _:
                self.paw, self.unit = 0, 'Byte'
        
        # محاسبه سایز (بدون نیاز به SSL)
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(start_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if os.path.exists(fp):
                    total_size += os.path.getsize(fp)
        
        size_in_unit = total_size / (1024 ** self.paw)
        return size_in_unit

    def run_safe_command(self, command, cwd=None, needs_ssl=False):
        """
        اجرای یک دستور با مدیریت خودکار SSL
        
        Args:
            command: دستوری که باید اجرا شود
            cwd: مسیر دایرکتوری اجرا (اختیاری)
            needs_ssl: آیا دستور به SSL نیاز دارد؟ (پیش‌فرض: False)
        """
        return self.run_command(command, cwd=cwd, manage_ssl=needs_ssl)

class terminal:
    def __init__(self , root):
        self.root = root

        self.termina_frame = tk.Frame(self.root)
        self.termina_frame.pack(fill='both' , expand=True)

        self.Termina_textBox = tk.Text(self.termina_frame, width=70 , height=20)
        self.Termina_textBox.pack(fill='both' , expand=True)
        #self.Termina_textBox.grid(row=11, column=0, padx=5 , pady=5, sticky='w')  # ✅ sticky='w'

class tools:
    def __init__(self, root , TextInput : terminal):
        self.root = root

        self.terminal = TextInput.Termina_textBox
        self.cmd = ready_command()

        # ===== موارد جدید اضافه شده =====
        # برای مدیریت threadها
        self.push_thread = None
        self.stop_push = False
        self.progress_queue = queue.Queue()
        
        # متغیر برای پیگیری وضعیت
        self.is_pushing = False
        # ===== پایان موارد جدید =====

        self.tools_frame = tk.Frame(self.root, width=10, height=50)
        self.tools_frame.grid(row=0, column=0, sticky='nsew')  # ✅ اضافه کردن sticky
        
        # ✅ تنظیم وزن ستون‌ها
        self.tools_frame.columnconfigure(0, weight=0)  # ستون اول کشیده شود
        self.tools_frame.columnconfigure(1, weight=1)  # ستون دوم فقط به اندازه خودش باشد
        #self.tools_frame.columnconfigure(2, weight=0)  # ستون دوم فقط به اندازه خودش باشد

        # Entry ها در ستون 0
        self.entry_path = tk.Entry(self.tools_frame)
        self.entry_path.grid(row=0, column=0, padx=5, pady=5, sticky='ew')  # ✅ sticky='ew'

        self.button_select_path = tk.Button(self.tools_frame , text="Select path" , command=self.select_path)
        self.button_select_path.grid(row=0, column=1 , padx=5, pady=5, sticky='ew')  # ✅ sticky='ew'

        self.entry_address = tk.Entry(self.tools_frame, width=50)
        self.entry_address.insert(0, default_entery_adress_text)
        self.entry_address.bind('<FocusIn>', self.entry_events('adress'))
        self.entry_address.bind('<FocusOut>', self.entry_events('adress_out'))
        self.entry_address.grid(row=1, column=0, padx=5, pady=5, sticky='ew')  # ✅ sticky='ew'

        self.entry_branch = tk.Entry(self.tools_frame, width=50)
        self.entry_branch.insert(0, default_entery_branch_text)
        self.entry_branch.bind('<FocusIn>', self.entry_events('branch'))
        self.entry_branch.bind('<FocusOut>', self.entry_events('branch_out'))
        self.entry_branch.grid(row=2, column=0, padx=5, pady=5, sticky='ew')

        self.entry_CommitMessage = tk.Entry(self.tools_frame, width=50)
        self.entry_CommitMessage.insert(0, default_entery_commitMessage_text)
        self.entry_CommitMessage.bind('<FocusIn>', self.entry_events('commit'))
        self.entry_CommitMessage.bind('<FocusOut>', self.entry_events('commit_out'))
        self.entry_CommitMessage.grid(row=3, column=0, padx=5, sticky='ew')

        # Combobox در ستون 1 (کنار entry_CommitMessage)
        self.combobox_commitTools = ttk.Combobox(self.tools_frame, 
                                                values=["Repository name", "Branch name", "Calender", "Time"],
                                                state='readonly', 
                                                width=22)
        self.combobox_commitTools.set("Select an item to write it")
        self.combobox_commitTools.bind("<<ComboboxSelected>>", self.on_combobox_select)
        self.combobox_commitTools.grid(row=3, column=1, pady=5, padx=5, sticky='e')  # ✅ sticky='e' برای چسبیدن به راست

        # دکمه در ستون 0، ردیف 3 با sticky='w' برای چسبیدن به چپ
        self.button_GitInit = tk.Button(self.tools_frame, text=" git init ", command = self.git_init)
        self.button_GitInit.grid(row=4, column=0, padx=5 , pady=5, sticky='ew')  # ✅ sticky='w'

        self.button_projectSize = tk.Button (self.tools_frame, text=" Project size" , command=self.project_size)#, command= project_size)
        self.button_projectSize.grid(row=4, column=1, padx=5 , pady=5, sticky='ew')  # ✅ sticky='w'

        self.combobox_unit = ttk.Combobox (self.tools_frame , values= ["Kb" , "Mb" , "Gb" , "Byte"] , state='readonly' , width= 5)
        self.combobox_unit.grid(row=4, column=2, padx=5 , pady=5, sticky='ew')  # ✅ sticky='w'
        self.combobox_unit.set ("Mb")

        self.button_CheckConection = tk.Button(self.tools_frame, text="Check conection" , command=self.check_conection)
        self.button_CheckConection.grid(row=5, column=1, padx=5 , pady=5, sticky='ew')  # ✅ sticky='w'

        self.button_DeletOrigin = tk.Button (self.tools_frame, text="Delete origin", command=self.delet_origin)
        self.button_DeletOrigin.grid(row=5, column=0, padx=5 , pady=5, sticky='ew')  # ✅ sticky='w'

        self.button_AddOrigin = tk.Button (self.tools_frame, text="Add origin", command=self.add_origin)
        self.button_AddOrigin.grid(row=6, column=0, padx=5 , pady=5, sticky='ew')  # ✅ sticky='w'

        self.button_GitPull = tk.Button (self.tools_frame, text="git pull", command=self.git_pull)
        self.button_GitPull.grid(row=7, column=0, padx=5 , pady=5, sticky='ew')  # ✅ sticky='w'

        self.button_GitAdd = tk.Button (self.tools_frame, text="git add", command=self.git_add)
        self.button_GitAdd.grid(row=8, column=0, padx=5 , pady=5, sticky='ew')  # ✅ sticky='w'

        self.button_GitCommit = tk.Button (self.tools_frame, text="git commit", command=self.git_commit)
        self.button_GitCommit.grid(row=9, column=0, padx=5 , pady=5, sticky='ew')  # ✅ sticky='w'

        self.button_GitPush = tk.Button (self.tools_frame, text=" git push", command=self.start_push)
        self.button_GitPush.grid(row=10, column=0, padx=5 , pady=5, sticky='ew')  # ✅ sticky='w'

        # ===== موارد جدید اضافه شده =====
        # Progress Bar برای نمایش پیشرفت push
        self.progress_frame = tk.Frame(self.tools_frame)
        self.progress_frame.grid(row=11, column=0, columnspan=3, padx=5, pady=5, sticky='ew')

        self.progress_label = tk.Label(self.progress_frame, text="Ready")
        self.progress_label.pack(side=tk.LEFT, padx=5)

        self.progress_bar = ttk.Progressbar(self.progress_frame, length=300, mode='determinate')
        self.progress_bar.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.progress_percent = tk.Label(self.progress_frame, text="0%")
        self.progress_percent.pack(side=tk.RIGHT, padx=5)

        # دکمه توقف
        self.stop_button = tk.Button(self.progress_frame, text="⏹ Stop", command=self.stop_push_operation,
                                    state=tk.DISABLED, bg='#ff4444', fg='white')
        self.stop_button.pack(side=tk.RIGHT, padx=5)
        # ===== پایان موارد جدید =====

        # ===== مورد جدید اضافه شده =====
        # شروع پردازش queue
        self.root.after(100, self.process_queue)
        # ===== پایان مورد جدید =====

    def select_path(self):
        """باز کردن دیالوگ انتخاب مسیر و به‌روزرسانی متغیر global"""
        global selected_path
        path = filedialog.askdirectory(title="Select project directory")
        if path:
            selected_path = path
            self.entry_path.delete(0 , tk.END)
            self.entry_path.insert(tk.END , path)
            # به‌روزرسانی مسیر در شیء cmd_ob
            self.cmd.set_working_directory(path)
            self.terminal.insert(tk.END, f"Working directory changed to: {path}\n")
    
    def check_conection(self):
        try:
            if self.cmd.check_connection()[0]:
                messagebox.showinfo(title='Good status' , message='Conection is ok')
            else :
                messagebox.showwarning(title='Field at conection' , message='Conection is not ok')
        except Exception as e:
            messagebox.showerror(title='Field at conection' , message=f'Error : \n\t{e}')
            print(f"Error : \n\t{e}")

    def git_init(self):
        try:
            answer = self.cmd.git_init()
            self.terminal.insert(tk.END, str(answer) + '\n')
            return str(answer)
        except Exception as e:
            messagebox.showerror(title="Field at run command 'git init'" , message=f'Error : \n\t{e}')
    
    def delet_origin(self):
        try:
            answer = self.cmd.delet_origin()
            self.terminal.insert(tk.END, str(answer) + '\n')
            return str(answer)
        except Exception as e:
            messagebox.showerror(title="Field at run command 'delet origin'" , message=f'Error : \n\t{e}')


    def add_origin(self):
        try:
            address = str(self.entry_address.get())
            answer = self.cmd.add_origin(address)
            self.terminal.insert(tk.END, str(answer) + '\n')
            return str(answer)
        except Exception as e:
            messagebox.showerror(title="Field at run command 'add origin'" , message=f'Error : \n\t{e}')


    def git_pull(self):
        try:
            Branch = str(self.entry_branch.get())
            answer = self.cmd.git_pull(Branch)
            self.terminal.insert(tk.END, str(answer) + '\n')
            answer = self.cmd.creat_LocalBranch()
            return str(answer)
        except Exception as e:
            messagebox.showerror(title="Field at run command 'git pull'" , message=f'Error : \n\t{e}')


    def git_add(self):
        try:
            answer = self.cmd.git_add()
            self.terminal.insert(tk.END, str(answer) + '\n')
            return str(answer)
        except Exception as e:
            messagebox.showerror(title="Field at run command 'git add'" , message=f'Error : \n\t{e}')


    def git_commit(self):
        try:
            Message = str(self.entry_CommitMessage.get())
            answer = self.cmd.git_commit(Message)
            self.terminal.insert(tk.END, str(answer) + '\n')
            return str(answer)
        except Exception as e:
            messagebox.showerror(title="Field at run command 'git commit'" , message=f'Error : \n\t{e}')
    
    def start_push(self):
        """شروع عملیات push در یک thread جداگانه"""
        if self.is_pushing:
            messagebox.showwarning("Warning", "Push operation is already in progress!")
            return
        
        try:
            # غیرفعال کردن دکمه‌ها در حین عملیات
            self.set_buttons_state(tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.is_pushing = True
            
            # ریست progress bar
            self.progress_bar['value'] = 0
            self.progress_percent.config(text="0%")
            self.progress_label.config(text="Starting push...")
            
            # ایجاد و شروع thread
            self.push_thread = threading.Thread(target=self._push_worker, daemon=True)
            self.push_thread.start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start push: {str(e)}")
            self.reset_push_state()
    # ===== پایان متد start_push =====

    # ===== متد جدید _push_worker =====
    def _push_worker(self):
        """کارگر thread برای اجرای push و نمایش پیشرفت"""
        try:
            # اجرای دستور push با خروجی real-time
            process = subprocess.Popen(
                f"git push -u origin {self.cmd.branch}",
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=self.cmd.working_dir,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # خواندن خروجی به صورت خط به خط
            total_files = self._count_files_to_push()
            pushed_files = 0
            progress = 0
            
            while True:
                if self.stop_push:
                    process.terminate()
                    self.progress_queue.put(('status', 'stopped'))
                    break
                
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                    
                if output:
                    self.progress_queue.put(('output', output))
                    
                    # تشخیص پیشرفت از خروجی git
                    if 'writing' in output.lower() or 'compressing' in output.lower() or 'delta' in output.lower():
                        pushed_files += 1
                        if total_files > 0:
                            progress = min(100, int((pushed_files / total_files) * 100))
                        else:
                            progress = min(100, progress + 5)  # افزایش تدریجی
                            
                        self.progress_queue.put(('progress', progress))
                        self.progress_queue.put(('status', f"Pushing... {pushed_files} files"))
            
            # بررسی نتیجه
            return_code = process.poll()
            if return_code == 0:
                self.progress_queue.put(('complete', True))
            else:
                error = process.stderr.read()
                self.progress_queue.put(('complete', False))
                self.progress_queue.put(('error', error))
                
        except Exception as e:
            self.progress_queue.put(('error', str(e)))
            self.progress_queue.put(('complete', False))
    # ===== پایان متد _push_worker =====

    # ===== متد جدید process_queue =====
    def process_queue(self):
        """پردازش queue و به‌روزرسانی UI"""
        try:
            while not self.progress_queue.empty():
                item = self.progress_queue.get_nowait()
                msg_type = item[0]
                data = item[1]
                
                if msg_type == 'progress':
                    self.progress_bar['value'] = data
                    self.progress_percent.config(text=f"{data}%")
                elif msg_type == 'status':
                    self.progress_label.config(text=data)
                elif msg_type == 'output':
                    self.terminal.insert(tk.END, data)
                    self.terminal.see(tk.END)
                elif msg_type == 'error':
                    self.terminal.insert(tk.END, f"Error: {data}\n")
                    self.terminal.see(tk.END)
                elif msg_type == 'complete':
                    if data:
                        self.on_push_complete(True)
                    else:
                        self.on_push_complete(False)
                elif msg_type == 'stopped':
                    self.on_push_stopped()
                    
        except Exception as e:
            print(f"Queue processing error: {e}")
            
        finally:
            # اگر push کامل نشده، دوباره صدا بزن
            if self.is_pushing:
                self.root.after(100, self.process_queue)
    # ===== پایان متد process_queue =====

    # ===== متد جدید on_push_complete =====
    def on_push_complete(self, success):
        """وقتی عملیات push کامل شد"""
        if success:
            self.progress_label.config(text="✅ Push completed!")
            self.terminal.insert(tk.END, f'\n\n✅ Push to "{self.cmd.branch}" branch operation was successful :)\n')
            
            # حذف پوشه .git
            try:
                self.cmd.delete_git()
                self.terminal.insert(tk.END, "✅ Git folder deleted successfully\n")
            except Exception as e:
                self.terminal.insert(tk.END, f"⚠️ Could not delete .git folder: {e}\n")
        else:
            self.progress_label.config(text="❌ Push failed!")
            
        self.reset_push_state()
    # ===== پایان متد on_push_complete =====
    # ===== متد جدید on_push_stopped =====
    def on_push_stopped(self):
        """وقتی عملیات push متوقف شد"""
        self.progress_label.config(text="⏹ Push stopped by user")
        self.terminal.insert(tk.END, "\n⚠️ Push operation was stopped by user\n")
        self.reset_push_state()
    # ===== پایان متد on_push_stopped =====

    # ===== متد جدید stop_push_operation =====
    def stop_push_operation(self):
        """توقف عملیات push"""
        if self.is_pushing:
            self.stop_push = True
            self.progress_label.config(text="Stopping...")
            self.stop_button.config(state=tk.DISABLED)
    # ===== پایان متد stop_push_operation =====

    # ===== متد جدید reset_push_state =====
    def reset_push_state(self):
        """بازنشانی وضعیت push"""
        self.is_pushing = False
        self.stop_push = False
        self.push_thread = None
        self.set_buttons_state(tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        
        # اگر progress کامل نشده، تنظیم مجدد
        if self.progress_bar['value'] < 100:
            self.progress_bar['value'] = 0
            self.progress_percent.config(text="0%")
            self.progress_label.config(text="Ready")
    # ===== پایان متد reset_push_state =====

    # ===== متد جدید set_buttons_state =====
    def set_buttons_state(self, state):
        """فعال/غیرفعال کردن دکمه‌ها"""
        buttons = [
            self.button_GitInit, self.button_projectSize, self.button_CheckConection,
            self.button_DeletOrigin, self.button_AddOrigin, self.button_GitPull,
            self.button_GitAdd, self.button_GitCommit, self.button_GitPush
        ]
        for btn in buttons:
            btn.config(state=state)
    # ===== پایان متد set_buttons_state =====
    def project_size(self):
        try:
            self.terminal.insert(tk.END, self.cmd.project_size(unit=self.combobox_unit.get()) + '\n')
        except Exception as e:
            messagebox.showerror(title="Field at get project size" , message=f'Error : \n\t{e}')
    
    def entry_events (self , entry_name):
        # For better management of these functions , I placed them inside a function 
        # so that I can hide them in VS cod when I don't need them.
        def on_entryAdress_click (event): #when clicked on address entry , its text will be delete
            if self.entry_address.get() == default_entery_adress_text :
                self.entry_address.delete(0 , tk.END)
                self.entry_address.config(fg = 'black')
        #
        def on_entryBranch_click (event): #when clicked on entry Branch entry , its text will be delete
            if self.entry_branch.get() == default_entery_branch_text :
                self.entry_branch.delete(0 , tk.END)
                self.entry_branch.config(fg = 'black')
        #
        def on_entryCommitMessage_click (event): #when clicked on Commit messege entry , its text will be delete
            if self.entry_CommitMessage.get() == default_entery_commitMessage_text :
                self.entry_CommitMessage.delete(0 , tk.END)
                self.entry_CommitMessage.config(fg = 'black')
            global can_write_in_commitEntry
            can_write_in_commitEntry = True
        #
        # Focus out function :
        # These functions check the entry text boxes. if they contain any value , they do nothing ,
        # but if they are empty , they write the initial text in gray color inside them. 
        def on_focus_out_adress(event):
            if self.entry_address.get() == '':
                self.entry_address.insert(0 , default_entery_adress_text)
                self.entry_address.config(fg = 'grey')
        #
        def on_focus_out_branch(event):
            if self.entry_branch.get() == '':
                self.entry_branch.insert(0 , default_entery_branch_text)
                self.entry_branch.config(fg = 'grey')
        #
        def on_focus_out_commit(event):
            if self.entry_CommitMessage.get() == '':
                self.entry_CommitMessage.insert(0 , default_entery_commitMessage_text)
                self.entry_CommitMessage.config(fg = 'grey')
        #
        match entry_name :
            #if click in entry box to writing , entry box will be empty
            case 'adress' : return on_entryAdress_click
            case 'branch' : return on_entryBranch_click
            case 'commit' : return on_entryCommitMessage_click
            #if entry box be empty , these cases will write the gray texts
            case 'adress_out' : return on_focus_out_adress
            case 'branch_out' : return on_focus_out_branch
            case 'commit_out' : return on_focus_out_commit
    def repName (self , rep_link : str):
        rep_link = rep_link.split('/')
        rep_name = rep_link.pop()
        rep_name = rep_name.replace('.git', '')
        return rep_name
    
    def on_combobox_select (self , event):
        selected = self.combobox_commitTools.get()
        DateTime = str(datetime.now()).split(' ')
        calender = DateTime[0]
        clock = DateTime[1]
        rep_name = self.repName(self.entry_address.get()) if 'https://github.com/' in self.entry_address.get() or '.git' in self.entry_address.get() else ''
        # if 'https://github.com/' in self.entry_address.get() or '.git' in self.entry_address.get():
        #     rep_name = self.repName(self.entry_address.get())
        # else : pass
        if self.entry_CommitMessage.get() != default_entery_commitMessage_text or can_write_in_commitEntry:
            match selected:
                
                case "Repository name" : 
                    if self.entry_CommitMessage.get() == default_entery_commitMessage_text and can_write_in_commitEntry:
                        self.entry_CommitMessage.delete(0 , tk.END)
                        self.entry_CommitMessage.config(fg = 'black')
                    self.entry_CommitMessage.insert(tk.END , f'{rep_name} ')
                case "Branch name" :
                    if self.entry_CommitMessage.get() == default_entery_commitMessage_text and can_write_in_commitEntry:
                        self.entry_CommitMessage.delete(0 , tk.END)
                        self.entry_CommitMessage.config(fg = 'black')
                    self.entry_CommitMessage.insert(tk.END , f'{self.entry_branch.get()} ')
                case "Calender" :
                    if self.entry_CommitMessage.get() == default_entery_commitMessage_text and can_write_in_commitEntry:
                        self.entry_CommitMessage.delete(0 , tk.END)
                        self.entry_CommitMessage.config(fg = 'black')
                    self.entry_CommitMessage.insert(tk.END , f'{calender} ')
                case "Time" :
                    if self.entry_CommitMessage.get() == default_entery_commitMessage_text and can_write_in_commitEntry:
                        self.entry_CommitMessage.delete(0 , tk.END)
                        self.entry_CommitMessage.config(fg = 'black')
                    self.entry_CommitMessage.insert(tk.END , f'{clock} ')


class GitHubTransmitter(tk.Tk):
    def __init__(self, screenName = None, baseName = None, className = "Tk", useTk = True, sync = False, use = None):
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.title("Transmitter to GitHub")
        self.set_window_size(width_ratio=0.385, height_ratio=0.8)

        self.main_pw = tk.PanedWindow(self , orient=tk.VERTICAL)
        self.main_pw.pack(fill=tk.BOTH , expand=1)
        self.pw_top_horizontala = tk.PanedWindow(self.main_pw , orient=tk.VERTICAL, bd=1 , relief="solid")
        self.pw_down_horizontala = tk.PanedWindow(self.main_pw , orient=tk.VERTICAL, bd=1 , relief="solid")
        self.main_pw.add(self.pw_top_horizontala , height = 450)
        self.main_pw.add(self.pw_down_horizontala)

        self.frame_tools = tk.Frame(self.pw_top_horizontala)
        self.frame_terminal = tk.Frame(self.pw_down_horizontala)

        self.pw_top_horizontala.add(self.frame_tools)
        self.pw_down_horizontala.add(self.frame_terminal)

        self.terminal_panel = terminal(self.frame_terminal)
        self.tools_panel = tools(root = self.frame_tools , TextInput = self.terminal_panel)
    
    def set_window_size(self , width_ratio, height_ratio): # this take our monitor siza and make a window with our monitor details 
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        window_width = int(screen_width * width_ratio)
        window_height = int(screen_height * height_ratio)

        self.geometry(f"{window_width}x{window_height}")

app = GitHubTransmitter()
app.mainloop()
