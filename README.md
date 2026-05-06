# TKINTER SYSTEM

## Para sa mga Teammates 👋
Bago kayo magsimula, basahin muna ito para ma-setup ang project sa inyong computer.

---

## Folder Structure
- 📁 views/ - Dito lalagay ang lahat ng Tkinter UI screens/pages
- 📁 controllers/ - Dito lalagay ang logic/functions ng system
- 📁 models/ - Dito lalagay ang lahat ng database queries
- 📁 database/ - Dito lalagay ang database connection setup
- 📁 assets/images/ - Dito lalagay ang lahat ng images at icons

---

## Setup Guide

### Step 1 - I-clone ang repo
    git clone https://github.com/rocky123454321/tkinter_system
    cd tkinter_system

### Step 2 - Gumawa ng venv
    python -m venv venv

### Step 3 - I-activate ang venv
    venv\Scripts\activate

### Step 4 - I-install ang libraries
    pip install -r requirements.txt

### Step 5 - Gumawa ng .env file
Gumawa ng .env file sa root folder at ilagay ang:

    DB_HOST=localhost
    DB_USER=root
    DB_PASSWORD=yourpassword
    DB_NAME=tkinter_system

### Step 6 - I-run ang system
    python main.py

---

## Reminders ⚠️
- Huwag i-push ang .env file sa GitHub
- I-activate lagi ang venv bago mag-code
- Gumawa ng sariling branch bago mag-code
- Mag-pull muna bago mag-push
