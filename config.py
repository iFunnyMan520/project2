import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MONGODB_DB = os.environ.get('MONGODB_DB')
    MONGODB_HOST = os.environ.get('MONGODB_HOST')
    MONGODB_PORT = int(os.environ.get('MONGODB_PORT'))


config = Config()
