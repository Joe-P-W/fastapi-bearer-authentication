import jwt
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from passlib.hash import bcrypt
from tortoise.contrib.fastapi import register_tortoise

from authentication import authenticate_user, JWT_SECRET, get_current_user
from models.pydantic import UserPydantic, UserInPydantic
from models.tortoise import User

app = FastAPI()
register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["models.tortoise"]},
    generate_schemas=True,
    add_exception_handlers=True
)


@app.post("/authenticate")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)

    user_object = await UserPydantic.from_tortoise_orm(user)

    raw_token = {"id": user_object.id, "username": user_object.username}

    token = jwt.encode(raw_token, JWT_SECRET)

    return {"access_token": token, "token_type": "bearer"}


@app.post("/users/create", response_model=UserPydantic)
async def create_user(user: UserInPydantic):
    user_object = User(username=user.username, password_hash=bcrypt.hash(user.password_hash))
    await user_object.save()
    return await UserPydantic.from_tortoise_orm(user_object)


@app.get("/users/me")
async def get_user(user: UserPydantic = Depends(get_current_user)):
    return user
