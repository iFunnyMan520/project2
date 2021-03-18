from typing import List

from bson import ObjectId

from api.posts.models import Posts


def get_post_by_id(_id: str) -> dict or None:
    """
    Gets post by its id
    :param _id: post id
    :return: post dict or None, if post with that id does not exist
    """
    post: 'Posts' = Posts.objects(_id=ObjectId(_id))

    if not post:
        return None

    return post.to_json()


def posts_per_page(page: int, count: int) -> List[dict] or None:
    """
    Gets posts on the page
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
        posts_list.append(post.to_json())

    return posts_list
