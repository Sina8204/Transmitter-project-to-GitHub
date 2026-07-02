# 🌐 Languages  
[English](#-english-version) | [فارسی](#نسخه-فارسی)

## 🇬🇧 English Version

# GitHub Transmitter  
A desktop application built with **Python** and **Tkinter** that provides a graphical interface for performing Git operations such as initializing repositories, adding remotes, pulling, committing, pushing, and checking connections — all without needing to use the terminal.

This tool is designed for developers who want a simple, visual way to interact with Git, especially in environments where SSL verification issues may occur. The application automatically manages SSL states when required.

---

## 🚀 Features

- **Graphical Git Controller**  
  Perform essential Git commands through buttons instead of CLI.

- **Automatic SSL Handling**  
  The app temporarily disables SSL verification when needed and restores it afterward.

- **Repository Tools**  
  - `git init`  
  - `git add`  
  - `git commit`  
  - `git pull`  
  - `git push`  
  - Add / Remove origin  
  - Create local branches  
  - Check remote connection

- **Commit Message Generator**  
  Insert repository name, branch name, date, or time into commit messages using a dropdown.

- **Project Size Calculator**  
  Calculate project size in KB, MB, GB, or Bytes.

- **Built‑in Terminal Panel**  
  Shows command outputs in real time.

- **Resizable UI with PanedWindow Layout**

---

## 🧩 Technologies Used

- **Python 3.x**
- **Tkinter**
- **Git CLI**
- **Subprocess**
- **OS module**

---

## 📷 Screenshots  
*(Add your screenshots here)*

---

## 📦 Installation

```bash
git clone <your-repository>
cd <project-folder>
python main.py
```

---

## 🛠 Usage

1. Select your project directory.  
2. Enter repository URL and branch name.  
3. Use the buttons to perform Git operations.  
4. View logs in the terminal panel.  
5. Use the commit message tools to generate structured commit messages.

---

## 🔐 SSL Management

The application includes functions such as:

> "🔓 SSL verification temporarily disabled"  
> "🔒 SSL verification re-enabled"

These ensure Git commands work even when SSL issues occur.

---

## 📁 Project Structure

```
GitHubTransmitter/
│── main.py
│── README.md
│── /assets (optional)
```

---

## 📜 License  
You may use or modify this project freely.

---

---

## 🇮🇷 نسخه فارسی

# GitHub Transmitter  
یک برنامه دسکتاپ ساخته‌شده با **Python** و **Tkinter** که امکان انجام عملیات Git را از طریق رابط گرافیکی فراهم می‌کند.  
این ابزار برای توسعه‌دهندگانی طراحی شده که می‌خواهند بدون استفاده از ترمینال، مخزن‌های Git را مدیریت کنند — مخصوصاً در شرایطی که مشکلات SSL رخ می‌دهد.

برنامه به‌صورت خودکار SSL را هنگام نیاز غیرفعال و پس از پایان عملیات دوباره فعال می‌کند.

---

## 🚀 قابلیت‌ها

- **کنترل کامل Git از طریق رابط گرافیکی**
- **مدیریت خودکار SSL**
- **ابزارهای مخزن**
  - ایجاد مخزن (`git init`)
  - افزودن فایل‌ها (`git add`)
  - کامیت کردن (`git commit`)
  - پول گرفتن (`git pull`)
  - پوش کردن (`git push`)
  - افزودن / حذف origin
  - ساخت برنچ محلی
  - بررسی اتصال به مخزن راه دور

- **ساخت پیام کامیت هوشمند**
  - نام مخزن  
  - نام برنچ  
  - تاریخ  
  - زمان  

- **محاسبه سایز پروژه**
- **ترمینال داخلی برای نمایش خروجی‌ها**
- **رابط کاربری قابل تغییر اندازه**

---

## 🧩 تکنولوژی‌های استفاده‌شده

- Python  
- Tkinter  
- Git CLI  
- Subprocess  
- OS module  

---

## 📦 نصب

```bash
git clone <آدرس مخزن>
cd <پوشه پروژه>
python main.py
```

---

## 🛠 نحوه استفاده

1. مسیر پروژه را انتخاب کنید.  
2. آدرس مخزن و نام برنچ را وارد کنید.  
3. عملیات Git را با دکمه‌ها انجام دهید.  
4. خروجی‌ها را در پنل ترمینال مشاهده کنید.  
5. پیام کامیت را با ابزارهای کمکی بسازید.

---

## 🔐 مدیریت SSL

بخشی از متن کد:

> "🔓 SSL verification temporarily disabled"  
> "🔒 SSL verification re-enabled"

این پیام‌ها نشان می‌دهند که برنامه SSL را هنگام نیاز مدیریت می‌کند.

---

## 📁 ساختار پروژه

```
GitHubTransmitter/
│── main.py
│── README.md
│── /assets (اختیاری)
```

---

## 📜 لایسنس  
استفاده و تغییر این پروژه آزاد است.

---
