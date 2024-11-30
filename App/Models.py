from sqlalchemy import String
from typing import Optional
import sqlalchemy.orm as so
from .extentions import db
from flask_login import UserMixin
from datetime import datetime,timezone




watchlist = db.Table(
    "Watchlist",
    db.Column("User_ID",db.Integer,db.ForeignKey('Users.id')),
    db.Column("Movie_ID",db.Integer,db.ForeignKey('Movies.index')),
)

class Review(db.Model):
    __tablename__ = "Reviews"
    Review_ID: so.Mapped[int] = so.mapped_column(primary_key=True)
    User_ID = db.Column("User_ID",db.Integer,db.ForeignKey('Users.id'))
    Movie_ID = db.Column("Movie_ID",db.Integer,db.ForeignKey('Movies.index'))
    title:so.Mapped[str] = so.mapped_column(String(150))
    rating: so.Mapped[float] = so.mapped_column(nullable=False)
    review_text:so.Mapped[str] = so.mapped_column(String(250))
    def __repr__(self) -> str:
       return '<Review {} {}>'.format(self.Review_ID,self.review_text)    
   
   
class User(UserMixin,db.Model):
    __tablename__ = "Users"
    id :so.Mapped[int] = so.mapped_column(primary_key=True)
    Username :so.Mapped[str] = so.mapped_column(String(50),nullable=False)
    Email :so.Mapped[str] = so.mapped_column(String(100),nullable=False)
    #Password:so.Mapped[Optional[str]] = so.mapped_column(String(120),nullable=False)
    Password_hash:so.Mapped[Optional[str]] = so.mapped_column(String(120),nullable=False)
    Bio:so.Mapped[Optional[str]]= so.mapped_column(String(250),nullable=True)
    first_name:so.Mapped[Optional[str]]= so.mapped_column(String(150),nullable=True)
    last_name:so.Mapped[Optional[str]]= so.mapped_column(String(150),nullable=True)
    avatar:so.Mapped[Optional[str]] = so.mapped_column(String(120),nullable=True)
    created_at = db.Column(db.DateTime,default=datetime.now(timezone.utc))
    last_seen = db.Column(db.DateTime,default=datetime.now(timezone.utc),onupdate=datetime.now(timezone.utc))
    reviews = db.relationship("Review", backref='author')
    watchlist = db.relationship("Movie",secondary=watchlist, backref='watched_by')
    def __repr__(self) -> str:
       return '<User {}>'.format(self.Username)
   
   
class Movie(db.Model):
    __tablename__ = "Movies"
    index: so.Mapped[int] = so.mapped_column(primary_key=True,nullable=False)
    id: so.Mapped[int] = so.mapped_column(primary_key=True,nullable=False)
    title: so.Mapped[str] = so.mapped_column(String(120),nullable=False)
    vote_average: so.Mapped[float] = so.mapped_column(nullable=True)
    vote_count: so.Mapped[float] = so.mapped_column(nullable=True)
    release_date: so.Mapped[str] = so.mapped_column(String(50),nullable=True)
    overview: so.Mapped[str] = so.mapped_column(nullable=True)
    #popularity: so.Mapped[float] = so.mapped_column(nullable=True)
    tagline: so.Mapped[str] = so.mapped_column(String(120),nullable=True)
    genres: so.Mapped[str] = so.mapped_column(String(120),nullable=True)
    #cast: so.Mapped[str] = so.mapped_column(nullable=True)
    #director: so.Mapped[str] = so.mapped_column(String(120),nullable=True)
    #writers: so.Mapped[str] = so.mapped_column(String(200),nullable=True)
    #producers: so.Mapped[str] = so.mapped_column(String(200),nullable=True)
    poster_path: so.Mapped[str] = so.mapped_column(String(150),nullable=True)
    score: so.Mapped[float] = so.mapped_column(nullable=True)
    reviews = db.relationship("Review", backref='movie')
    def __repr__(self) -> str:
        return '<Movie {} {} {}>'.format(self.id,self.title,self.genres)

    