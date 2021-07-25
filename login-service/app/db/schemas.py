from pydantic import BaseModel
from typing import Optional

class Role(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True



    class Config:
        orm_mode = True

class User(BaseModel):
    id: int
    email: str
    is_active: bool
    role: Role

    class Config:
        orm_mode = True

class LoginUser(BaseModel):
    email: str
    password: str

# class User(BaseModel):
#     username: str
#     email: Optional[str] = None
#     full_name: Optional[str] = None
#     disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str