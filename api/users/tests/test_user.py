from bson import ObjectId

from api import client
from api.users.models import Users

email = 'test_email'
password = 'test_password'
first_name = 'test_first_name'
username = 'test_username'
last_name = 'test_last_name'
user_id = ObjectId(b'test_user_id')
test_token = 'test_token'


def test_get_users():
    response = client.get('/api/v1.0/users/')

    users = Users.objects()
    users_array = []

    if not users:
        assert response.status_code == 404
        assert response.data == b'Users cannot be found'
        return

    for user in users:
        users_array.append(user.to_json())

    assert response.status_code == 200
    assert {'users': users_array} == response.get_json()


def test_me():
    response = client.post('/api/v1.0/users/signUp', json={
        'emails': email,
        'password': password
    })

    assert response.status_code == 400
    assert response.data == b'Invalid data'

    response = client.post('/api/v1.0/users/signUp', json={
        'email': email,
        'passwords': password
    })

    assert response.status_code == 400
    assert response.data == b'Invalid data'

    response = client.post('/api/v1.0/users/signUp', json={
        'email': email,
        'password': password
    })

    token = response.get_json()['token']

    response = client.post('/api/v1.0/users/signUp', json={
        'email': email,
        'password': password
    })

    assert response.status_code == 401
    assert response.data == b'User already exists'

    user_check = Users.objects(email=email).first()

    response = client.get('/api/v1.0/users/me', json={
        'token': token
    })

    assert response.status_code == 200
    assert response.get_json() == user_check.to_json()

    response = client.get('/api/v1.0/users/me', json={
        'token': test_token
    })

    assert response.status_code == 404
    assert response.data == b'User could not be found'

    response = client.put('/api/v1.0/users/me', json={
        'token': test_token,
        'username': username,
        'first_name': first_name,
        'last_name': last_name
    })

    assert response.status_code == 404
    assert response.data == b'User could not be found'

    response = client.put('/api/v1.0/users/me', json={
        'token': token,
        'username': username,
        'first_name': first_name,
        'last_name': last_name
    })

    user_check = Users.objects(email=email).first()

    assert response.status_code == 200
    assert response.get_json() == user_check.to_json()

    response = client.delete('/api/v1.0/users/me', json={
        'token': test_token
    })

    assert response.data == b'User could not be found'
    assert response.status_code == 404

    response = client.delete('/api/v1.0/users/me', json={
        'token': token
    })

    user_check = Users.objects(email=email).first()

    assert response.data == b'User has been deleted'
    assert user_check is None
