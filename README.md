# janitor

A program for performing checks on, and enhancing, my markdown notes.

## Design

### Planning stage

A **Crawler** would walk through all of the **Notes** and store their state & metadata into an **Index**. Each note (in the index) when crawled would be scanned for forward links.

The planning stage is just for gathering data about the notes and persisting the index to disk somewhere that we can read it later.

### Execution stage

The execution stage will read the index into memory and do things to the notes based on the data that we've gathered. This would involve the usage of **Hooks**, where each hook is applied to a notes while it's being processed.

Every hook is applied sequentially to a note to fully process that note before moving to the next (pseudocode below):

```
for note in notes:
    for hook in hooks:
        hook.apply(note)
```

Using hooks will allow for extensibility later on because I'm not sure how many operations I will need to perform on my notes (it will depend on how much stuff I want to do to the notes in the first place).

Might be worth introducing the concept of a **Hook Manager** into which hooks can be added. The hook manager itself would be iterable, so that it could fit into the proposed structure above. Note: if I end up using Python - you only need to implement `__len__` and `__getitem__` to make something iterable (see [Raymond Hettinger - Beyond PEP 8](https://www.youtube.com/watch?v=wf-BqAjZb8M) @ 38:09).
