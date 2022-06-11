import os
from pathlib import Path

import typer

from .crawler import Crawler
from .gatherers import BacklinkGatherer
from .gatherers import ForwardLinkGatherer
from .gatherers import ModifiedTimeGatherer
from .gatherers import NoteTitleGatherer
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
        typer.echo("The '--force-index-rebuild' option is not supported at the moment.")
        raise typer.Exit(code=1)

    # crawl the given folder and build out the index
    crawler = Crawler(crawl_dir=folder)
    crawler.gatherers.append(Sha256ChecksumGatherer())
    crawler.gatherers.append(ForwardLinkGatherer())
    crawler.gatherers.append(BacklinkGatherer())
    crawler.gatherers.append(ModifiedTimeGatherer())
    crawler.gatherers.append(NoteTitleGatherer())
    crawler.go()

    raise typer.Exit()


@app.command(
    short_help="Convert your notes to HTML.",
    help=(
        "Convert the notes in a scanned folder to HTML files. A custom stylesheet will be applied to the notes "
        "automatically."
    ),
)
def publish(
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
    destination: Path = typer.Argument(
        Path(os.path.expanduser("~/Documents/Notes/.publish")),
        help="The folder that your published notes will be saved to.",
        envvar="JANITOR_DESTINATION_FOLDER",
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,
    ),
) -> None:
    # 0) download https://raw.githubusercontent.com/hawkz/gdcss/master/gd.css if not present
    #      to destination/css/main.css
    # 0) offer to do scan if cannot find index?
    #      put --assume-yes back if this gets implemented
    # 1) read the index
    # 2) if file was modified since last script runtime, queue it for publishing
    # 3) do pandoc conversion (use pandoc.write https://boisgera.github.io/pandoc/api/#pandoc)
    #      command:
    #        pandoc
    #        filename.md
    #        --metadata=author:getpass.getuser()
    #        --metadata=lang:en-GB
    #        --metadata=charset:utf-8
    #        --metadata=pagetitle:(get the page title somehow)
    #        --no-highlight
    #        --css=css/main.css
    #        --from=markdown
    #        --to=html
    #        --id-prefix=(create some sort of footnote id prefix using file name)
    #        --output=filename.html
    # TODO: re-implement filters from old static site generator?
    # TODO: figure out how to customise favicon
    # 4) generate and publish an index file (if not present in notes)
    raise typer.Exit()


@app.command()
def apply() -> None:
    raise typer.Exit()


@app.command()
def toolbox() -> None:
    raise typer.Exit()


def main() -> None:
    app()


if __name__ == "__main__":
    main()
