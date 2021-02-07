from flasgger import SwaggerView
from flask import jsonify, request
from .utils import *


class UserLoginView(SwaggerView):
    """
    TODO create login view
    """


class UserSignUpView(SwaggerView):

    def post(self):
        """
        file: docs/post/sign_up.yml
        """
        response = request.get_json()
        if 'email' not in response or 'password' not in response:
            return 'Invalid data', 400

        if get_user_by_email(email=response['email']):
            return 'User already exists', 401

        user = Users.create_user(email=response['email'],
                                 password=response['password'])
        user.save()

        return jsonify({'token': user.auth_token})


class MeView(SwaggerView):

    def get(self):
        response = request.get_json()

        if 'token' not in response:
            return 'Invalid data', 400

        user = check_token(token=response['token'])

        if not user:
            return 'User could not be found', 404

        return jsonify(user.to_json())

    def put(self):
        response = request.get_json()

        if 'username' not in response or 'first_name' not in response or \
                'last_name' not in response or 'token' not in response:
            return 'Invalid data', 400

        user_check = check_token(token=response['token'])

        if not user_check:
            return 'User could not be found', 404

        user = add_data_to_user(user=user_check,
                                first_name=response['first_name'],
                                last_name=response['last_name'],
                                username=response['username'])

        return jsonify(user.to_json())

    def delete(self):
        response = request.get_json()

        if 'token' not in response:
            return 'Invalid data', 400

        user = check_token(token=response['token'])

        if not user:
            return 'User could not be found', 404

        user.delete()

        return 'User has been deleted'


class UserLogOutView(SwaggerView):
    """
    TODO create view for logout logged user
    """


class UsersView(SwaggerView):

    def get(self):
        users = Users.objects()
        users_array = []

        if not users:
            return 'Users cannot be found', 404

        for user in users:
            users_array.append(user.to_json())
        return jsonify({'users': users_array})


class UserByIdView(SwaggerView):

    def get(self, id: str):
        _id = ObjectId(id)
        user = get_user_by_id(_id=_id)

        if not user:
            return 'User could not be found', 404

        return jsonify(user.to_json())


class UserByUsernameView(SwaggerView):

    def get(self, username: str):
        user = get_user_by_username(username=username)

        if not user:
            return 'User could not be found', 404

        return jsonify(user.to_json())


class UsersByFirstNameView(SwaggerView):

    def get(self, first_name: str):
        users = get_users_by_first_name(first_name=first_name)

        if not users:
            return 'Users could not be found', 404

        return jsonify({'users': users})


class UsersByLastNameView(SwaggerView):

    def get(self, last_name: str):
        users = get_users_by_last_name(last_name=last_name)

        if not users:
            return 'Users could not be found', 404

        return jsonify({'users': users})


class FollowersView(SwaggerView):
    """
    TODO create view for followers
    """


class FollowedView(SwaggerView):
    """
    TODO create view for followed
    """
