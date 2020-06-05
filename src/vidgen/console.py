"""Command line interface."""
import json

import click
import praw

from . import __version__
from .reddit import post_to_dict


@click.group()
@click.version_option(version=__version__)
def cli() -> None:
    """Vidgen is a command line tool for generating videos."""
    pass


@cli.command(short_help="Download a post from reddit")
@click.option(
    "-cid",
    "--client-id",
    required=True,
    envvar="REDDIT_CLIENT_ID",
    help="Reddit client ID (https://reddit.com/prefs/apps). "
    "Can be set with REDDIT_CLIENT_ID environment variable.",
)
@click.option(
    "-csec",
    "--client-secret",
    required=True,
    envvar="REDDIT_CLIENT_SECRET",
    help="Reddit client secret (https://reddit.com/prefs/apps). "
    "Can be set with REDDIT_CLIENT_SECRET environment variable.",
)
@click.option(
    "-ua",
    "--user-agent",
    required=True,
    envvar="REDDIT_USER_AGENT",
    help="Unique and descriptive reddit user agent."
    "Recommended format is "
    "<platform>:<app ID>:<version string> (by u/<Reddit username>)"
    "Can be set with REDDIT_CLIENT_SECRET environment variable.",
)
@click.option(
    "-cl",
    "--comment-limit",
    type=int,
    default=10,
    help="Maximum amount of comments to save",
)
@click.option("--include-children/--top-level", default=False)
@click.option("--minify-json/--pretty-json", default=False)
@click.argument("post", type=str)
@click.argument("output", type=click.types.Path(writable=True))
def redditdl(
    client_id: str,
    client_secret: str,
    user_agent: str,
    comment_limit: int,
    include_children: bool,
    minify_json: bool,
    post: str,
    output: str,
) -> None:
    """Download post data from reddit given a post id or url."""
    click.echo("Downloading post...")
    reddit = praw.Reddit(
        client_id=client_id, client_secret=client_secret, user_agent=user_agent
    )
    # assume URL if pattern contains . or /
    if "." in post or "/" in post:
        post_obj = reddit.submission(url=post)
    else:
        post_obj = reddit.submission(id=post)

    post_data = post_to_dict(
        post_obj, include_children=include_children, limit=comment_limit
    )

    with open(output, "w") as f:
        json.dump(post_data, f, indent=4 if not minify_json else None)

    click.secho(f"Wrote JSON data to {output}")
