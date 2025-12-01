from pydantic import BaseModel
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from typing import Optional
import os

# Simple in-memory user store for starter. Replace with DB.
_USERS = {}

SECRET_KEY = os.getenv("FINSTOP_SECRET", "change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[str] = None


class User(BaseModel):
    username: str
    email: Optional[str] = None


def create_user(user: UserCreate) -> bool:
    if user.username in _USERS:
        return False
    hashed = pwd_context.hash(user.password)
    _USERS[user.username] = {"password": hashed, "email": user.email}
    return True


def verify_password(plain, hashed) -> bool:
    return pwd_context.verify(plain, hashed)


def authenticate_user_for_token(username: str, password: str):
    user = _USERS.get(username)
    if not user or not verify_password(password, user["password"]):
        return None
    to_encode = {"sub": username, "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)}
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}


from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    if username not in _USERS:
        raise credentials_exception
    return User(username=username, email=_USERS[username].get("email"))
