from itertools import chain
from .article import Article
from ..tex import render_command, render_env, join_and, include


class IEEEtran(Article):
    provides = ["IEEEtran", "ieeetran"]

    def setup(self):
        if self.cname is None:
            self.cname = "IEEEtran"

        if self.bibstyle is None:
            self.bibstyle = "IEEEtran"

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

        if self.anonymous:
            self.headers[4] = self.anon_title
            self.headers[5] = self.anon_authors

        if "noheader" in self.opts:
            self.opts.remove("noheader")
        else:
            self.headers.insert(3, self.extra_header)

        if not self.anonymous:
            self.footers.insert(0, self.render_acknowledgements)

    def anon_authors(self):
        return render_command("author", "Anonymous Author(s)")

    def anon_title(self):
        return render_command("title", self.title)

    def extra_header(self):
        header = render_command("usepackage", "amsmath, amssymb, amsthm")
        header += render_command("usepackage", "flushend")
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

    def render_author(self, author):
        if "conference" in self.opts:
            addr = author["affiliation"]
            add = []
            if "department" in addr:
                add.append(addr["department"])
            if "institution" in addr:
                add.append(addr["institution"])
            add.append(addr["city"] + ", " + addr["country"])
            add.append("Email: {}".format(author["email"]))

            return render_command(
                "IEEEauthorblockN", author["name"]
            ) + render_command("IEEEauthorblockA", "\\\\\n".join(add))
        else:
            return author["name"]

    def render_authors(self):
        if "conference" in self.opts:
            return Article.render_authors(self)
        else:
            return render_command(
                "author", join_and(map(self.render_author, self.authors))
            )

    def render_keywords(self):
        try:
            return render_env("IEEEkeywords", "; ".join(self.keywords))
        except AttributeError:
            return None

    def body(self):
        _include = lambda fn: include(fn, end="\n", soft=not self.include)
        content = map(_include, self.recipe.content)
        if self.recipe.appendix:
            appendix = chain(
                ("\n\\appendices\n",), map(_include, self.recipe.appendix)
            )
        else:
            appendix = ()
        return chain(content, appendix)

    def render_acknowledgements(self):
        if not self.anonymous:
            acks = []
            try:
                acks.append(self.acknowledgements.strip() + "\n")
            except AttributeError:
                pass
            if "conference" in self.opts and self.funding_note is not None:
                acks.append(self.funding_note())
            if acks != []:
                acks.insert(0, r"\subsection*{Acknowledgements}" "\n")
                return "\n".join(acks)
        return None
