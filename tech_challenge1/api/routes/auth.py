from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
from tech_challenge1.db.database import SessionLocal
from tech_challenge1.models.user import User as DBUser
from tech_challenge1.core.security import create_access_token, get_password_hash, verify_password

auth_router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class UserRegister(BaseModel):
    username: str
    password: str


@auth_router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    user_exists = db.query(DBUser).filter(DBUser.username == user.username).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="Usuário já existe")

    db_user = DBUser(username=user.username, hashed_password=get_password_hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"msg": f"Usuário '{user.username}' criado com sucesso"}


@auth_router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(DBUser).filter(DBUser.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")

    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
