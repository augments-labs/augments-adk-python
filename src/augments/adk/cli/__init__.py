"""Command-line interface for the Augments ADK.

The ``augments`` console script (also runnable as ``python -m
augments.adk.cli``) drives agents built with this ADK from the terminal:
running and chatting with agents declared in JSON/YAML config files or
referenced as Python objects, validating configs against the published
schemas, scaffolding new agent projects, inspecting session stores, and
serving an agent over the A2A protocol.

The CLI is a consumer of the ADK's public API only — it loads through
``load_agent`` / ``load_topology`` or a dotted
reference, executes through ``Runner``, and
persists through the session manager. Command results are written to
stdout (pipeable); diagnostics go through ``logging``. Every
cost-affecting behavior (sessions, verbose rendering, tracing, env-file
loading) is off until its flag is passed.
"""

from __future__ import annotations

import click

from augments.adk import __version__, setup_logging


@click.group(name="augments")
@click.version_option(version=__version__, prog_name="augments")
def main() -> None:
    """Augments ADK — run, chat with, validate, scaffold, and serve agents."""
    setup_logging()


# Command registrations live below the group so each command module can
# import the group's siblings (options, errors, loading) without cycles.
from augments.adk.cli.chat import chat
from augments.adk.cli.deploy import deploy
from augments.adk.cli.new import new
from augments.adk.cli.run import run
from augments.adk.cli.schema import schema
from augments.adk.cli.serve import serve
from augments.adk.cli.sessions import sessions
from augments.adk.cli.validate import validate

main.add_command(chat)
main.add_command(deploy)
main.add_command(new)
main.add_command(run)
main.add_command(schema)
main.add_command(serve)
main.add_command(sessions)
main.add_command(validate)
