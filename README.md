# janitor

[![PyTest](https://github.com/apatel762/janitor/actions/workflows/pytest.yml/badge.svg)](https://github.com/apatel762/janitor/actions/workflows/pytest.yml) [![CodeQL](https://github.com/apatel762/janitor/actions/workflows/codeql.yml/badge.svg)](https://github.com/apatel762/janitor/actions/workflows/codeql.yml)

**WORK IN PROGRESS** (lots of bugs, don't use this)

A program for performing checks on, and enhancing, my markdown notes.

The name of the project ('janitor') is inspired by the ['note-link-janitor'](https://github.com/andymatuschak/note-link-janitor) by Andy Matuschak. I'm using this repo to maintain my own version of his scripts because I want to support regular Markdown links (instead of Wikilinks) and I want to have the 'janitor' to extra checks like looking for dead links.

## Requirements

- You must have `pandoc` installed on your machine.
- Python ^3.10

## Installation

### pipx

Using `pipx` is recommended so that the dependencies of the janitor app don't conflict with your system installation of Python.

    pipx install git+https://github.com/apatel762/janitor.git

### pip

    python -m pip install git+https://github.com/apatel762/janitor.git

## Usage

Ensure that your markdown notes are all in a single folder. This script does not support nested folders, the notes should all be present in the top-level of the folder. The notes must have the `.md` file extension, and every note must begin with an H1 header i.e. something like this `# My Header Here`.

Links must be formatted as standard markdown links, i.e. `[My Note](note1.md)`.

**Take a backup before running this script as it will modify your notes in place**. Alternatively, you could version your notes in a git repository, which would allow you to roll back if something goes wrong.

Read through the `janitor maintain` docs using the `--help` param. This is the command that will look through your notes and maintain backlinks across them.

    $ janitor maintain --help
    Usage: janitor maintain [OPTIONS] FOLDER

      This is a composite command that will run the 'scan' and 'apply' commands
      for you in one go.

    Arguments:
      FOLDER  The folder containing all of your Markdown (*.md) notes.  [env var:
              JANITOR_NOTES_FOLDER;required]

    Options:
      -y, --assume-yes     Automatic 'Yes' to every prompt.
      -f, --force-refresh  Ignore the cached index, if one exists.
      --help               Show this message and exit.

Use `janitor --help` to discover other commands and read about them.

### Example usage

There are some example notes included in this repository. Try out this command and see what happens.

    janitor maintain tests/notes

## References

- Boisgérault, Sébastien. "[API reference - Pandoc (Python)](https://boisgera.github.io/pandoc/api/)". *[Archived](https://web.archive.org/web/20220625093512/https://boisgera.github.io/pandoc/api/)*. Retrieved June 25, 2022.
- MacFarlane, John (April 2, 2022). "[pandoc-types: Types for representing a structured document](https://hackage.haskell.org/package/pandoc-types)". *[Archived](https://web.archive.org/web/20220625093701/https://hackage.haskell.org/package/pandoc-types)*. Retrieved June 25, 2022.
