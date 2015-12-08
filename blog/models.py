from flask.ext.login import UserMixin
from .database import Base, engine
from sqlalchemy import Column, Integer, String, Text, DateTime
import datetime
    
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    email = Column(String(128), unique=True)
    password = Column(String(128))
    entries = relationship("Entry", backref="author")

class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True)
    title = Column(String(1024))
    content = Column(Text)
    datetime = Column(DateTime, default=datetime.datetime.now)
    author_id = Column(Integer, ForeignKey('users.id'))