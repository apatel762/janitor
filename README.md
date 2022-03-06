# janitor

[![CodeQL](https://github.com/apatel762/janitor/actions/workflows/codeql.yml/badge.svg)](https://github.com/apatel762/janitor/actions/workflows/codeql.yml)

A program for performing checks on, and enhancing, my markdown notes.

The name of the project ('janitor') is inspired by the ['note-link-janitor'](https://github.com/andymatuschak/note-link-janitor) by Andy Matuschak. I'm using this repo to maintain my own version of his scripts because I want to support regular Markdown links (instead of Wikilinks) and I want to have the 'janitor' to extra checks like looking for dead links.

## Requirements

- You must have `pandoc` installed on your machine.
- Python ^3.9

## Installation

### pipx

This method is recommended so that the dependencies of the janitor app don't conflict with your system installation of Python.

```commandline
pipx install git+https://github.com/apatel762/janitor.git
```

### pip

```commandline
python -m pip install git+https://github.com/apatel762/janitor.git
```

## Doco

Quick links to doco (TODO: clean this up later)

- <https://boisgera.github.io/pandoc/api/#pandoc> - Pandoc-to-Python API
- <https://hackage.haskell.org/package/pandoc-types> - click on `Text.Pandoc.Definition` (official Pandoc types doc)
