"""CLI entry point for Questionable AI.

Provides the ``questionable-ai`` command with subcommands for running
multi-model debates, replaying transcripts, and managing configuration.
"""

import click

from questionable_ai import __version__


@click.group()
@click.version_option(version=__version__, prog_name="questionable-ai")
def main() -> None:
    """Cross-vendor multi-model debate and consensus engine.

    Sends a query to multiple AI models, shares competing responses back
    for reflection and critique, then synthesizes a final answer through
    a user-selected model.
    """


@main.command()
@click.argument("query")
@click.option("--panel", default=None, help="Comma-separated model aliases (e.g. claude,gpt).")
@click.option("--synthesizer", default=None, help="Model alias for final synthesis.")
@click.option("--rounds", default=1, type=click.IntRange(1, 3), help="Reflection rounds (1-3).")
def ask(query: str, panel: str | None, synthesizer: str | None, rounds: int) -> None:
    """Send a query to the debate panel.

    Fans out QUERY to all panel models, runs reflection rounds, and
    synthesizes a final answer.

    Args:
        query: The question or prompt to debate.
        panel: Comma-separated model aliases to use as panelists.
        synthesizer: Model alias for final synthesis.
        rounds: Number of reflection rounds.
    """
    click.echo(f"Query: {query}")
    click.echo(f"Panel: {panel or 'default'}")
    click.echo(f"Synthesizer: {synthesizer or 'auto'}")
    click.echo(f"Rounds: {rounds}")
    click.echo("\n[Not yet implemented — Phase 1 in progress]")


if __name__ == "__main__":
    main()
