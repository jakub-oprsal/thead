# tmarko

A hack of [marko] markdown parser to produce LaTeX files.

My intention was to create a parser that would not produce a complete document, but rather bits of LaTeX code which could be used in a bigger LaTeX document, or together with another tool that creates headers of the file, e.g., my [thead] package.


## Usage

This is a simple tool that gets a filename as parameter and outputs the content. So you can run, e.g.,
```
  python3 -m tmarko section.md > section.tex
```
To produce `section.tex` from `section.md`. If you know some Python, it's probably easy to hack to do whatever you'd like.


## Extended markdown syntax

I have added a few new elements to make writing scientific (math, or theoretical computer science) papers easier.

### Inline and display math

The parser recognises `$...$` and `\[...\]` as inline and display math, respectively. No other math delimiters are recognised, and display math has to be formated with the delimiters on separate lines, i.e., as
```latex
\[
  ...
\]
```
The main point of these is that the content is not processed as markdown, and hence special TeX characters can be unescaped, and don't cause weird behaviour. Display math environments can be added as
```latex
\[{align*}
  ...
\]
```
to produce
```latex
\begin{align*}
  ...
\end{align*}
```


### Theorem environments

Theorems, lemmas, propositions, corollaries, claims, proofs, definitions, examples, remarks, notes, and conjectures can be input simply as
```
Theorem.
  There are infinitely many primes.
```
Note the indentation of the second line.


### Labels, references, citations, and minor hacks

Labels and references to these labels are input as `{#...}` and `{@...}`. For example, we could give the above theorem a name, to refer later, e.g.,
```
Theorem. {#thm:primes}
  There are infinitely many primes.

As per Theorem {@thm:primes} they are enough primes for us to do this.
```

Citations are included with `[@...]`, e.g., `[@Kar72]` will produce `\cite{Kar72}`, and `[@Kar72, Theorem 3]` will produce `\cite[Theorem 3]{Kar72}`.

Finally, I added few hacks to improve typography. First, LaTeX is not escaped, so you can use LaTeX macros in plain text as long as they are not a valid markdown. Markdown emphasis `*...*` is now rendered as `\emph{...}`, and matching apostrophes are replaced by \`...' and \`\`...''.


[marko]: https://github.com/frostming/marko
[thead]: https://github.com/jakub-oprsal/thead
