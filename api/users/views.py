from flasgger import SwaggerView
from flask import jsonify, request
from marshmallow import ValidationError
from api.users import inputs
from .decorators import only_authorized, with_secret_key
from .utils import *
from ..posts.models import Posts


class UserLoginView(SwaggerView):

    @with_secret_key
    def post(self):
        try:
            response = inputs.AuthSchema().load(request.get_json())
        except ValidationError as err:
            return jsonify(err.messages), 400

        user = check_user(email=response['email'],
                          password=response['password'])

        if not user:
            return jsonify({'message': 'Wrong email or password'}), 404

        if user.auth_token:
            return jsonify({'message': 'User is already logged in'})

        user.auth_token = Users.generate_token()
        user.save()

        return jsonify({'token': user.auth_token})


class UserSignUpView(SwaggerView):

    @with_secret_key
    def post(self):
        """
        file: docs/post/sign_up.yml
        """
        try:
            response = inputs.AuthSchema().load(request.get_json())
        except ValidationError as err:
            return jsonify(err.messages), 400

        if get_user_by_email(email=response['email']):
            return jsonify({'message': 'User already exists'}), 401

        user = Users.create_user(email=response['email'],
                                 password=response['password'])

        return jsonify({'token': user.auth_token})


class MeView(SwaggerView):

    @only_authorized
    def get(self, user: 'Users'):
        """
        file: docs/get/me.yml
        """
        posts = Posts.by_user(user, user)
        return jsonify({'me': user.to_json(), 'posts': posts})

    @only_authorized
    def put(self, user: 'Users'):
        try:
            response = inputs.UpdateMeSchema().load(request.get_json())
        except ValidationError as err:
            return jsonify(err.messages), 400

        if get_user_by_username(username=response['username']) and not \
                user.username == response['username']:
            return jsonify({'message': 'Username already exists'}), 401

        user = add_data_to_user(user=user,
                                first_name=response['first_name'],
                                last_name=response['last_name'],
                                username=response['username'])

        return jsonify(user.to_json())

    @only_authorized
    def delete(self, user: 'Users'):
        user.delete()

        return jsonify({'message': 'User has been deleted'})


class UserLogOutView(SwaggerView):

    @only_authorized
    def post(self, user: 'Users'):

        user.auth_token = None
        user.save()
        return jsonify({'message': 'You are logged out now'})


class UsersView(SwaggerView):

    @only_authorized
    def get(self, user: 'Users'):
        users = Users.objects()
        users_array = []

        if not users:
            return jsonify({'message': 'Users cannot be found'}), 404

        for each_user in users:
            users_array.append(each_user.to_json(user))
        return jsonify({'users': users_array})


class UserByIdView(SwaggerView):

    @only_authorized
    def get(self, id: str, user: 'Users'):
        _id = ObjectId(id)
        user_by_id = get_user_by_id(_id=_id)

        if not user_by_id:
            return jsonify({'message': 'User could not be found'}), 404

        return jsonify(user_by_id.to_json(user))


class UserByUsernameView(SwaggerView):

    @only_authorized
    def get(self, username: str, user: 'Users'):
        user_by_username = get_user_by_username(username=username)

        if not user_by_username:
            return jsonify({'message': 'User could not be found'}), 404

        return jsonify(user_by_username.to_json(user))


class UsersByFirstNameView(SwaggerView):

    @only_authorized
    def get(self, first_name: str, user: 'Users'):
        users = get_users_by_first_name(first_name=first_name, user=user)

        if not users:
            return jsonify({'message': 'Users could not be found'}), 404

        return jsonify({'users': users})


class UsersByLastNameView(SwaggerView):

    @only_authorized
    def get(self, last_name: str, user: 'Users'):
        users = get_users_by_last_name(last_name=last_name, user=user)

        if not users:
            return jsonify({'message': 'Users could not be found'}), 404

        return jsonify({'users': users})


class FollowersView(SwaggerView):

    @only_authorized
    def get(self, id: str, user: 'Users'):
        _id = ObjectId(id)
        user_follow = get_user_by_id(_id=_id)

        if not user_follow:
            return jsonify({'message': 'User could not be found'}), 404

        followers = get_followers(user_follow=user_follow, user=user)
        return jsonify(followers)


class FollowedView(SwaggerView):

    @only_authorized
    def get(self, id: str, user: 'Users'):
        _id = ObjectId(id)
        user_follow = get_user_by_id(_id=_id)

        if not user_follow:
            return jsonify({'message': 'User could not be found'}), 404

        followed = get_followed(user_follow=user_follow, user=user)
        return jsonify(followed)


class MyFollowView(SwaggerView):

    @only_authorized
    def post(self, user: 'Users'):
        try:
            response = inputs.FollowSchema().load(request.get_json())
        except ValidationError as err:
            return jsonify(err.messages), 400

        _id = ObjectId(response['_id'])
        followed = get_user_by_id(_id=_id)

        if not followed:
            return jsonify({'message': 'User could not be found'}), 404

        sub = subscribe(user, followed)

        if not sub:
            return jsonify({'message': 'You have already subscribed'})

        return jsonify({'message': 'You have subscribed now'})

    @only_authorized
    def delete(self, user: 'Users'):
        try:
            response = inputs.FollowSchema().load(request.get_json())
        except ValidationError as err:
            return jsonify(err.messages), 400

        _id = ObjectId(response['_id'])
        followed = get_user_by_id(_id=_id)

        if not followed:
            return jsonify({'message': 'User could not be found'}), 404

        unsubscribe(user, followed)

        return jsonify({'message': 'You have unsubscribed now'})
