import pytest
from flask import Flask
from werkzeug.security import generate_password_hash

from api import app
from api.users.models import Users


@pytest.fixture(scope='module')
def server_app() -> Flask:
    print('\nServer started')
    return app


@pytest.fixture(scope='session', autouse=True)
def create_base():
    Users.drop_collection()
    hash_pass = generate_password_hash('1234')
    Users(email='test_email1@mail.com', password=hash_pass).save()
    Users(email='test_email2@mail.com', password=hash_pass).save()
    Users(email='test_email3@mail.com', password=hash_pass).save()
    Users(email='test_email4@mail.com', password=hash_pass).save()
    Users(email='test_email5@mail.com', password=hash_pass).save()


@pytest.fixture(scope='session', autouse=True)
def me() -> Users:
    user: Users = Users.create_user(email='me_email@gmail.com',
                                    password=generate_password_hash('qwerty'))

    return user


@pytest.fixture(scope='session', autouse=True)
def simple_user_1() -> str:
    user: Users = Users(email='simple_email1@gmail.com',
                        password=generate_password_hash('qwerty')).save()

    return str(user.pk)


@pytest.fixture(scope='session', autouse=True)
def simple_user_2() -> str:
    user: Users = Users(email='simple_email2@gmail.com',
                        password=generate_password_hash('qwerty')).save()

    return str(user.pk)
