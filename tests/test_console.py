from click.testing import CliRunner
import pytest

from vidgen import console


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


def test_main_succeeds(runner: CliRunner) -> None:
    result = runner.invoke(console.main)
    assert result.exit_code == 0
