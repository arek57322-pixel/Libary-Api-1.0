from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import models
from app.schemas import UserRegister, UserLogin, Token
from app.auth import hash_password, verify_password, create_access_token


router = APIRouter(prefix="/auth", tags=["Auth"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register(data: UserRegister, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == data.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = models.User(
        email=data.email,
        password_hash=hash_password(data.password),
        role="client"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"id": new_user.id, "email": new_user.email, "role": new_user.role}


@router.post("/login", response_model=Token)
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id), "role": user.role})
    return {"access_token": token, "token_type": "bearer"}
