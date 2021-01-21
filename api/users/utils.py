from .models import Users


def create_new_user(email: str, password: str) -> Users or str:
    """
    Creates a new user with a hashed password and adds it to the database
    :param email: user email
    :param password: user password to be hashed
    :return: user model or information that the user already exists
    """
    if Users.objects(email=email):
        return 'User already exists'

    user = Users.create_user(email, password)
    user.save()

    return user


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


def get_users_by_first_name():
    # TODO create a function that return a list of users with the same first
    #  name
    pass


def get_users_by_last_name():
    # TODO create a function that return a list of users with the same last
    #  name
    pass


def get_user_by_email(email: str) -> Users or None:
    """
    Gets user by email
    :param email:
    :return: user with received email or None if that user doesn't exist
    """
    user = Users.objects(email=email).first()
    return user


def get_user_by_username(username: str) -> Users or None:
    """
    Gets user by username
    :param username:
    :return: user with received username or None if that user doesn't exist
    """
    user = Users.objects(username=username).first()
    return user
