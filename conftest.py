import pytest
from flask import Flask
from werkzeug.security import generate_password_hash

from api import app
from api.users.models import Users
from api.posts.models import Posts
from api.users.utils import subscribe


@pytest.fixture(scope='module')
def server_app() -> Flask:
    print('\nThe server is running')
    return app


@pytest.fixture(scope='session', autouse=True)
def create_base():
    Users.drop_collection()
    Posts.drop_collection()
    hash_pass = generate_password_hash('1234')
    user1 = Users(email='test_email1@mail.com', password=hash_pass).save()
    user2 = Users(email='test_email2@mail.com', password=hash_pass).save()
    user3 = Users(email='test_email3@mail.com', password=hash_pass).save()
    user4 = Users(email='test_email4@mail.com', password=hash_pass).save()
    user5 = Users(email='test_email5@mail.com', password=hash_pass).save()
    Posts(title='post1', author=user1).save()
    Posts(title='post2', author=user1).save()
    Posts(title='post3', author=user3).save()
    Posts(title='post4', author=user5).save()


@pytest.fixture(scope='session', autouse=True)
def simple_user_1() -> 'Users':
    user: Users = Users(email='simple_email1@gmail.com',
                        password=generate_password_hash('qwerty')).save()
    Posts(title='post_user_1', author=user).save()
    Posts(title='post_user_2', author=user).save()

    return user


@pytest.fixture(scope='session', autouse=True)
def simple_user_2() -> 'Users':
    user: Users = Users(email='simple_email2@gmail.com',
                        password=generate_password_hash('qwerty')).save()

    return user


@pytest.fixture(scope='session', autouse=True)
def me(simple_user_1) -> Users:
    user: Users = Users.create_user(email='me_email@gmail.com',
                                    password=generate_password_hash('qwerty'))

    me_user = subscribe(user, simple_user_1)

    return me_user
