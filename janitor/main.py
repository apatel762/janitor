import typer

app = typer.Typer()


@app.command()
def scan(folder: str = typer.Argument(..., envvar="JANITOR_NOTES_FOLDER")):
    typer.echo(f"Will index folder: {folder}")
    typer.confirm("Would you like to continue?", abort=True)
    typer.echo("Starting scan...")
    # TODO: scan everything in the folder with a progress bar
    # TODO: put all info about notes into a file
    # TODO: how do I know that this is a valid folder?
    typer.Exit()


@app.command()
def apply():
    pass


@app.command()
def toolbox():
    pass


def main():
    app()


if __name__ == "__main__":
    main()
