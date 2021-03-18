from flask import Flask, Response
from flask.testing import FlaskClient


class UserClient:

    def __init__(self, app: Flask):
        self.client: FlaskClient = app.test_client()
        self.headers = dict()

    def get_users(self) -> Response:
        return self.client.get('/api/v1.0/users/')

    def invalid_data_sign_up(self, emails: str, passwords: str) -> Response:
        return self.client.post('/api/v1.0/users/signUp', json={
            'emails': emails,
            'passwords': passwords
        })

    def sign_up(self, email: str, password: str) -> Response:
        return self.client.post('/api/v1.0/users/signUp', json={
            'email': email,
            'password': password
        })

    def invalid_data_login(self, emails: str, passwords: str) -> Response:
        return self.client.post('/api/v1.0/users/logIn', json={
            'emails': emails,
            'passwords': passwords
        })

    def login(self, email: str, password: str) -> Response:
        return self.client.post('/api/v1.0/users/logIn', json={
            'email': email,
            'password': password
        })

    def me(self, token) -> Response:
        return self.client.get('/api/v1.0/users/me', headers={
            'token': token
        })

    def change_my_data(self,
                       token: str,
                       username: str,
                       first_name: str,
                       last_name: str) -> Response:
        return self.client.put('/api/v1.0/users/me', json={
            'token': token,
            'username': username,
            'first_name': first_name,
            'last_name': last_name
        })

    def delete_me(self, token: str) -> Response:
        return self.client.delete('/api/v1.0/users/me', json={
            'token': token
        })

    def logout(self, token: str) -> Response:
        return self.client.post('/api/v1.0/users/me/logOut', json={
            'token': token
        })

    def followers(self, my_id: str) -> Response:
        return self.client.get(f'/api/v1.0/users/id={my_id}/followers')

    def followed(self, my_id: str) -> Response:
        return self.client.get(f'/api/v1.0/users/id={my_id}/followed')

    def subscribe(self, token: str, _id: str) -> Response:
        return self.client.post('/api/v1.0/users/me/follow', json={
            'token': token,
            '_id': _id
        })

    def unsubscribe(self, token: str, _id: str) -> Response:
        return self.client.delete('/api/v1.0/users/me/follow', json={
            'token': token,
            '_id': _id
        })






