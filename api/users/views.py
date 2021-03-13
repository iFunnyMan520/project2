from flasgger import SwaggerView
from flask import jsonify, request
from marshmallow import ValidationError
from api.users import inputs
from .utils import *


class UserLoginView(SwaggerView):

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

    def get(self):
        """
        file: docs/get/me.yml
        """
        try:
            response = inputs.TokenSchema().load(request.get_json())
        except ValidationError as err:
            return jsonify(err.messages), 400

        user = check_token(token=response['token'])

        if not user:
            return jsonify({'message': 'User could not be found'}), 404

        return jsonify(user.to_json())

    def put(self):
        try:
            response = inputs.UpdateMeSchema().load(request.get_json())
        except ValidationError as err:
            return jsonify(err.messages), 400

        user_check = check_token(token=response['token'])

        if not user_check:
            return jsonify({'message': 'User could not be found'}), 404

        if get_user_by_username(username=response['username']) and not \
                user_check.username == response['username']:
            return jsonify({'message': 'Username already exists'}), 401

        user = add_data_to_user(user=user_check,
                                first_name=response['first_name'],
                                last_name=response['last_name'],
                                username=response['username'])

        return jsonify(user.to_json())

    def delete(self):
        try:
            response = inputs.TokenSchema().load(request.get_json())
        except ValidationError as err:
            return jsonify(err.messages), 400

        user = check_token(token=response['token'])

        if not user:
            return jsonify({'message': 'User could not be found'}), 404

        user.delete()

        return jsonify({'message': 'User has been deleted'})


class UserLogOutView(SwaggerView):

    def post(self):
        try:
            response = inputs.TokenSchema().load(request.get_json())
        except ValidationError as err:
            return jsonify(err.messages), 400

        user = check_token(token=response['token'])

        if not user:
            return jsonify({'message': 'User is not logged in'}), 401

        user.auth_token = None
        user.save()
        return jsonify({'message': 'You are logged out now'})


class UsersView(SwaggerView):

    def get(self):
        users = Users.objects()
        users_array = []

        if not users:
            return jsonify({'message': 'Users cannot be found'}), 404

        for user in users:
            users_array.append(user.to_json())
        return jsonify({'users': users_array})


class UserByIdView(SwaggerView):

    def get(self, id: str):
        _id = ObjectId(id)
        user = get_user_by_id(_id=_id)

        if not user:
            return jsonify({'message': 'User could not be found'}), 404

        return jsonify(user.to_json())


class UserByUsernameView(SwaggerView):

    def get(self, username: str):
        user = get_user_by_username(username=username)

        if not user:
            return jsonify({'message': 'User could not be found'}), 404

        return jsonify(user.to_json())


class UsersByFirstNameView(SwaggerView):

    def get(self, first_name: str):
        users = get_users_by_first_name(first_name=first_name)

        if not users:
            return jsonify({'message': 'Users could not be found'}), 404

        return jsonify({'users': users})


class UsersByLastNameView(SwaggerView):

    def get(self, last_name: str):
        users = get_users_by_last_name(last_name=last_name)

        if not users:
            return jsonify({'message': 'Users could not be found'}), 404

        return jsonify({'users': users})


class FollowersView(SwaggerView):

    def get(self, id: str):
        _id = ObjectId(id)
        user = get_user_by_id(_id=_id)

        if not user:
            return jsonify({'message': 'User could not be found'}), 404

        followers = get_followers(user=user)
        return jsonify(followers)


class FollowedView(SwaggerView):

    def get(self, id: str):
        _id = ObjectId(id)
        user = get_user_by_id(_id=_id)

        if not user:
            return jsonify({'message': 'User could not be found'}), 404

        followed = get_followed(user=user)
        return jsonify(followed)


class MyFollowView(SwaggerView):

    def post(self):
        try:
            response = inputs.FollowSchema().load(request.get_json())
        except ValidationError as err:
            return jsonify(err.messages), 400

        user = check_token(token=response['token'])

        if not user:
            return jsonify({'message': 'User is not logged in'}), 401

        _id = ObjectId(response['_id'])
        followed = get_user_by_id(_id=_id)

        if not followed:
            return jsonify({'message': 'User could not be found'}), 404

        sub = subscribe(user, followed)

        if not sub:
            return jsonify({'message': 'You have already subscribed'})

        return jsonify({'message': 'You have subscribed now'}), 200

    def delete(self):
        try:
            response = inputs.FollowSchema().load(request.get_json())
        except ValidationError as err:
            return jsonify(err.messages), 400

        user = check_token(token=response['token'])

        if not user:
            return jsonify({'message': 'User is not logged in'}), 401

        _id = ObjectId(response['_id'])
        followed = get_user_by_id(_id=_id)

        if not followed:
            return jsonify({'message': 'User could not be found'}), 404

        unsubscribe(user, followed)

        return jsonify({'message': 'You have unsubscribed now'}), 200
