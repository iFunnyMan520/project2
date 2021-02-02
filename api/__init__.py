from flask import Flask
from flasgger import Swagger
from flask_mongoengine import MongoEngine

from config import config

app = Flask(__name__)
client = app.test_client()
swagger = Swagger(app)
app.config.from_object(config)
db = MongoEngine(app)


from api.posts import routes as posts_routes
from api.users import routes as users_routes
