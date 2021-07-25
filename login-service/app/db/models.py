from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from passlib.context import CryptContext
from datetime import datetime

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role_id = Column(Integer, ForeignKey("roles.id"))
    
    role = relationship("Role")

    pwd_context =CryptContext(schemes = ['bcrypt'], deprecated = 'auto')


    def __init__(self,**kwargs):
        super(User, self).__init__(**kwargs)
        self.hashed_password = self.get_password_hash(self.hashed_password)

    def verify_password(self,password):
        return self.pwd_context.verify(password, self.hashed_password)
    
    def get_password_hash(self,password):
        return self.pwd_context.hash(password)

    def get_payload(self):
        return { 'sub':str(self.id),
                'email':self.email,
                'is_active':self.is_active,
                'role':self.role.title}

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)
