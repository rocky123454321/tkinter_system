# Tutorial: I-transfer / I-clone ang Project sa Ibang PC (Windows)

## Layunin
Makapag-run ang Tkinter Hotel Management System sa ibang computer sa pamamagitan ng:
- **(A) Git Clone** (kung may Git repository)
- **(B) Zip/Folder transfer** (kung walang Git)

---

## Prerequisites (pareho sa A at B)
1. **Install Python** sa target PC
   - Recommended: **Python 3.10+**
   - https://www.python.org/downloads/
2. **Install Git** (only kung gagamit ng A)
   - https://git-scm.com/download/win

---

## A) Git Clone Method
> Gamitin ito kung ang project ay nasa Git repository (GitHub/GitLab/etc.).

### Step-by-step
1. Magbukas ng **Command Prompt** sa folder kung saan mo gustong ilagay ang project.
2. I-clone ang repo:
   ```bat
   git clone <YOUR_REPO_URL>
   cd <YOUR_REPO_FOLDER_NAME>
   ```
3. Gumawa ng virtual environment:
   ```bat
   python -m venv venv
   ```
4. Activate ang venv:
   ```bat
   venv\Scripts\activate
   ```
5. I-install ang dependencies:
   ```bat
   pip install -r requirements.txt
   ```
6. Run app:
   ```bat
   python main.py
   ```

---

## B) Zip / Folder Transfer (No Git)
> Ito ang pinakasimpleng paraan kung gusto mong i-transfer via USB/Drive o file sharing.

### Step-by-step
1. **I-compress** ang buong project folder (dapat kasama ang lahat ng folder/files sa project).
   - Kasama dapat:
     - `main.py`
     - `controllers/`
     - `views/`
     - `models/`
     - `database/`  *(critical: may `_db.sqlite`)*
     - `utils/`
     - `assets/`  *(critical: may images)*
     - `requirements.txt`
2. Copy/transfer ang zip sa ibang PC.
3. Extract ang zip sa desired folder.
4. Gumawa ng virtual environment:
   ```bat
   python -m venv venv
   ```
5. Activate ang venv:
   ```bat
   venv\Scripts\activate
   ```
6. Install requirements:
   ```bat
   pip install -r requirements.txt
   ```
7. Run app:
   ```bat
   python main.py
   ```

---

## Common Problems & Fixes

### 1) Missing images (assets)
**Symptoms:** may errors sa loading images, blank UI.
- Fix: tiyaking na-transfer ang buong `assets/` folder.

### 2) Database errors / walang data
**Symptoms:** di gumagana login/admin seeds, tables missing.
- Fix: tiyaking na-transfer ang buong `database/` folder (may `_db.sqlite`).

### 3) Dependency errors
**Symptoms:** ImportError / ModuleNotFoundError.
- Fix: siguraduhing naka-activate ang venv bago mag `pip install -r requirements.txt`.

---

## Quick Checklist bago i-run
- [ ] `main.py` exists
- [ ] `requirements.txt` exists
- [ ] `database/_db.sqlite` exists (sa folder `database/`)
- [ ] `assets/` folder exists

---

## File Summary ng kailangan i-transfer
Pinakamabilis tandaan:
**`main.py` + `controllers/` + `views/` + `models/` + `utils/` + `database/` + `assets/` + `requirements.txt`**

