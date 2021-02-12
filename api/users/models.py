import uuid

from werkzeug.security import generate_password_hash, check_password_hash
from api import db


class Avatar(db.EmbeddedDocument):
    """
    TODO create model for avatar
    """


class Followers(db.EmbeddedDocument):
    qty = db.IntField(default=0)
    followers = db.ListField(db.StringField())

    def add_follower(self, _id: str):
        self.followers.append(_id)
        self.qty += 1

    def delete_follower(self, _id: str):
        self.followers.remove(_id)
        self.qty -= 1


class Followed(db.EmbeddedDocument):
    qty = db.IntField(default=0)
    followed = db.ListField(db.StringField())

    def add_followed(self, _id: str):
        self.followed.append(_id)
        self.qty += 1

    def delete_followed(self, _id: str):
        self.followed.remove(_id)
        self.qty -= 1


class Users(db.Document):
    first_name = db.StringField()
    last_name = db.StringField()
    username = db.StringField()
    email = db.StringField(unique=True)
    password = db.StringField()
    auth_token = db.StringField()
    followers = db.EmbeddedDocumentField(Followers)
    followed = db.EmbeddedDocumentField(Followed)

    @staticmethod
    def generate_token():
        return str(uuid.uuid4())

    @classmethod
    def create_user(cls, email: str, password: str):
        """
        Creates a user with a hashing password, auth token and adds its to the
        database
        :param email: sent email that adding to the database
        :param password: sent password that adding to the database
        :return: user model
        """
        hash_pass = generate_password_hash(password)
        token = cls.generate_token()
        user = cls(email=email, password=hash_pass, auth_token=token)
        return user

    def check_pass(self, password):
        """
        Checks if the sent password matches the password in the database
        :param password: sent password
        :return: true if the password matches the password in the database,
        false otherwise
        """
        return check_password_hash(self.password, password)

    def to_json(self):
        return {
            '_id': str(self.pk),
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'email': self.email,
            'followers': self.followers,
            'followed': self.followed
        }
