# 🎮 GAME_PROJECT

Project game berbasis **Python** yang dibangun secara modular dan dapat dibuild menjadi file **.exe** menggunakan **PyInstaller**.
dan Kelompok kami berisi dari:

- Ulil Amry AQ
- Artia Jofi Fiorenthia
- Putri Tandi Langi Paonganan

---

---

## 🚀 Setup Project

### 1️⃣ Clone Repository

```bash
git clone https://github.com/USERNAME/GAME_PROJECT.git
cd GAME_PROJECT
```

### 2️⃣ Buat & Aktifkan Virtual Environment

```bash
python -m venv venv
```

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

Pastikan muncul `(venv)` di terminal.

---

### 3️⃣ Install Dependency

```bash
pip install -r requirements.txt
```

---

## ▶️ Menjalankan Game

```bash
python main.py
```

---

## 🛠️ Build menjadi EXE

Project ini menggunakan **PyInstaller**.

```bash
pyinstaller main.spec
```

Hasil build akan muncul di folder:

```bash
dist/main.exe
```

---
