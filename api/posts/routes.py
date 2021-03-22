from api import app
from .views import PostsView


app.add_url_rule('/api/v1.0/posts/',
                 view_func=PostsView.as_view('posts'))
