"""Console test suite."""
from io import IOBase
import json
from typing import Any, Callable
from unittest.mock import Mock

from click.testing import CliRunner
import pytest
from pytest_mock import MockFixture

from vidgen import console


@pytest.fixture
def runner() -> CliRunner:
    """Generate a click CLI runner."""
    return CliRunner()


@pytest.fixture
def test_redditdl() -> Callable[
    [CliRunner, MockFixture, Callable[[dict], None], str, str], None
]:
    """Run redditdl with given arguments."""

    def test(
        runner: CliRunner,
        mocker: MockFixture,
        check_post_dict: Callable[[dict], None],
        post: str,
        output: str = "out.json",
    ) -> None:
        with runner.isolated_filesystem():
            # Make a fake reddit instance
            mock = mocker.patch("praw.Reddit")
            mock.return_value.submission.return_value.comments.__iter__.return_value = [
                mocker.MagicMock()
            ]

            # Mock objects aren't serializeable,
            #  so patch json.dump to return "asdf" for every key
            dump = json.dump
            mock_json_dump = mocker.patch("json.dump")

            def make_json_serializable(obj: Any) -> Any:
                """Make an object JSON serializable."""
                if isinstance(obj, list):
                    return [make_json_serializable(i) for i in obj]
                elif isinstance(obj, dict):
                    return {
                        make_json_serializable(k): make_json_serializable(v)
                        for k, v in obj.items()
                    }
                elif type(obj) in [str, int, float, bool]:
                    return obj
                elif isinstance(obj, Mock):
                    return "asdf"
                else:
                    raise TypeError(
                        f"Can't make object of type {type(obj).__class__} JSON "
                        "serializable"
                    )

            def fake_json_dump(obj: Any, f: IOBase, **kwargs: dict) -> None:
                return dump(make_json_serializable(obj), f, **kwargs)

            mock_json_dump.side_effect = fake_json_dump

            result = runner.invoke(
                console.cli,
                [
                    "redditdl",
                    "-cid",
                    "test",
                    "-csec",
                    "test",
                    "-ua",
                    "test",
                    post,
                    output,
                ],
            )
            print(result.output)
            assert result.exit_code == 0

            with open(output, "r") as f:
                res = json.load(f)

            check_post_dict(res)

    return test


def test_redditdl_id(
    runner: CliRunner,
    mocker: MockFixture,
    check_post_dict: Callable[[dict], None],
    test_redditdl: Callable[
        [CliRunner, MockFixture, Callable[[dict], None], str, str], None
    ],
) -> None:
    """Redditdl succeeds with a post id."""
    test_redditdl(runner, mocker, check_post_dict, "test_post_id")


def test_redditdl_url(
    runner: CliRunner,
    mocker: MockFixture,
    check_post_dict: Callable[[dict], None],
    test_redditdl: Callable[
        [CliRunner, MockFixture, Callable[[dict], None], str, str], None
    ],
) -> None:
    """Redditdl succeeds with a post url."""
    test_redditdl(runner, mocker, check_post_dict, "https://redd.it/test_post_url")
