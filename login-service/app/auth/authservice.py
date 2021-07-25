from sqlalchemy.orm import Session
from db.models import User

class AuthService():

    def login_user(self,db,username:str,password:str):
        user = self.get_user_by_username(db,username)

        if user:
            if user.verify_password(password):
                return user


    def get_user_by_username(self, db:Session, username:str):
        return db.query(User).filter(User.email == username).first()
    
    def get_user_by_id(self, db:Session, id:int):
        return db.query(User).filter(User.id == id).first()

    
