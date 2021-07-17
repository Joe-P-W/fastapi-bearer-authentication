import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from models.pydantic import UserPydantic
from models.tortoise import User

JWT_SECRET = "secret"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="authenticate")


async def authenticate_user(username: str, password: str):
    user = await User.get(username=username)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    if not user.verify_password(password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user_object = await User.get(id=payload.get("id"))
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    return await UserPydantic.from_tortoise_orm(user_object)
