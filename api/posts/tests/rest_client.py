from typing import List

from flask import Flask, Response
from flask.testing import FlaskClient


class PostClient:

    def __init__(self, app: Flask):
        self.client: FlaskClient = app.test_client()
        self.key: str = '4da5933b-120a-4108-8670-faa83ca6a43a'

    def posts(self, token: str) -> Response:
        return self.client.get('/api/v1.0/posts/', headers={
            'token': token,
            'secret_key': self.key
        })

    def create(self,
               token: str,
               title: str,
               tags: List[str],
               description: str,
               only_for_followers: bool = False) -> Response:
        return self.client.post('/api/v1.0/posts/me', json={
            'title': title,
            'tags': tags,
            'description': description,
            'only_for_followers': only_for_followers
        }, headers={
            'token': token,
            'secret_key': self.key
        })

    def feed(self, token: str) -> Response:
        return self.client.get('/api/v1.0/posts/feed', headers={
            'token': token,
            'secret_key': self.key
        })

    def like(self, token: str, _id: str) -> Response:
        return self.client.post('/api/v1.0/posts/like', json={
            '_id': _id
        }, headers={
            'token': token,
            'secret_key': self.key
        })

    def dislike(self, token: str, _id: str) -> Response:
        return self.client.delete('/api/v1.0/posts/like', json={
            '_id': _id
        }, headers={
            'token': token,
            'secret_key': self.key
        })

    def view(self, token: str, _id: str) -> Response:
        return self.client.post('/api/v1.0/posts/view', json={
            '_id': _id
        }, headers={
            'token': token,
            'secret_key': self.key
        })
