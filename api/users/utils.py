from typing import List

from bson import ObjectId

from .models import Users


def create_new_user(email: str, password: str) -> Users or None:
    """
    Creates a new user with a hashed password and adds it to the database
    :param email: user email
    :param password: user password to be hashed
    :return: user model or information that the user already exists
    """
    if Users.objects(email=email):
        return None

    user = Users.create_user(email, password)
    user.save()

    return user


def add_user_avatar():
    # TODO create a function to add user avatar
    pass


def check_user(email: str, password: str) -> Users or None:
    """
    Checks that the sent data is equal to the data in the database
    :param email: sent email that compares with all emails in database
    :param password: sent password that compares with password in database
    :return: user model or information that the data
    """
    user = get_user_by_email(email)

    if not user:
        return None

    if not user.check_pass(password):
        return None

    return user


def add_data_to_user(user: Users,
                     first_name: str = None,
                     last_name: str = None,
                     username: str = None) -> Users or None:
    """
    Adds new data to user
    :param user: user model
    :param first_name: user first name
    :param last_name: user last name
    :param username: username
    :return: user model with new data
    """

    if get_user_by_username(username):
        return None

    user.first_name = first_name
    user.last_name = last_name
    user.username = username
    user.save()

    return user


def get_users_by_first_name(first_name: str) -> List[Users] or None:
    """
    Gets all users with the same first name
    :param first_name: sent first name
    :return: list of users or None
    """
    users_list = []
    users = Users.objects(first_name=first_name)

    if not users:
        return None

    for user in users:
        users_list.append(user)

    return users_list


def get_users_by_last_name(last_name: str) -> List[Users] or None:
    """
    Gets all users with the same last name
    :param last_name: sent last name
    :return: list of users or None
    """
    users_list = []
    users = Users.objects(last_name=last_name)

    if not users:
        return None

    for user in users:
        users_list.append(user)

    return users_list


def get_user_by_id(id: ObjectId) -> Users or None:
    """
    Gets user by id
    :param id: sent id
    :return: user or None
    """
    user = Users.objects(pk=id).first()
    return user


def get_user_by_email(email: str) -> Users or None:
    """
    Gets user by email
    :param email: sent email
    :return: user with received email or None if that user doesn't exist
    """
    user = Users.objects(email=email).first()
    return user


def get_user_by_username(username: str) -> Users or None:
    """
    Gets user by username
    :param username: sent username
    :return: user with received username or None if that user doesn't exist
    """
    user = Users.objects(username=username).first()
    return user
