from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from blog import app

"""engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])"""
engine = create_engine("postgresql://ubuntu:thinkful@localhost:5432/blogful")

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime

from .database import Base, engine
from sqlalchemy import ForeignKey

    
Base.metadata.create_all(engine)