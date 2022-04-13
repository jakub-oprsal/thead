# Tools for generating LaTeX files from metadata

This package generates LaTeX headers from a yaml metadata file. The intended use is to ease preparation of submissions to various (mostly math and tcs) conferences and journals. It is still very much work in progress, and I am personally actively using it, so it can change at moments notice.

Currently supported LaTeX classes are: **acmart**, **lipics**, and **amsart**.

## The problem and philosophy

LaTeX, however wonderful and world changing system it is, has its own troubles. Some of come as historical baggage, some of them come form lack of standardisation among LaTeX developers. In my eyes, the key issues are:

- *Lack of standardisation of headers.*  Often, one has to rewrite the whole headers of a file when changing the class of a document. Arguably, TeX/LaTeX was never intended to be used in such a way, but it has become necessary in the current academic workflow when a paper is first published in arXiv, then at a conference, and finally, in a journal. While the content of the paper does not change too much, the class usually changes with any new submission.

- *Imperfect separation of typesetting instructions from content.*  This comes from the heritage. TeX was written as a typesetting program. It is therefore not a document preparation tool, it has never had a gui for that reason, and the original TeX macros are not very flexible when one would like to change the style of the document. This was somewhat addressed by LaTeX, which took advantage of the strong language that came with TeX, and aimed to provide a more human-readable structure. But LaTeX's solutions is imperfect: all the typesetting information is still contained in the same file as the content of the document, and users are usually tempted to hack their typesetting when creating content which results in clumsy source files that do not compile with just minor changes.

- *Outdated compiling routine.*  Again, this comes from the heritage. TeX was written to run reasonably efficiently on machines that we now consider ancient. It is able to compile a book on a processor which was weaker that what you can find these days in clocks in a single pass! One implication of that is that back-references are not easily done in TeX/LaTeX, and documents these days require at least 2–3 passes to compile when that is completely unnecessary, and one pass would be enough if the TeX source was well enough prepared.

This package is addressing the first two issues with the hope of being extendible to deal with the final issue as well. My goal is separation of the input into three bits: *metadata*, *content*, and *typesetting instructions*. Only the language for typesetting instructions needs to be powerful.

From a practical standpoint, I believe that people have a general understanding of what separates metadata and content from typesetting instructions – generally, if you can imagine your document would be prepared for a different medium, the things that do not change are content and metadata. The separation between metadata and content is a bit trickier — for example, is abstract part of metadata or content? The rule of thumb that I am using for this separation is that whatever would appear on a journal webpage together with a link to download a pdf is metadata, e.g., title, authors, funding information, math/cs classification, but also abstract and list of references. Metadata is also what you input to various forms when you submit a paper. In the ideal word, we would have a unified format for metadata, so that submission would really be just uploading a metadata file, and (say) LaTeX source of the pdf.

Again, to reiterate, the purpose of this package is **separate metadata from content and typesetting instructions**.


## Installation and usage

This is a python package that can be either install through pip git interface, i.e., by running
```
python3 -m pip install git+https://github.com/jakub-oprsal/thead
```
or by downloading and installing by running `python3 -m setup build` and `python3 -m setup install`.

Everything is work in progress. I will soon provide an example metadata file. To get help on invocation, run `python3 -m thead -h`.
