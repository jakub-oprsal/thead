from .article import Article
from ..tex import render_command


class AMSart(Article):
    provides = ["amsart"]

    def setup(self):
        if self.cname is None:
            self.cname = "amsart"

        if self.bibstyle is None:
            self.bibstyle = "amsalpha"

        if "noheader" in self.opts:
            self.opts.remove("noheader")
        else:
            self.headers += [self.render_encs, self.extra_header]

        self.headers += [
            self.macro,
            self.render_pdfmeta,
            self.begin_document,
            self.render_title,
            self.render_authors,
            self.render_funding,
            self.render_abstract,
            self.render_keywords,
            self.maketitle,
        ]

        self.footers.insert(0, self.render_acknowledgements)

    def extra_header(self):
        header = render_command(
            "usepackage",
            "hyperref",
            "colorlinks, citecolor=blue, linkcolor=black, urlcolor=red",
        )
        header += render_command("urlstyle", "same")
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
        return header

    def render_pdfmeta(self):
        if not self.anonymous:
            authors = self.authors_list(short=True)
        else:
            authors = "Anonymous Author(s)"
        return (
            "\\hypersetup{%\n"
            f"  pdftitle  = {{{self.title}}},\n"
            f"  pdfauthor = {{{authors}}}}}\n"
        )

    def render_title(self):
        shorttitle = self.__dict__.get("shorttitle", "")
        return render_command("title", self.title, shorttitle)

    def render_author(self, author):
        out = render_command("author", author["name"])
        if "affiliation" in author:
            out += render_command(
                "address",
                ", ".join(
                    str(value) for _, value in author["affiliation"].items()
                ),
            )
        if "email" in author:
            out += render_command("email", author["email"])
        return out

    def render_authors(self):
        if not self.anonymous:
            return "\n".join(map(self.render_author, self.authors))
        else:
            return render_command("author", "Anonymous Author(s)")

    def render_funding(self):
        if self.anonymous:
            return None

        try:
            note = self.note
        except AttributeError:
            note = None

        funding = self.funding_note()
        if funding is not None:
            if note is not None:
                note += "\\\\\n\\indent " + funding
            else:
                note = funding

        if not note:
            return None
        else:
            return render_command("thanks", note)
