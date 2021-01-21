from werkzeug.security import generate_password_hash, check_password_hash
from api import db


class Users(db.Document):
    first_name = db.StringField()
    last_name = db.StringField()
    username = db.StringField()
    email = db.StringField(unique=True)
    password = db.StringField()

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

        :param password:
        :return:
        """
        return check_password_hash(self.password, password)


class Avatar(db.EmbeddedDocument):
    # TODO create model for avatar
    pass


class Followers(db.EmbeddedDocument):
    # TODO create model for followers
    pass


class Followed(db.EmbeddedDocument):
    # TODO create model for followed
    pass
