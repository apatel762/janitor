# janitor

A program for performing checks on, and enhancing, my markdown notes.

The name of the project ('janitor') is inspired by the ['note-link-janitor'](https://github.com/andymatuschak/note-link-janitor) by Andy Matuschak. I'm using this repo to maintain my own version of his scripts because I want to support regular Markdown links (instead of Wikilinks) and I want to have the 'janitor' to extra checks like looking for dead links.

## Requirements

- You must have `pandoc` installed on your machine.
- Python ^3.9

## Doco

Quick links to doco (TODO: clean this up later)

- <https://boisgera.github.io/pandoc/api/#pandoc> - Pandoc-to-Python API
- <https://hackage.haskell.org/package/pandoc-types> - click on `Text.Pandoc.Definition` (official Pandoc types doc)

## Roadmap

These are the features that I want the Janitor to have before I can call it 'ready'.

- `janitor scan` - basically done
- `janitor apply`
  - Might need to think of a better name for this, but that's not important because it's easy to change.
  - Maintains backlink structure among interlinked Markdown notes.
    - Extend in future to detect broken links & orphan notes?
  - This option will make it clear that it is about to modify your notes and will ask if you want to back them up.
    - Could use a script arg to bypass this
  - This option will ask you *y/N* (the same way that `nb` does) before continuing. <https://typer.tiangolo.com/tutorial/prompt/#confirm-or-abort>.
  - **Execution**
    - The execution stage will read the index into memory and do things to the notes based on the data that we've gathered.
    - This would involve the usage of **Hooks**, where each hook is applied to a notes while it's being processed.
    - Every hook is applied sequentially to a note to fully process that note before moving to the next.
    - Using hooks will allow for extensibility later on because I'm not sure how many operations I will need to perform on my notes (it will depend on how much stuff I want to do to the notes in the first place).
    - Might be worth introducing the concept of a **Hook Manager** into which hooks can be added. The hook manager itself would be iterable, so that it could fit into the proposed structure above.
- `janitor config`
  - **This whole sub-command is a big 'maybe' from me, don't know how useful it'll *really* be**
  - Use this to manage a config file that controls the behaviour of the rest of the script.
  - If you have a config file, it'll be used so that you can avoid having to pass script args every time you use the janitor.
- `janitor toolbox`
  - This is where I will put various sub-commands.
  - The sub-commands will mimic the stuff that I already do with my custom `nv` script (if possible):
    - Save a URL
    - Create a citation
    - Create files based on date using natural language
    - Open Wayback Machine version of URL in browser <https://typer.tiangolo.com/tutorial/launch/>
  - Any time we are generating text, it should be copied to the clipboard (<https://pypi.org/project/pyperclip/>)
  - Is it possible to call `nb` from Python? If so we could potentially replace my `notes.sh` script with a toolbox subcommand.
  - <https://typer.tiangolo.com/tutorial/subcommands/add-typer/>

## Misc. requirements

All long-running stuff will use a progress bar: <https://typer.tiangolo.com/tutorial/progressbar/>

All scripts should use colour to signal good and bad results: <https://typer.tiangolo.com/tutorial/printing/>

All user-facing parts of the CLI are fully documented: <https://typer.tiangolo.com/tutorial/arguments/help/>

An `nb` plugin should be included somewhere in this repo.

Scripts support using env vars instead of params: <https://typer.tiangolo.com/tutorial/arguments/envvar/>
