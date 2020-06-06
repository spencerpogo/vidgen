"""Reddit downloader client."""
import html

import praw


ZERO_WIDTH_SPACE = html.unescape("&#x200B;")


def process_text(text: str) -> str:
    """Processes text into human readable format.

    Escapes all html entities and strips zero-width spaces.

    Args:
        text: The text to be processed

    Returns:
        The processed text.
    """
    text = html.unescape(text)
    return text.replace(ZERO_WIDTH_SPACE, "")


def post_to_dict(
    post: praw.models.Submission, include_children: bool = False, limit: int = None
) -> dict:
    """Processes the top level comments of a reddit post into a json object.

    Gets all of the comments of the post,

    Args:
        post: The reddit post to get comments from
        include_children: Whether to include non top-level comments
        limit: The maximum amount of comments to return

    Returns:
        A dictionary with the post id, title, and a list of processed comment
        dictionaries with author, votes, ts, and body fields.
    """
    # Download all comments
    post.comments.replace_more(limit=0)
    data = {
        "id": post.id,
        "title": post.title,
        "author": post.author.name,
        "url": post.url,
        "votes": post.score,
        "comments": [],
    }

    for comment in post.comments:
        print("c")
        if limit is not None and len(data["comments"]) >= limit:
            break

        if not include_children and not comment.is_root:
            continue

        text = process_text(comment.body)
        data["comments"].append(
            {
                "author": comment.author.name,
                "votes": comment.score,
                "ts": comment.created_utc,
                "body": text,
            }
        )

    return data
