from typing import List

from api import db
from datetime import datetime

from api.users.models import Users


class Picture(db.EmbeddedDocument):
    """
    TODO create model for picture
    """


class Likes(db.EmbeddedDocument):
    qty: int = db.IntField(default=0)
    likes: List[str] = db.ListField(db.StringField())

    def like(self, _id: str):
        self.qty += 1
        self.likes.append(_id)

    def dislike(self, _id: str):
        self.qty -= 1
        self.likes.remove(_id)


class Views(db.EmbeddedDocument):
    qty: int = db.IntField(default=0)
    views: List[str] = db.ListField(db.StringField())

    def view(self, _id: str):
        self.qty += 1
        self.views.append(_id)


class Posts(db.Document):
    title: str = db.StringField()
    description: str = db.StringField(default='There is no description')
    author: 'Users' = db.ReferenceField(Users)
    tags: List[str] = db.ListField(db.StringField(), default=[])
    only_for_followers: bool = db.BooleanField(default=False)
    created_at: datetime = db.DateTimeField(default=datetime.now)
    likes: 'Likes' = db.EmbeddedDocumentField(Likes)
    views: 'Views' = db.EmbeddedDocumentField(Views)

    @property
    def prev_description(self):
        if not self.description or len(self.description) <= 20:
            return None
        return self.description[:20] + '...'

    @property
    def views_count(self) -> int:
        if not self.views:
            return 0
        return len(self.views)

    def is_liked(self, user: 'Users'):
        return str(user.pk) in self.likes.likes

    def is_viewed(self, user: 'Users'):
        return str(user.pk) in self.views.views

    @classmethod
    def create(cls, title: str, author: Users, tags: List[str],
               description: str, only_for_followers: bool):
        post: 'Posts' = cls(title=title, author=author, tags=tags,
                            only_for_followers=only_for_followers,
                            description=description)
        post.save()
        return post

    def add_new_tag(self, tag: str):
        self.tags.append(tag)
        self.save()

    @staticmethod
    def by_tag(tag: str, user: 'Users') -> List[dict] or None:
        posts: List['Posts'] = Posts.objects(tags=tag)

        if not posts:
            return

        posts_list = []

        for post in posts:
            posts_list.append(post.to_json(user))

        return posts_list

    @staticmethod
    def by_user(user: 'Users', current: 'Users') -> List[dict] or None:
        posts: List['Posts'] = Posts.objects(author=user).order_by(
            '-created_at')
        if not posts:
            return

        posts_list = []

        for post in posts:
            posts_list.append(post.to_json(current))
        return posts_list

    @staticmethod
    def my_followed_posts(current: 'Users'):
        _id: str = str(current.pk)

        posts: List['Posts'] = Posts.query(str(Posts.author.pk) in
                                           current.followed.followed).order_by(
            '-created_at'
        )

        posts_list = []

        for post in posts:
            posts_list.append(post.to_json(current))

        return posts_list

    def like_post(self, user: 'Users') -> 'Posts':
        """
        Likes post
        :param user: user who likes the post
        :return: liked post
        """
        if not self.likes:
            new_like: 'Likes' = Likes()
            new_like.like(_id=str(user.pk))
            self.likes = new_like
        else:
            self.likes.like(_id=str(user.pk))

        self.save()

        return self

    def dislike_post(self, user: 'Users') -> 'Posts':
        """
        Dislikes post
        :param user: user who dislikes the post
        :return: disliked post
        """
        self.likes.dislike(_id=str(user.pk))

        return self

    def view_post(self, user: 'Users') -> 'Posts':
        """
        Views post
        :param user: user who viewed the post
        :return: viewed post
        """
        if not self.views:
            new_view = Views()
            new_view.view(str(user.pk))
            self.views = new_view
        else:
            self.views.view(str(user.pk))

        self.save()

        return self

    def to_json(self, user: 'Users'):
        return {
            '_id': str(self.pk),
            'title': self.title,
            'description': self.description,
            'prev_description': self.prev_description,
            'tags': self.tags,
            'only_for_followers': self.only_for_followers,
            'created_at': self.created_at,
            'user_likes': self.likes,
            'likes': self.likes,
            'is_liked': self.is_liked(user),
            'is_viewed': self.is_viewed(user),
            'views': self.views_count
        }
