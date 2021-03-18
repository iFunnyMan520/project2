from api.posts import utils


def test_query():
    posts = utils.posts_per_page(8, 2)

    assert posts is None
