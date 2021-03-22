from typing import List

from bson import ObjectId
from flask import jsonify, request
from flasgger import SwaggerView
from marshmallow import ValidationError

from api.posts.models import Posts
from api.users.decorators import only_authorized
from api.users.models import Users
from api.posts import inputs
from api.posts import utils


class PostsView(SwaggerView):

    @only_authorized
    def get(self, user: 'Users'):
        posts: List['Posts'] = Posts.query().order_by('-created_at')

        posts_list = []

        for post in posts:
            posts_list.append(post.to_json(user))

        return jsonify({'posts': posts_list, 'me': user.to_json()})


class MyPostsView(SwaggerView):

    @only_authorized
    def post(self, user: 'Users'):
        try:
            response = inputs.NewPostSchema().load(request.get_json())
        except ValidationError as err:
            return jsonify(err.messages), 400

        Posts.create(title=response['title'],
                     author=user,
                     tags=response['tags'],
                     description=response['description'],
                     only_for_followers=response['only_for_followers'])

        return jsonify({'message': 'You have successful added new post'})


class NewsFeedView(SwaggerView):

    @only_authorized
    def get(self, user: 'Users'):
        posts = Posts.my_followed_posts(user)

        return jsonify({'posts': posts, 'me': user.to_json()})


class PostByIdVIew(SwaggerView):

    @only_authorized
    def get(self, user: 'Users'):
        try:
            response = inputs.IdSchema().load(request.get_json())
        except ValidationError as err:
            return jsonify(err.messages), 400

        post: 'Posts' = utils.get_post_by_id(response['_id'])

        if not post:
            return jsonify({'message': 'Post cannot be found'}), 404

        return jsonify(post.to_json(user))


class PostsByTagView(SwaggerView):

    @only_authorized
    def get(self, user: 'Users'):
        try:
            response = inputs.PostsByTagSchema().load(request.get_json())
        except ValidationError as err:
            return jsonify(err.messages), 400

        posts: List[dict] = Posts.by_tag(tag=response['tag'], user=user)

        return jsonify({'posts:': posts, 'me': user.to_json()})


class LikeView(SwaggerView):

    @only_authorized
    def post(self, user: 'Users'):
        try:
            response = inputs.IdSchema().load(request.get_json())
        except ValidationError as err:
            return jsonify(err.messages), 400

        post: 'Posts' = utils.get_post_by_id(response['_id'])

        if not post:
            return jsonify({'message': 'Post cannot be found'}), 404

        post.like_post(user)

        return jsonify({'is_liked': post.is_liked(user)})

    @only_authorized
    def delete(self, user: 'Users'):
        try:
            response = inputs.IdSchema().load(request.get_json())
        except ValidationError as err:
            return jsonify(err.messages), 400

        post: 'Posts' = utils.get_post_by_id(response['_id'])

        if not post:
            return jsonify({'message': 'Post cannot be found'}), 404

        post.dislike_post(user)

        return jsonify({'is_liked': post.is_liked(user)})


class ViewPostView(SwaggerView):

    @only_authorized
    def post(self, user: 'Users'):
        try:
            response = inputs.IdSchema().load(request.get_json())
        except ValidationError as err:
            return jsonify(err.messages), 400

        post: 'Posts' = utils.get_post_by_id(response['_id'])

        if not post:
            return jsonify({'message': 'Post cannot be found'}), 404

        post.view_post(user)

        return jsonify({'is_viewed': post.is_viewed(user)})
