# janitor

A program for performing checks on, and enhancing, my markdown notes.

The name of the project ('janitor') is inspired by the ['note-link-janitor'](https://github.com/andymatuschak/note-link-janitor) by Andy Matuschak. I'm using this repo to maintain my own version of his scripts because I want to support regular markdown links (instead of Wikilinks) and I want to have the 'janitor' to extra checks like looking for dead links.

## Design

TODO: remove this section later, just writing it here as a reminder to myself.

### Programming language

Will be written in Python. Installed as an executable via pipx (see <https://python-poetry.org/docs/pyproject/#scripts>).

### Planning stage

A **Crawler** would walk through all of the **Notes** and store their state & metadata into an **Index**. Each note (in the index) when crawled would be scanned for forward links.

The planning stage is just for gathering data about the notes and persisting the index to disk somewhere that we can read it later.

### Execution stage

The execution stage will read the index into memory and do things to the notes based on the data that we've gathered. This would involve the usage of **Hooks**, where each hook is applied to a notes while it's being processed.

Every hook is applied sequentially to a note to fully process that note before moving to the next (pseudocode below):

```python
for note in notes:
    for hook in hooks:
        hook.apply(note)
```

Using hooks will allow for extensibility later on because I'm not sure how many operations I will need to perform on my notes (it will depend on how much stuff I want to do to the notes in the first place).

Might be worth introducing the concept of a **Hook Manager** into which hooks can be added. The hook manager itself would be iterable, so that it could fit into the proposed structure above.
