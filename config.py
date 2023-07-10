import os


class AppConfig:
    DEBUG = os.getenv('DEBUG')
    PORT = os.getenv('PORT')
    SECRET_KEY = os.getenv('SECRET_KEY')
    HOST = os.getenv('HOST')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
