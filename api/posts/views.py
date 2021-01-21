from flask import jsonify
from flasgger import SwaggerView
from .models import Posts


class PostsView(SwaggerView):

    def get(self):
        post = Posts(title='First post')
        post.save()
        return 'Ok'
