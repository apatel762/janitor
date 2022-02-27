# janitor

A program for performing checks on, and enhancing, my markdown notes.

The name of the project ('janitor') is inspired by the ['note-link-janitor'](https://github.com/andymatuschak/note-link-janitor) by Andy Matuschak. I can't use his implementation directly as his only supports Wikilinks. **There is a [fork](https://github.com/sjmarshy/note-link-janitor) of the program that supports normal Markdown links**, but I'm hesitant to just use that as-is because I don't really understand what the code is doing, and I'm not confident that I could maintain it myself if I had to.

## Development

You can either install the dependencies yourself or do development inside of the container (Dan Arias, 2019).

## Design

Requirements:

- The programming language must be statically-typed.
- The end result should compile into a single executable (that requires no setup/installation to use).
- The programming language should have a well-supported library for converting CommonMark to an abstract syntax tree.

I can find things that match a couple of these requirements, but nothing that matches all three.

Golang has a library (see [here](https://github.com/yuin/goldmark)) for parsing Markdown as an abstract syntax tree. It is statically-typed and code can be trivially turned into a static binary. But the library seems really complex and doesn't seem to be usable for converting from Markdown-to-Markdown (which is what I want to do).

There are [other CommonMark parsers](https://github.com/commonmark/commonmark-spec/wiki/List-of-CommonMark-Implementations) but they all seem to be used for going from CommonMark-to-HTML directly, which isn't what I want.

I'm leaning towards using TypeScript because the original script also uses TypeScript. TypeScript programs can be compiled into a single executable using Deno 1.6+ or [vercel/pkg](https://github.com/vercel/pkg) and there is definitely a good library that can be used for manipulating Markdown ([syntax-tree/mdast](https://github.com/syntax-tree/mdast)). TypeScript is statically compiled, and of all the possible languages, it has the biggest advantage because I can use the original code as a reference.


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

Might be worth introducing the concept of a **Hook Manager** into which hooks can be added. The hook manager itself would be iterable, so that it could fit into the proposed structure above. Note: if I end up using Python - you only need to implement `__len__` and `__getitem__` to make something iterable (see [Raymond Hettinger - Beyond PEP 8](https://www.youtube.com/watch?v=wf-BqAjZb8M) @ 38:09).

## References

- Hacker News (December 9, 2020). "[on: Deno 1.6 supports compiling TypeScript to a single executable](https://news.ycombinator.com/item?id=25366484)". *[Archived](https://web.archive.org/web/20220227123534/https://news.ycombinator.com/item?id=25366484)*. Retrieved February 27, 2022.
- Arias, Dan (February 26, 2019). "[Use Docker to Create a Node Development Environment](https://auth0.com/blog/use-docker-to-create-a-node-development-environment/)". *[Archived](https://web.archive.org/web/20220227132024/https://auth0.com/blog/use-docker-to-create-a-node-development-environment/)*. Retrieved February 27, 2022.
