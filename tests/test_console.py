"""Console test suite."""
from click.testing import CliRunner
import pytest

from vidgen import console


@pytest.fixture
def runner() -> CliRunner:
    """Generate a click CLI runner."""
    return CliRunner()


def test_main_succeeds(runner: CliRunner) -> None:
    """Main exits with a code of zero (sucess)."""
    result = runner.invoke(console.main)
    assert result.exit_code == 0
