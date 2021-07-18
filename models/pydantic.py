from pydantic import BaseModel, constr
from tortoise.contrib.pydantic import pydantic_model_creator

from const.user_constants import PASSWORD_MAX_LENGTH, USERNAME_MAX_LENGTH
from models.tortoise import User


UserAPI = pydantic_model_creator(User, name="User")


class CreateUserReturn(BaseModel):
    saved: bool
    username: constr(max_length=USERNAME_MAX_LENGTH)


class CreateUser(BaseModel):
    username: constr(max_length=USERNAME_MAX_LENGTH)
    password: constr(max_length=PASSWORD_MAX_LENGTH)


class GetUserReturn(BaseModel):
    username: constr(max_length=USERNAME_MAX_LENGTH)
