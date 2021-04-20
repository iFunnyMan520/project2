from api import app
from api.posts import views


app.add_url_rule('/api/v1.0/posts/',
                 view_func=views.PostsView.as_view('posts'))


app.add_url_rule('/api/v1.0/posts/me',
                 view_func=views.MyPostsView.as_view('my_post'),
                 methods=['POST'])


app.add_url_rule('/api/v1.0/posts/feed',
                 view_func=views.NewsFeedView.as_view('feed'))


app.add_url_rule('/api/v1.0/posts/byId',
                 view_func=views.PostByIdVIew.as_view('by_id'))


app.add_url_rule('/api/v1.0/posts/byTag',
                 view_func=views.PostsByTagView.as_view('by_tag'))


app.add_url_rule('/api/v1.0/posts/like',
                 view_func=views.LikeView.as_view('like'),
                 methods=['POST', 'DELETE'])


app.add_url_rule('/api/v1.0/posts/view',
                 view_func=views.ViewPostView.as_view('view'),
                 methods=['POST'])
