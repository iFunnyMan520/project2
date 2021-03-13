from api import app
from api.users import views


app.add_url_rule('/api/v1.0/users/',
                 view_func=views.UsersView.as_view('users'))


app.add_url_rule('/api/v1.0/users/signUp',
                 view_func=views.UserSignUpView.as_view('signUp'),
                 methods=['POST'])


app.add_url_rule('/api/v1.0/users/logIn',
                 view_func=views.UserLoginView.as_view('logIn'),
                 methods=['POST'])


app.add_url_rule('/api/v1.0/users/me',
                 view_func=views.MeView.as_view('me'),
                 methods=['PUT', 'GET', 'DELETE'])


app.add_url_rule('/api/v1.0/users/me/logOut',
                 view_func=views.UserLogOutView.as_view('logOut'),
                 methods=['POST'])


app.add_url_rule('/api/v1.0/users/me/follow',
                 view_func=views.MyFollowView.as_view('my_follow'),
                 methods=['POST', 'DELETE'])


app.add_url_rule('/api/v1.0/users/id=<string:id>',
                 view_func=views.UserByIdView.as_view('user_by_id'))


app.add_url_rule('/api/v1.0/users/username=<string:username>',
                 view_func=views.UserByUsernameView.as_view(
                     'user_by_username'))


app.add_url_rule('/api/v1.0/users/first_name=<string:first_name>',
                 view_func=views.UsersByFirstNameView.as_view(
                     'users_by_first_name'))


app.add_url_rule('/api/v1.0/users/last_name=<string:last_name>',
                 view_func=views.UsersByLastNameView.as_view(
                     'users_by_last_name'))


app.add_url_rule('/api/v1.0/users/id=<string:id>/followers',
                 view_func=views.FollowersView.as_view('followers'))


app.add_url_rule('/api/v1.0/users/id=<string:id>/followed',
                 view_func=views.FollowedView.as_view('followed'))
