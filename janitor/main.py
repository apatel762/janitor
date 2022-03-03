import typer

app = typer.Typer()


@app.command()
def plan(verbose: bool = False):
    if verbose:
        typer.echo("I am the janitor")
    typer.echo("This is my plan... Nothing yet.")


@app.command()
def apply():
    plan()
    typer.echo("I am now doing things according to plan!")


def main():
    app()


if __name__ == "__main__":
    main()
