from api import app
from .views import UserView


app.add_url_rule('/api/v1.0/users/',
                 view_func=UserView.as_view('users'))
