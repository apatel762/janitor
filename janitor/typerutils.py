import typer


def warn(message: str) -> str:
    """
    Formats a given message as a warning by prepending a yellow string to the
    beginning that says 'WARN'.

    :param message: The message that you want to format as a warning.
    :return: The given message, with a yellow warning string at the beginning.
    """
    return typer.style("WARN", fg=typer.colors.YELLOW, bold=True) + ": " + message
