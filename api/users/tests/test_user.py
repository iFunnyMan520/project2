import pytest
from bson import ObjectId

from api.users.models import Users
from flask import Flask

from api.users.tests.rest_client import UserClient

email = 'test_email@gmail.com'
password = 'test_password'
first_name = 'test_first_name'
username = 'test_username'
last_name = 'test_last_name'
user_id = ObjectId(b'test_user_id')
test_token = 'test_token'


@pytest.fixture(scope='module')
def user(server_app: Flask):
    return UserClient(server_app)


@pytest.fixture
def my_token(me) -> str:
    return me.auth_token


@pytest.fixture
def my_id(me) -> str:
    return str(me.pk)


@pytest.fixture
def first_id(simple_user_1):
    return simple_user_1


@pytest.fixture
def second_id(simple_user_2):
    return simple_user_2


def test_get_users(user: UserClient):
    response = user.get_users()

    users = Users.objects()
    users_array = []

    for user in users:
        users_array.append(user.to_json())

    assert response.status_code == 200
    assert {'users': users_array} == response.get_json()
    assert len(response.get_json()['users']) == 8


def test_sign_up(user: UserClient):
    response = user.invalid_data_sign_up(email, password)

    data = response.get_json()

    assert response.status_code == 400
    assert data['email'] == ['Missing data for required field.']
    assert data['emails'] == ['Unknown field.']
    assert data['password'] == ['Missing data for required field.']
    assert data['passwords'] == ['Unknown field.']

    response = user.sign_up('email', password)

    data = response.get_json()

    assert data['email'] == ['Not a valid email address.']

    response = user.sign_up(email, password)

    global token
    token = response.get_json()['token']

    response = user.sign_up(email, password)

    assert response.status_code == 401
    assert response.get_json()['message'] == 'User already exists'


def test_me(user: UserClient):

    user_check = Users.objects(email=email).first()

    response = user.me(token)

    assert response.status_code == 200
    assert response.get_json() == user_check.to_json()

    response = user.me(test_token)

    assert response.status_code == 404
    assert response.get_json()['message'] == 'User could not be found'

    response = user.change_my_data(test_token, username, first_name, last_name)

    assert response.status_code == 404
    assert response.get_json()['message'] == 'User could not be found'

    response = user.change_my_data(token, username, first_name, last_name)

    user_check = Users.objects(email=email).first()

    assert response.status_code == 200
    assert response.get_json() == user_check.to_json()

    response = user.change_my_data(token, username, first_name, last_name)

    assert response.status_code == 200
    assert response.get_json() == user_check.to_json()


def test_delete_me(user: UserClient):
    response = user.delete_me(test_token)

    assert response.get_json()['message'] == 'User could not be found'
    assert response.status_code == 404

    response = user.delete_me(token)

    user_check = Users.objects(email=email).first()

    assert response.get_json()['message'] == 'User has been deleted'
    assert user_check is None


def test_login(user: UserClient):
    response = user.invalid_data_login('test_email1', '1234')

    err_messages = response.get_json()

    assert response.status_code == 400
    assert err_messages['email'] == ['Missing data for required field.']
    assert err_messages['password'] == ['Missing data for required field.']

    assert err_messages['emails'] == ['Unknown field.']
    assert err_messages['passwords'] == ['Unknown field.']

    response = user.login('test_email1@mail.com', '12345')

    assert response.status_code == 404
    assert response.get_json()['message'] == 'Wrong email or password'

    response = user.login('test_email11@mail.com', '1234')

    assert response.status_code == 404
    assert response.get_json()['message'] == 'Wrong email or password'

    response = user.login('test_email1@mail.com', '1234')

    global auth_token

    auth_token = response.get_json()['token']

    assert response.status_code == 200
    assert auth_token is not None

    response = user.login('test_email1@mail.com', '1234')

    assert response.get_json()['message'] == 'User is already logged in'


def test_logout(user: UserClient):
    response = user.logout(test_token)

    assert response.status_code == 401
    assert response.get_json()['message'] == 'User is not logged in'

    response = user.logout(auth_token)

    assert response.status_code == 200
    assert response.get_json()['message'] == 'You are logged out now'


def test_follow_views(user: UserClient, my_id):
    response = user.followers(my_id)

    assert response.get_json() is None


def test_my_followed(user: UserClient, my_id, my_token, first_id, second_id):
    response = user.subscribe(my_token, first_id)

    assert response.status_code == 200
    assert response.get_json()['message'] == 'You have subscribed now'

    response = user.subscribe(my_token, second_id)

    assert response.status_code == 200
    assert response.get_json()['message'] == 'You have subscribed now'

    response = user.followed(my_id)

    assert response.status_code == 200
    assert len(response.get_json()) == 2

    response = user.subscribe(my_token, second_id)

    assert response.status_code == 200
    assert response.get_json()['message'] == 'You have already subscribed'

    response = user.followers(second_id)

    assert response.status_code == 200
    assert len(response.get_json()) == 1

    response = user.unsubscribe(my_token, second_id)

    assert response.status_code == 200
    assert response.get_json()['message'] == 'You have unsubscribed now'

    response = user.followed(my_id)

    assert response.status_code == 200
    assert len(response.get_json()) == 1

    response = user.followers(second_id)

    assert response.status_code == 200
    assert response.get_json() is None
