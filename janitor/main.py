import time

import typer

app = typer.Typer()


@app.command()
def scan(verbose: bool = False):
    if verbose:
        typer.echo("I am the janitor and I am about to look around for stuff to do")
    typer.echo("I am done scanning for stuff to do")


@app.command()
def apply():
    scan()
    typer.echo(
        "I am now doing things according to the information I got while scanning!"
    )


@app.command()
def toolbox():
    typer.echo("I am about to progress a lot of stuff!")
    total = 0
    with typer.progressbar(range(1000)) as progress:
        for value in progress:
            # Fake processing time
            time.sleep(0.01)
            total += 1
    typer.echo(f"Processed {total} things.")


def main():
    app()


if __name__ == "__main__":
    main()
