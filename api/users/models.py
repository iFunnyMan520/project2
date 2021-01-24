from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from api import db


class Avatar(db.EmbeddedDocument):
    # TODO create model for avatar
    pass


class Followers(db.EmbeddedDocument):
    qty = db.IntField(default=0)
    followers = db.ListField(db.ObjectIdField(), default=[])

    def add_follower(self, id: ObjectId):
        self.followers.append(id)
        self.qty += 1

    def delete_follower(self, id: ObjectId):
        self.followers.remove(id)
        self.qty -= 1


class Followed(db.EmbeddedDocument):
    qty = db.IntField(default=0)
    followed = db.ListField(db.ObjectIdField(), default=[])

    def add_followed(self, id: ObjectId):
        self.followed.append(id)
        self.qty += 1

    def delete_followed(self, id: ObjectId):
        self.followed.remove(id)
        self.qty -= 1


class Users(db.Document):
    first_name = db.StringField()
    last_name = db.StringField()
    username = db.StringField()
    email = db.StringField(unique=True)
    password = db.StringField()
    followers = db.EmbeddedDocumentField(Followers)
    followed = db.EmbeddedDocumentField(Followed)

    @classmethod
    def create_user(cls, email: str, password: str):
        """
        Creates a user with a hashing password and adds its to the database
        :param email: sent email that adding to the database
        :param password: sent password that adding to the database
        :return: user model
        """
        hash_pass = generate_password_hash(password)
        user = cls(email=email, password=hash_pass)
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
            'username': '@' + self.username,
            'email': self.email,
            'followers': self.followers,
            'followed': self.followed
        }
