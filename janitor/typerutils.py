import typer


def warn(message: str) -> str:
    """
    Formats a given message as a warning by prepending a yellow string to the
    beginning that says 'WARN'.

    :param message: The message that you want to format as a warning.
    :return: The given message, with a yellow warning string at the beginning.
    """
    if type(message) is not str:
        raise TypeError(
            "Cannot create warning message for type: " + repr(type(message))
        )

    if len(message) == 0:
        raise RuntimeError("Cannot create warning message for empty string.")

    return typer.style("WARN", fg=typer.colors.YELLOW, bold=True) + ": " + message


def error(message: str) -> str:
    """
    Same as WARN except with a red string that says ERROR at the beginning

    :param message: The message that you want to format as a warning.
    :return: The given message, with a red ERROR string at the beginning.
    """
    if type(message) is not str:
        raise TypeError(
            "Cannot create warning message for type: " + repr(type(message))
        )

    if len(message) == 0:
        raise RuntimeError("Cannot create warning message for empty string.")

    return typer.style("ERROR", fg=typer.colors.RED, bold=True) + ": " + message
