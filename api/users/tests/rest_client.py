from flask import Flask, Response
from flask.testing import FlaskClient


class UserClient:

    def __init__(self, app: Flask):
        self.client: FlaskClient = app.test_client()
        self.key: str = '4da5933b-120a-4108-8670-faa83ca6a43a'

    def get_users(self, token: str) -> Response:
        return self.client.get('/api/v1.0/users/', headers={
            'token': token, 'secret_key': self.key
        })

    def invalid_data_sign_up(self, emails: str, passwords: str) -> Response:
        return self.client.post('/api/v1.0/users/signUp', json={
            'emails': emails,
            'passwords': passwords
        }, headers={'secret_key': self.key})

    def sign_up(self, email: str, password: str) -> Response:
        return self.client.post('/api/v1.0/users/signUp', json={
            'email': email,
            'password': password
        }, headers={'secret_key': self.key})

    def invalid_data_login(self, emails: str, passwords: str) -> Response:
        return self.client.post('/api/v1.0/users/logIn', json={
            'emails': emails,
            'passwords': passwords
        }, headers={'secret_key': self.key})

    def login(self, email: str, password: str) -> Response:
        return self.client.post('/api/v1.0/users/logIn', json={
            'email': email,
            'password': password
        }, headers={'secret_key': self.key})

    def me(self, token) -> Response:
        return self.client.get('/api/v1.0/users/me', headers={
            'token': token, 'secret_key': self.key
        })

    def change_my_data(self,
                       token: str,
                       username: str,
                       first_name: str,
                       last_name: str) -> Response:
        return self.client.put('/api/v1.0/users/me', json={
            'username': username,
            'first_name': first_name,
            'last_name': last_name
        }, headers={'token': token, 'secret_key': self.key})

    def delete_me(self, token: str) -> Response:
        return self.client.delete('/api/v1.0/users/me', headers={
            'token': token, 'secret_key': self.key
        })

    def logout(self, token: str) -> Response:
        return self.client.post('/api/v1.0/users/me/logOut', headers={
            'token': token, 'secret_key': self.key
        })

    def followers(self, my_id: str, token: str) -> Response:
        return self.client.get(f'/api/v1.0/users/id={my_id}/followers',
                               headers={
                                   'token': token,
                                   'secret_key': self.key
                               }
                               )

    def followed(self, my_id: str, token: str) -> Response:
        return self.client.get(f'/api/v1.0/users/id={my_id}/followed',
                               headers={
                                   'token': token,
                                   'secret_key': self.key
                               }
                               )

    def subscribe(self, token: str, _id: str) -> Response:
        return self.client.post('/api/v1.0/users/me/follow', json={
            '_id': _id
        }, headers={'token': token, 'secret_key': self.key})

    def unsubscribe(self, token: str, _id: str) -> Response:
        return self.client.delete('/api/v1.0/users/me/follow', json={
            '_id': _id
        }, headers={'token': token, 'secret_key': self.key})






