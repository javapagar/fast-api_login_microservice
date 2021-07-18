from typing import List, Optional

from pydantic import BaseModel


# class RoleBase(BaseModel):
#     title: str

# class RoleCreate(RoleBase):
#     pass


# class Role(RoleBase):
#     id: int
#     users: List[User] = []

#     class Config:
#         orm_mode = True


class UserBase(BaseModel):
    email: str


# class UserCreate(UserBase):
#     password: str


class User(UserBase):
    id: int
    is_active: bool
    # rol_id: int

    class Config:
        orm_mode = True