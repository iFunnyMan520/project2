from api import db
from datetime import datetime

from api.users.models import Users


class Comments(db.EmbeddedDocument):
    """
    TODO create model for comments
    """


class Picture(db.EmbeddedDocument):
    """
    TODO create model for picture
    """


class Likes(db.EmbeddedDocument):
    """
    TODO create model for likes
    """


class Posts(db.Document):
    title = db.StringField()
    author = db.ReferenceField(Users)
    tags = db.ListField(db.StringField(), default=[])
    only_for_followers = db.BooleanField(default=False)
    created_at = db.DateTimeField(default=datetime.now)

