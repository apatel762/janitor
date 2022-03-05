from pathlib import Path

import typer

from .crawler import Crawler
from .gatherers import ForwardLinkGatherer
from .gatherers import Sha256ChecksumGatherer

app = typer.Typer(
    help="A program for performing checks on, and enhancing, markdown notes."
)


@app.command(
    short_help="Scan a given folder and create a metadata index.",
    help=(
        "Scan a folder containing Markdown notes and build a metadata "
        "index that can be operated on by Janitor via the other commands. "
        "\n"
        "\n"
        "NOTE: This operation will not recursively traverse sub-directories, "
        "so only the notes in the top-level of the given folder will be "
        "found."
    ),
)
def scan(
    folder: Path = typer.Argument(
        ...,
        help="The folder containing all of your Markdown (*.md) notes.",
        envvar="JANITOR_NOTES_FOLDER",
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,
    ),
    assume_yes: bool = typer.Option(
        False, "--assume-yes", help="Automatic 'Yes' to every prompt."
    ),
    force_index_rebuild: bool = typer.Option(
        False, "--force-index-rebuild", help="Rebuild the index entirely from scratch."
    ),
) -> None:
    typer.echo(f"Will index folder: {folder}")
    if not assume_yes:
        typer.confirm("Would you like to continue?", abort=True)
    typer.echo("Starting scan...")

    if force_index_rebuild:
        typer.echo(
            "The '--force-index-rebuild' option is not supported at the moment.",
            color=True,
        )

    # crawl the given folder and build out the index
    crawler = Crawler(crawl_dir=folder)
    crawler.gatherers.append(Sha256ChecksumGatherer())
    crawler.gatherers.append(ForwardLinkGatherer())
    crawler.go()

    typer.Exit()


@app.command()
def apply() -> None:
    typer.Exit()


@app.command()
def toolbox() -> None:
    typer.Exit()


def main() -> None:
    app()


if __name__ == "__main__":
    main()
