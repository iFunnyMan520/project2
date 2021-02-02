from flasgger import SwaggerView
from flask import jsonify, request
from .utils import *


class UserLogin(SwaggerView):
    """
    TODO create login with token
    """


class UserSignUp(SwaggerView):
    """
    TODO create user registration with token
    """


class Me(SwaggerView):
    """
    TODO create view for logged user
    """


class UserLogOut(SwaggerView):
    """
    TODO create view for logout logged user
    """


class UsersView(SwaggerView):

    def get(self):
        users = Users.objects()
        users_array = []
        for user in users:
            users_array.append(user.to_json())
        return jsonify({'users': users_array})

    def post(self):
        response = request.get_json()
        if 'email' not in response or 'password' not in response:
            return 'Invalid data', 400

        if get_user_by_email(email=response['email']):
            return 'User already exists', 401

        user = Users.create_user(email=response['email'],
                                 password=response['password'])
        user.save()

        return 'User has been created', 201


class UserByIdView(SwaggerView):

    def get(self, id: str):
        _id = ObjectId(id)
        user = get_user_by_id(_id=_id)

        if not user:
            return 'User could not be found', 404

        return jsonify(user.to_json())

    def put(self, id: str):
        response = request.get_json()

        if 'first_name' not in response or 'username' not in response or \
                'last_name' not in response:
            return 'Invalid data', 400

        _id = ObjectId(id)
        user = get_user_by_id(_id=_id)

        if not user:
            return 'User could not be found', 404

        updated_user = add_data_to_user(user=user,
                                        first_name=response['first_name'],
                                        last_name=response['last_name'],
                                        username=response['username'])

        if not updated_user:
            return 'Username is already taken', 401

        return updated_user.to_json()

    def delete(self, id: str):
        _id = ObjectId(id)
        user = get_user_by_id(_id=_id)

        if not user:
            return 'User could not be found', 404

        user.delete()

        return 'User has been deleted'


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
