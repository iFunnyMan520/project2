import os


class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'very_secret_key')
    MONGODB_DB = os.getenv('DB_NAME', 'mydb')
    MONGODB_HOST = os.getenv('DB_HOST', 'localhost')
    MONGODB_PORT = os.getenv('DB_PORT', 27017)


config = Config()
