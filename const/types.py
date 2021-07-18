from pydantic import constr

from const.user_constants import USERNAME_MAX_LENGTH, PASSWORD_MAX_LENGTH

USERNAME_TYPE = constr(max_length=USERNAME_MAX_LENGTH, to_lower=True)
PASSWORD_TYPE = constr(max_length=PASSWORD_MAX_LENGTH)
