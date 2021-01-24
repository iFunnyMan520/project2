from api.users.utils import *


email = 'test_email@gmail.com'
password = 'test123'
first_name = 'Test first name'
last_name = 'Test last name'
username = 'test username'


def test_create_user():
    new_user = create_new_user(email=email, password=password)
    user = get_user_by_email(email=email)

    assert new_user.email == user.email
    assert new_user.password == user.password


def test_create_the_same_user():
    new_user = create_new_user(email=email, password=password)

    assert new_user is None


def test_check_user():
    user = get_user_by_email(email=email)
    user1 = check_user(email=email, password=password)

    assert user.email == user1.email
    assert user.password == user1.password

    user2 = check_user(email=email, password='test')

    assert user2 is None

    user3 = check_user(email='test', password=password)

    assert user3 is None


def test_add_data():
    user = get_user_by_email(email=email)
    modified_user = add_data_to_user(user=user, first_name=first_name,
                                     last_name=last_name, username=username)

    same_user = get_user_by_email(email=email)

    assert modified_user.email == same_user.email
    assert modified_user.first_name == same_user.first_name
    assert modified_user.last_name == same_user.last_name
    assert modified_user.username == same_user.username


def test_get_user_by_username():
    user_by_username = get_user_by_username(username=username)
    user = get_user_by_email(email=email)

    assert user_by_username.email == user.email
    assert user_by_username.first_name == user.first_name
    assert user_by_username.last_name == user.last_name
    assert user_by_username.username == user.username

    user.delete()
    user_by_username = get_user_by_username(username=username)

    assert user_by_username is None


def test_get_users_by_first_name():
    user1 = Users(first_name=first_name, email='test1')
    user2 = Users(first_name=first_name, email='test2')
    user1.save()
    user2.save()

    users = [user1, user2]

    get_users = get_users_by_first_name(first_name=first_name)

    assert users == get_users

    user1.delete()
    user2.delete()

    assert get_users_by_first_name(first_name=first_name) is None


def test_get_users_by_last_name():
    user1 = Users(last_name=last_name, email='test1')
    user2 = Users(last_name=last_name, email='test2')
    user1.save()
    user2.save()

    users = [user1, user2]

    get_users = get_users_by_last_name(last_name=last_name)

    assert users == get_users

    user1.delete()
    user2.delete()

    assert get_users_by_last_name(last_name=last_name) is None


def test_get_user_by_id():
    new_user = create_new_user(email=email, password=password)
    user = get_user_by_id(id=new_user.pk)

    assert user == new_user

    new_user.delete()
