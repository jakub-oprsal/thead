# Tools for generating LaTeX files from metadata

This package generates LaTeX headers from a yaml metadata file. The intended use is to ease preparation of submissions to various (mostly math and tcs) conferences and journals. It is still very much work in progress, and I am personally actively using it, so it can change at moments notice.

Currently supported LaTeX classes are: **acmart**, **lipics**, **siamart**, and **amsart**.


## The problem and philosophy

LaTeX, however wonderful and world changing system it is, has its own troubles. Some of come as historical baggage, some of them come form lack of standardisation among LaTeX developers. In my eyes, the key issues are:

1. *Lack of standardisation of headers.*  Often, one has to rewrite the whole headers of a file when changing the class of a document. Arguably, TeX/LaTeX was never intended to be used in such a way, but it has become necessary in the current academic workflow when a paper is first published in arXiv, then at a conference, and finally, in a journal. While the content of the paper does not change too much, the class usually changes with any new submission.

2. *Imperfect separation of typesetting instructions from content.*  This comes from the heritage. TeX was written as a typesetting program. It is therefore not a document preparation tool, it has never had a gui for that reason, and the original TeX macros are not very flexible when one would like to change the style of the document. This was somewhat addressed by LaTeX, which took advantage of the strong language that came with TeX, and aimed to provide a more human-readable structure. But LaTeX's solutions is imperfect: all the typesetting information is still contained in the same file as the content of the document, and users are usually tempted to hack their typesetting when creating content which results in clumsy source files that do not compile with just minor changes.

3. *Outdated compiling routine.*  Again, this comes from the heritage. TeX was written to run reasonably efficiently on machines that we now consider ancient. It is able to compile a book on a processor which was weaker that what you can find these days in clocks in a single pass! One implication of that is that back-references are not easily done in TeX/LaTeX, and documents these days require at least 2–3 passes to compile when that is completely unnecessary, and one pass would be enough if the TeX source was well enough prepared.

This package is addressing the first issue, and partially the second issue. It is the first step towards the system that could deal with all three of the above.

The solution to problem 2 would be a separation of the input into three bits: *metadata*, *content*, and *typesetting instructions*. Naturally, all three of these require different approach. The metadata, which are dealt with in this package, would ideally be presented in easily transferable open format. For now, I have choosen `yaml` since it is easy to write, and there are enough packages that can process it.

From a practical standpoint, I believe that people have a general understanding of what separates metadata and content from typesetting instructions – generally, if you can imagine your document would be prepared for a different medium, the things that do not change are content and metadata. The separation between metadata and content is a bit trickier — for example, is abstract part of metadata or content? The rule of thumb that I am using for this separation is that whatever would appear on a journal webpage together with a link to download a pdf is metadata, e.g., title, authors, funding information, math/cs classification, but also abstract and list of references. Metadata is also what you input into various forms when you submit a paper. In the ideal word, we would have a unified format for metadata, so that submission would really be just uploading a metadata file, and a LaTeX source, or a pdf.

Again, to reiterate, the purpose of this package is **separate metadata from content and typesetting instructions**, and adapt to non-standardised LaTeX headers.


## Installation

You need a functioning Python 3 environment which is present on most current UNIX systems.  Then this package that can be installed by pip git interface, i.e., by running
```
python3 -m pip install git+https://github.com/jakub-oprsal/thead
```

Eventually, I might upload it to PyPI if there is enough interest —so please let me know if you find this package useful!


## Usage

Currently, the project is very much work in progress, so is provided without any guarantees for stability accross versions. It is nevertheless a workable prototype that I am actively using, and adapting for my use. This in particular means that the number of formats will slowly increase as I prepare papers for submissions to different venues.


### Structure of the metadata file and invocation

Let me put in a simple example of a metadata file based on Alan Turing's seminal paper. Say, this is stored in the file `computablenumbers.yaml`
```yaml
title: On Computable Numbers, with an Application to the Entscheidungsproblem
authors:
  - name: Alan M. Turing
    affiliation:
      department: The Graduate College
      institution: Princeton University 
      city: New Jersey
      country: U.S.A.

abstract: |
  The ``computable'' numbers may be described briefly as the real numbers whose
  expressions as a decimal are calculable by finite means. Although the subject
  of this paper is ostensibly the computable numbers, it is almost equally easy
  to define and investigate computable functions of an integral variable or a
  real or computable variable, computable predicates, and so forth. [...]
```

Now, assume that Dr Turing would like to submit this article to Journal of the ACM. To use the acmart style, he would run:
```
thead -c acmart computablenumbers.yaml
```
This then produces a file `computablenumbers.tex` that serves as a base of latex document. *thead* is trying to guess which files in the current directory substite the content of the document, and additional sources:

- the content is assumed to be included in `content.tex`, or in several separate files following, e.g., this naming convention:
```
1_computing_machines.tex
2_definitions.tex
...
11_application_to_the_Entscheidungsproblem.tex
appendix.tex
```

- *thead* also discovers all `*.bib` files in the current directory, and includes them in the bibliography command.

- additional tex macros to be included in the header are assumed to be in the file `macro.tex`.

All of this behaviour can be altered with different options. Naturally, he could also try to run
```
thead -c lipics computablenumbers.yaml
```
to produce a file for submission to a conference using a lipics style. But this command will fail, since he would need to include more necessary metadata, e.g.,
```yaml
keywords:
  - Entscheidungsproblem
  - computable numbers
```
He would be also kindly asked by the resulting pdf to include some ccs2012 classification:
```yaml
ccs2012:
  concepts:
    - id: 10003752.10003753.10010622
      desc: Theory of computation~Abstract machines
      significance: 500
```
I think now, you are getting to understand a bit how the system works, and that publishing in this time is considerably more annoying than in 1936.

More details on the possible options can viewed by running `thead -h`, and example(s) are included in the examples folder of this repository.


## References

The example is constructed from Alan Turing's paper appearing at Proc. of the LMS.

A.M. Turing, *On Computable Numbers, with an Application to the Entscheidungsproblem*, Proc. of the London Math. Soc., Volumes 2–42, Issue 1, 1937, Pages 230–265. [doi:10.1112/plms/s2-42.1.230](https://doi.org/10.1112/plms/s2-42.1.230)
