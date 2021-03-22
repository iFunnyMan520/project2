from typing import List

from bson import ObjectId

from api.posts.models import Posts
from api.users.models import Users


def get_post_by_id(_id: str) -> 'Posts' or None:
    """
    Gets post by its id
    :param _id: post id
    :return: post dict or None, if post with that id does not exist
    """
    post: 'Posts' = Posts.objects(_id=ObjectId(_id))

    return post


def posts_per_page(page: int, count: int, user: 'Users') -> List[dict] or None:
    """
    Gets posts on the page
    :param user:
    :param page: number of page
    :param count: number of posts to be shown on the page
    :return: list of post dicts or None
    """
    start: int = (page - 1) * count
    end: int = start + count

    posts: List['Posts'] = Posts.objects[start:end].order_by('-created_at')

    if not posts:
        return

    posts_list = []

    for post in posts:
        posts_list.append(post.to_json(user))

    return posts_list
