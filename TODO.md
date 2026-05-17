# Clone Tutorial (Windows)

- [ ] Tutorial: I-clone lang ang repository sa Ibang PC (Windows)

---

## Tutorial: I-clone lang ang Project sa Ibang PC (Windows)

### Layunin
I-clone at i-run ang Tkinter project gamit ang Git para sa repo na ito:
https://github.com/rocky123454321/tkinter_system/tree/main

---

### Prerequisites
1. **Install Python** sa target PC
   - Recommended: **Python 3.10+**
   - https://www.python.org/downloads/
2. **Install Git**
   - https://git-scm.com/download/win

---

## Git Clone Method (Only)

### Step-by-step
1. Magbukas ng **Command Prompt** sa folder kung saan mo gustong ilagay ang project.

2. I-clone ang repo (clone URL papuntang main repo):
   ```bat
   git clone https://github.com/rocky123454321/tkinter_system.git
   cd tkinter_system
   ```

3. (Optional) Tiyakin na naka-main branch:
   ```bat
   git checkout main
   ```

4. Gumawa ng virtual environment:
   ```bat
   python -m venv venv
   ```

5. Activate ang venv:
   ```bat
   venv\Scripts\activate
   ```

6. I-install ang dependencies:
   ```bat
   pip install -r requirements.txt
   ```

7. Run app:
   ```bat
   python main.py
   ```

---

## Quick Troubleshooting

### 1) `python` / `pip` not recognized
- Add Python to PATH during install, then restart Command Prompt.

### 2) `ModuleNotFoundError`
- Siguraduhing activated ang venv bago mag `pip install -r requirements.txt`.

### 3) Image/database loading issues
- Confirm na na-clone ang `assets/` at `database/` folders (kasama dapat ang repo contents).

---

## Checklist bago i-run
- [ ] `main.py` exists
- [ ] `requirements.txt` exists
- [ ] `database/_db.sqlite` exists (sa folder `database/`)
- [ ] `assets/` folder exists

