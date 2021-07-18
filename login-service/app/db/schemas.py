from pydantic import BaseModel

class Role(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True


class User(BaseModel):
    id: int
    email: str
    is_active: bool
    role: Role

    class Config:
        orm_mode = True