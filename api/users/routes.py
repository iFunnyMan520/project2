from api import app
from api.users import views


app.add_url_rule('/api/v1.0/users/',
                 view_func=views.UsersView.as_view('users'))


app.add_url_rule('/api/v1.0/users/id=<string:id>',
                 view_func=views.UserByIdView.as_view('user_by_id'))

