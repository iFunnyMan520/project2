import pytest
from flask import Flask, Response

from api.posts.models import Posts
from api.posts.tests.rest_client import PostClient


@pytest.fixture(scope='module')
def post(server_app: Flask):
    return PostClient(server_app)


@pytest.fixture
def my_token(me) -> str:
    return me.auth_token


def test_my_posts(post: PostClient, my_token):
    response: 'Response' = post.posts(my_token)

    assert len(response.get_json()['posts']) == 6


def test_create_post(post: PostClient, my_token):
    response: 'Response' = post.create(my_token, 'my first post',
                                       ['my', 'post'], 'no description')

    assert response.get_json()['message'] == 'You have successful added new post'

    response: 'Response' = post.create(my_token, 'my first post',
                                       ['some', 'tag', 'my'], 'no description')

    assert response.get_json()['message'] == 'You have successful added new post'


def test_feed(post: PostClient, my_token):
    response: 'Response' = post.feed(my_token)

    assert len(response.get_json()['posts']) == 2
