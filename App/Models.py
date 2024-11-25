from sqlalchemy import String
from typing import Optional
import sqlalchemy.orm as so
from .extentions import db



class User(db.Model):
    __tablename__ = "Users"
    User_ID :so.Mapped[int] = so.mapped_column(primary_key=True)
    Username :so.Mapped[str] = so.mapped_column(String(50))
    Password:so.Mapped[Optional[str]] = so.mapped_column(String(120),)
    Password_hash:so.Mapped[Optional[str]] = so.mapped_column(String(120))
    Bio:so.Mapped[Optional[str]]= so.mapped_column(String(250))
    avatar:so.Mapped[Optional[str]] = so.mapped_column(String(120))
    
    def __repr__(self) -> str:
       return '<User {}>'.format(self.Username)