"""Reddit downloader test suite."""
from pytest_mock import MockFixture

from vidgen import reddit


def test_process_text() -> None:
    """The text processor removes a zero width space and an html entity correctly."""
    res = reddit.process_text("di&#x200B;dn&#39;t")
    assert res == "didn't"


def test_post_to_dict(mocker: MockFixture) -> None:
    """The reddit.post_to_dict function suceeds and has the required keys."""
    post = mocker.MagicMock()

    comment_a = mocker.MagicMock()
    type(comment_a).body = "lorem ipsum"
    type(comment_a).is_root = True
    # this comment should be skipped because it is non root
    comment_b = mocker.MagicMock()
    type(comment_b).is_root = False
    type(comment_b).body = "lorem ipsum"
    post.comments.__iter__.return_value = [comment_b, comment_a, comment_a]

    res = reddit.post_to_dict(post, include_children=False, limit=1)

    for k in ["id", "title", "author", "url", "votes", "comments"]:
        assert k in res

    for k in ["author", "votes", "ts", "body"]:
        assert k in res["comments"][0]


def test_post_to_dict_no_coments(mocker: MockFixture) -> None:
    """The reddit.post_to_dict function suceeds when there are no comments."""
    post = mocker.MagicMock()
    post.comments.__iter__.return_value = []

    res = reddit.post_to_dict(post)

    assert len(res["comments"]) == 0
