from .article import Article
from ..tex import render_command


class AMSart(Article):
    provides = ["amsart"]
    cname_ = "amsart"
    bibstyle_ = "amsalpha"

    def setup(self):
        self.TeXauthors = self.render_authors()
        self.TeXtitle = self.render_title()
        self.thanks = self.funding_note()
        self.abstract = self.abstract.strip()

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
