# SwaadPe 🍽️

**SwaadPe** is a **tiffin-first food platform** focused on delivering **everyday Indian meals**.  
It is designed to start with **tiffin services** and scale later into **restaurant / cloud kitchen** operations.

Built with **FastAPI**, secure authentication, and a scalable backend architecture.

---

## ✨ Features

- Customer & Admin authentication (JWT based)
- Secure Register / Login
- Protected APIs
- User profile (`/me`)
- Tiffin-service–ready backend (Lunch / Dinner)
- Subscription-ready architecture (weekly / monthly)
- Loyalty system foundation (Swaad Coins – upcoming)
- Mobile & desktop friendly (UI planned)

---

## 🧱 Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: SQLite (local) / PostgreSQL (production)
- **ORM**: SQLAlchemy
- **Auth**: JWT (OAuth2 compatible)
- **UI**: Tailwind CSS (planned)
- **Version Control**: GitHub

---

## 📁 Project Structure
```bash
swaadpe/
│
├── backend/
│ ├── main.py
│ ├── auth.py
│ ├── database.py
│ ├── models.py
│ ├── schemas.py
│ └── init.py
│
├── .env # REQUIRED (not committed)
├── requirements.txt
├── README.md
└── venv/
```
---

## 🚀 Run SwaadPe Locally (Step-by-Step)

Follow **all steps in order** to run the project locally.

---

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/<your-username>/swaadpe.git
cd swaadpe
```
---

### 2️⃣ Create & Activate Virtual Environment
#### Windows
```bash

python -m venv venv
venv\Scripts\activate
```
#### macOS / Linux
```bash

python3 -m venv venv
source venv/bin/activate
```
---

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Create .env File (MANDATORY)

Create a file named .env in the project root:
```bash
swaadpe/.env
```


✅ .env content (copy–paste exactly)
```bash
# =========================
# SECURITY
# =========================
SECRET_KEY=<YOUR SECRET KEY>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_HOURS=24

# =========================
# DATABASE
# =========================
DATABASE_URL=<YOUR DATABASE URL>

# =========================
# DATABASE
# =========================
ADMIN_EMAIL=<ADMIN_EMAIL>
# =========================
# APP CONFIG
# =========================
APP_NAME=SwaadPe
ENV=development

```
⚠️ Important rules:
- ❌ Do NOT add quotes
- ❌ Do NOT add spaces around =
- ❌ Do NOT commit .env to GitHub

.env is already included in .gitignore.

### 5️⃣ Start the Server

Make sure you are in the project root (swaadpe/), then run:
```bash
uvicorn backend.main:app --reload
```
You should see:
Application startup complete.

### 6️⃣ Open the App

- API Root → http://127.0.0.1:8000
- Swagger Docs → http://127.0.0.1:8000/docs