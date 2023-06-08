from datetime import datetime
from itertools import chain

from ..tex import *
from ..u2tex import u2tex


class Article:
    provides = ["article"]

    def __init__(self, meta, recipe, args):
        self.cls = args.cls
        self.cname = args.cname
        self.bibstyle = args.bibstyle
        self.anonymous = args.anonymous
        self.opts = args.opts
        self.include = args.include
        self.recipe = recipe
        self.__dict__.update(meta)

        self.headers = [self.render_comment, self.render_documentclass]
        self.footers = [self.render_bib, self.end_document]

        self.setup()

    def setup(self):
        if self.cname is None:
            self.cname = "article"

        if self.bibstyle is None:
            self.bibstyle = "plainurl"

        self.headers += [
            self.render_encs,
            self.macro,
            self.render_title,
            self.render_authors,
            self.begin_document,
            self.maketitle,
            self.render_abstract,
            self.render_keywords,
        ]

        if "noheader" in self.opts:
            self.opts.remove("noheader")
        else:
            self.headers.insert(3, self.extra_header)

        self.footers.insert(0, self.render_acknowledgements)

    def authors_list(self, short=False):
        def name(author):
            return short_name(author["name"]) if short else author["name"]

        names = map(name, self.authors)
        return join_and(names)

    def render_comment(self):
        COMMENT = (
            "% Generated by <https://github.com/jakub-oprsal/thead> "
            "on {now}\n%\n% {title}\n% by {authors}\n%\n"
        )
        return COMMENT.format(
            now=datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            title=self.title.upper(),
            authors=self.authors_list(short=True),
        )

    def render_documentclass(self):
        return render_command("documentclass", self.cname, ",".join(self.opts))

    def maketitle(self):
        return "\\maketitle\n"

    def begin_document(self):
        return render_command("begin", "document")

    def end_document(self):
        return render_command("end", "document")

    def macro(self):
        _include = lambda fn: include(fn, end="", soft=not self.include)
        return "".join(map(_include, self.recipe.header))

    def extra_header(self):
        header = render_command(
            "usepackage",
            "hyperref",
            "colorlinks, citecolor=blue, linkcolor=blue, urlcolor=red",
        )
        header += render_command("urlstyle", "same")
        header += render_command("usepackage", "amsmath, amssymb, amsthm")
        header += (
            "\\newtheorem{theorem}{Theorem}[section]\n"
            "\\newtheorem{lemma}[theorem]{Lemma}\n"
            "\\newtheorem{proposition}[theorem]{Proposition}\n"
            "\\newtheorem{corollary}[theorem]{Corollary}\n"
            "\\newtheorem{conjecture}[theorem]{Conjecture}\n"
            "\\newtheorem{claim}[theorem]{Claim}\n"
            "\\theoremstyle{definition}\n"
            "\\newtheorem{definition}[theorem]{Definition}\n"
            "\\newtheorem{example}[theorem]{Example}\n"
            "\\newtheorem{remark}[theorem]{Remark}\n"
        )
        header += (
            "\\providecommand{\keywords}[1]"
            "{\\textbf{\\textit{Keywords---}} #1}\n"
        )
        return header

    def render_encs(self):
        return render_command(
            "usepackage", "inputenc", "utf8"
        ) + render_command("usepackage", "fontenc", "T1")

    def funding_note(self):
        try:
            return "\n".join(
                grant["note"] for grant in self.funding if "note" in grant
            )
        except AttributeError:
            return None

    def render_title(self):
        title = u2tex(self.title)
        if hasattr(self, "funding") and not self.anonymous:
            title += "%\n" + render_command(
                "thanks", self.funding_note(), end="%\n"
            )
        return render_command("title", title)

    def render_address(self, addr):
        out = []
        if "department" in addr:
            out.append(addr["department"])
        if "institution" in addr:
            out.append(addr["institution"])
            if "city" in addr and addr["city"] not in addr["institution"]:
                out.append(addr["city"])
        elif "city" in addr:
            out.append(addr["city"])
        if "country" in addr:
            out.append(addr["country"])
        return ", ".join(out)

    def render_author(self, author):
        author_lns = [u2tex(author["name"])]
        if "affiliation" in author:
            author_lns.append(self.render_address(author["affiliation"]))
        if "email" in author:
            author_lns.append(
                "({})".format(
                    render_command("texttt", author["email"]).strip()
                )
            )
        return "\\\\\n".join(author_lns)

    def render_authors(self):
        if not self.anonymous:
            return render_command(
                "author",
                "\\and\n".join(
                    self.render_author(author) for author in self.authors
                ),
            )
        else:
            return render_command("author", "Anonymous Author(s)")

    def render_abstract(self):
        try:
            return render_env("abstract", self.abstract.strip())
        except AttributeError:
            return None

    def render_keywords(self):
        try:
            return render_command("keywords", ", ".join(self.keywords))
        except AttributeError:
            return None

    def render_acknowledgements(self):
        if not self.anonymous:
            try:
                return (
                    r"\subsection*{Acknowledgements}"
                    + "\n\n"
                    + self.acknowledgements.strip()
                    + "\n"
                )
            except AttributeError:
                pass
        return None

    def render_bib(self):
        if self.recipe.bib:
            return render_command(
                "bibliographystyle", self.bibstyle
            ) + render_command("bibliography", ",".join(self.recipe.bib))
        else:
            return "% no bibliography information\n"

    def header(self):
        headers = (f() for f in self.headers if f() is not None)
        return "\n".join(headers) + "\n"

    def body(self):
        _include = lambda fn: include(fn, end="\n", soft=not self.include)
        content = map(_include, self.recipe.content)
        if self.recipe.appendix:
            appendix = chain(
                ("\n\\appendix\n",), map(_include, self.recipe.appendix)
            )
        else:
            appendix = ()
        return chain(content, appendix)

    def footer(self):
        footers = (f() for f in self.footers if f() is not None)
        return "\n".join(footers)

    def dump(self):
        yield self.header()
        yield from self.body()
        yield self.footer()
