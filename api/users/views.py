from flasgger import SwaggerView
from flask import jsonify, request

from .models import Users
from .utils import *


class UsersView(SwaggerView):

    def get(self):
        response = Users.objects()
        users = []
        for user in response:
            users.append(user.to_json())
        return jsonify({'users': users})

    def post(self):
        response = request.get_json()
        if 'email' not in response or 'password' not in response:
            return 'Invalid data', 400

        user = create_new_user(email=response['email'],
                               password=response['password'])

        if not user:
            return 'User already exists', 401

        return 'User has been created', 201


class UserByIdView(SwaggerView):

    def get(self, id: str):
        _id = ObjectId(id)
        user = get_user_by_id(id=_id)

        if not user:
            return 'User could not be found', 404

        return jsonify(user.to_json())

    def put(self, id: str):
        response = request.get_json()

        if 'first_name' not in response or 'username' not in response or \
                'last_name' not in response:
            return 'Invalid data', 400

        _id = ObjectId(id)
        user = get_user_by_id(id=_id)

        if not user:
            return 'User could not be found', 404

        updated_user = add_data_to_user(user=user,
                                        first_name=response['first_name'],
                                        last_name=response['last_name'],
                                        username=response['username'])

        if not updated_user:
            return 'Username is already taken', 401

        return updated_user.to_json(), 200


class UserByUsernameView(SwaggerView):
    pass


class UsersByFirstNameView(SwaggerView):
    pass


class UsersByLastNameView(SwaggerView):
    pass
