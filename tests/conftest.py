"""Global test configuration and shared fixtures."""
from typing import Callable

import pytest


@pytest.fixture
def check_post_dict() -> Callable[[dict], None]:
    """Check if a dictionary returned by reddit.post_to_dict is valid."""

    def assert_valid_post_dict(post: dict) -> None:
        for k in ["id", "title", "author", "url", "votes", "comments"]:
            assert k in post

        for k in ["author", "votes", "ts", "body"]:
            assert k in post["comments"][0]

    return assert_valid_post_dict
