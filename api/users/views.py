from flasgger import SwaggerView
from flask import jsonify
from .utils import *
from api.posts.models import Posts


class UserView(SwaggerView):

    def get(self):

        return 'Ok'
