"""Tests for the ``augments`` root command group."""

from __future__ import annotations

import subprocess
import sys

from click.testing import CliRunner

from augments.adk import __version__
from augments.adk.cli import main


def test_help_exits_zero() -> None:
    result = CliRunner().invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "augments" in result.output


def test_version_prints_package_version() -> None:
    result = CliRunner().invoke(main, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.output


def test_python_dash_m_entry_point() -> None:
    proc = subprocess.run(
        [sys.executable, "-m", "augments.adk.cli", "--help"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0
    assert "augments" in proc.stdout
