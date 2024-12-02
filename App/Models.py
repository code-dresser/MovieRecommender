from sqlalchemy import String
from typing import Optional
import sqlalchemy.orm as so
from .extentions import db
from flask_login import UserMixin
from datetime import datetime,timezone
from hashlib import md5



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
    Password:so.Mapped[Optional[str]] = so.mapped_column(String(120),nullable=False)
    Password_hash:so.Mapped[Optional[str]] = so.mapped_column(String(120),nullable=False)
    Bio:so.Mapped[Optional[str]]= so.mapped_column(String(250),nullable=True)
    first_name:so.Mapped[Optional[str]]= so.mapped_column(String(150),nullable=True,default="Mystery")
    last_name:so.Mapped[Optional[str]]= so.mapped_column(String(150),nullable=True,default="Person")
    created_at:so.Mapped[datetime] = db.Column(db.DateTime,default=datetime.now(timezone.utc))
    last_seen:so.Mapped[datetime] = db.Column(db.DateTime,default=datetime.now(timezone.utc))
    reviews = db.relationship("Review", backref='author')
    watchlist = db.relationship("Movie",secondary=watchlist, backref='watched_by')
    
    
    def __repr__(self) -> str:
       return '<User {}>'.format(self.Username)
   
    def watchlist_query(self):
        subquery = db.session.query(watchlist.c.Movie_ID).filter(watchlist.c.User_ID == self.id)
        return db.session.query(Movie).filter(Movie.index.in_(subquery))
   
    def avatar(self, size):
        digest = md5(self.Email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
    
    def since_date(self):
        return self.created_at.strftime(r'%Y-%m-%d')
    
    def last_seen_at(self):
        return self.last_seen.strftime(r'%Y-%m-%d %X')
   
class Movie(db.Model):
    __tablename__ = "Movies"
    index: so.Mapped[int] = so.mapped_column(primary_key=True,nullable=False)
    id: so.Mapped[int] = so.mapped_column(primary_key=True,nullable=False)
    title: so.Mapped[str] = so.mapped_column(String(120),nullable=False)
    vote_average: so.Mapped[float] = so.mapped_column(nullable=True)
    vote_count: so.Mapped[float] = so.mapped_column(nullable=True)
    release_date: so.Mapped[str] = so.mapped_column(String(50),nullable=True)
    overview: so.Mapped[str] = so.mapped_column(nullable=True)
    tagline: so.Mapped[str] = so.mapped_column(String(120),nullable=True)
    genres: so.Mapped[str] = so.mapped_column(String(120),nullable=True)
    poster_path: so.Mapped[str] = so.mapped_column(String(150),nullable=True)
    score: so.Mapped[float] = so.mapped_column(nullable=True)
    reviews = db.relationship("Review", backref='movie')
    def __repr__(self) -> str:
        return '<Movie {} {} {}>'.format(self.id,self.title,self.genres)

    