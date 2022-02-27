# janitor

A program for performing checks on, and enhancing, my markdown notes.

The name of the project ('janitor') is inspired by the ['note-link-janitor'](https://github.com/andymatuschak/note-link-janitor) by Andy Matuschak. I'm using this repo to maintain my own version of his scripts because I want to support regular markdown links (instead of Wikilinks) and I want to have the 'janitor' to extra checks like looking for dead links.

## Development

You can either install the dependencies yourself or do development inside of a container (Dan Arias, 2019).

## Design

TODO: remove this section later, just writing it here as a reminder to myself.

### Programming language

The program will be written in TypeScript, because I want to learn how to use TypeScript and the original 'note-link-janitor' (that this project is inspired by) is also written in TypeScript so that it can take advantage of [syntax-tree/mdast](https://github.com/syntax-tree/mdast) for manipulating Markdown abstract syntax trees.

Might also be worth seeing if I can package the entire app as a single executable using something like Deno or [vercel/pkg](https://github.com/vercel/pkg) (Hacker News, 2019).

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

## References

- Hacker News (December 9, 2020). "[on: Deno 1.6 supports compiling TypeScript to a single executable](https://news.ycombinator.com/item?id=25366484)". *[Archived](https://web.archive.org/web/20220227123534/https://news.ycombinator.com/item?id=25366484)*. Retrieved February 27, 2022.
- Arias, Dan (February 26, 2019). "[Use Docker to Create a Node Development Environment](https://auth0.com/blog/use-docker-to-create-a-node-development-environment/)". *[Archived](https://web.archive.org/web/20220227132024/https://auth0.com/blog/use-docker-to-create-a-node-development-environment/)*. Retrieved February 27, 2022.
