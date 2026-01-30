from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
from pathlib import Path
from datetime import date, timedelta
from backend.models import TiffinStatus
from backend.schemas import TiffinStatusOut, TiffinStatusUpdate

from backend.database import SessionLocal, engine, Base
from backend.models import User
from backend.schemas import UserCreate, TokenResponse
from backend.auth import (
    hash_password,
    verify_password,
    create_access_token,
    decode_token
)

# =========================
# ENV LOAD (IMPORTANT)
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)

if not os.getenv("SECRET_KEY"):
    raise RuntimeError("SECRET_KEY not set in environment")

# =========================
# DB INIT
# =========================
Base.metadata.create_all(bind=engine)

# =========================
# APP INIT
# =========================
app = FastAPI(
    title="SwaadPe",
    description="Everyday Indian Food - Tiffin-first platform",
    version="1.0.0"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# =========================
# DEPENDENCIES
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    user = db.query(User).filter(User.email == payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

def admin_required(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user
# =========================
# ROUTES
# =========================
@app.get("/")
def root():
    return {"message": "Welcome to SwaadPe – Everyday Indian Food"}


@app.post("/register", status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    admin_email = os.getenv("ADMIN_EMAIL")

    role = "admin" if admin_email and user.email == admin_email else "customer"

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        role=role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "role": role
    }



@app.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Swagger sends "username", we map it to email
    db_user = db.query(User).filter(User.email == form_data.username).first()

    if not db_user or not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        data={"sub": db_user.email, "role": db_user.role}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@app.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role
    }

@app.get("/tiffin/calendar", response_model=list[TiffinStatusOut])
def get_tiffin_calendar(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    today = date.today()
    days = 30  # show next 30 days

    records = (
        db.query(TiffinStatus)
        .filter(TiffinStatus.user_id == current_user.id)
        .all()
    )

    record_map = {r.date: r for r in records}

    calendar = []

    for i in range(days):
        d = today + timedelta(days=i)
        record = record_map.get(d)

        calendar.append({
            "date": d,
            "lunch": record.lunch if record else False,
            "dinner": record.dinner if record else False
        })

    return calendar

@app.post("/admin/tiffin/update")
def update_tiffin_status(
    payload: TiffinStatusUpdate,
    user_id: int,
    current_user: User = Depends(admin_required),
    db: Session = Depends(get_db),
):
    record = (
        db.query(TiffinStatus)
        .filter(
            TiffinStatus.user_id == user_id,
            TiffinStatus.date == payload.date
        )
        .first()
    )

    if not record:
        record = TiffinStatus(
            user_id=user_id,
            date=payload.date,
        )
        db.add(record)

    if payload.lunch is not None:
        record.lunch = payload.lunch
    if payload.dinner is not None:
        record.dinner = payload.dinner

    db.commit()

    return {"message": "Tiffin status updated"}

