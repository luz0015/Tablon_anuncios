import os

class Config:
    SECRET_KEY = '123456789'
   
    SQLALCHEMY_DATABASE_URI = 'sqlite:///bd_anuncios.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
