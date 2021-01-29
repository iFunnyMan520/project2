from api import app
from api.users import views


app.add_url_rule('/api/v1.0/users/',
                 view_func=views.UsersView.as_view('users'))


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
