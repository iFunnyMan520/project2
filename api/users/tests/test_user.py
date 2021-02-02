from bson import ObjectId

from api import client
from api.users.models import Users

email = 'test_email'
password = 'test_password'
first_name = 'test_first_name'
username = 'test_username'
last_name = 'test_last_name'
user_id = ObjectId(b'test_user_id')


def test_get_users():
    response = client.get('/api/v1.0/users/')

    users = Users.objects()
    users_array = []
    for user in users:
        users_array.append(user.to_json())

    assert response.status_code == 200
    assert {'users': users_array} == response.get_json()


def test_add_user():
    response = client.post('/api/v1.0/users/', json={
        'emails': email,
        'password': password
    })

    assert response.status_code == 400
    assert response.data == b'Invalid data'

    response = client.post('/api/v1.0/users/', json={
        'email': email,
        'password': password
    })

    assert response.status_code == 201
    assert response.data == b'User has been created'

    response = client.post('/api/v1.0/users/', json={
        'email': email,
        'password': password
    })

    assert response.status_code == 401
    assert response.data == b'User already exists'


def test_get_user_by_id():
    user = Users.objects(email=email).first()

    _id = str(user.pk)
    response = client.get(f'/api/v1.0/users/id={_id}')

    assert response.status_code == 200
    assert response.get_json() == user.to_json()

    response = client.get(f'/api/v1.0/users/id={user_id}')

    assert response.status_code == 404
    assert response.data == b'User could not be found'


def test_add_new_data():
    user = Users.objects(email=email).first()

    _id = str(user.pk)
    response = client.put(f'/api/v1.0/users/id={_id}', json={
        'first_name': first_name,
        'username': username,
        'last_name': last_name
    })

    user = Users.objects(email=email).first()

    assert response.status_code == 200
    assert response.get_json() == user.to_json()

    response = client.put(f'/api/v1.0/users/id={user_id}', json={
        'first_name': first_name,
        'username': username,
        'last_name': last_name
    })

    assert response.data == b'User could not be found'
    assert response.status_code == 404

    response = client.put(f'/api/v1.0/users/id={_id}', json={
        'first_names': first_name,
        'username': username,
        'last_name': last_name
    })

    assert response.data == b'Invalid data'
    assert response.status_code == 400


def test_delete_user():
    user = Users.objects(email=email).first()

    _id = str(user.pk)

    response = client.delete(f'/api/v1.0/users/id={_id}')

    assert response.data == b'User has been deleted'
    assert response.status_code == 200

    response = client.delete(f'/api/v1.0/users/id={user_id}')

    assert response.data == b'User could not be found'
    assert response.status_code == 404

    user = Users.objects(email=email).first()

    assert user is None
