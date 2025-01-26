from datetime import datetime
from itertools import chain
from importlib import resources
from Cheetah.Template import Template

from .tex import *
from .u2tex import u2tex
from . import templates


class Article:
    provides = ["article"]

    def __init__(self, meta, recipe, args):
        self.cls = args.cls
        self.cname = args.cname
        self.bibstyle = args.bibstyle
        self.anonymous = args.anonymous
        self.opts = args.opts
        self.include = args.include

        self.macro = recipe.header
        self.content = recipe.content
        self.appendix = recipe.appendix
        self.bib = recipe.bib
        self.__dict__.update(meta)

        if "keywords" not in meta:
            self.keywords = []
        if "acknowledgements" not in meta:
            self.acknowledgements = []

        if self.cname is None:
            self.cname = "article"

        if self.bibstyle is None:
            self.bibstyle = "plainurl"

        if "noheader" in self.opts:
            self.noheader = True
            self.opts.remove("noheader")
        else:
            self.noheader = False

        self.now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.plaintext_title = self.title
        self.plaintext_authors = self.authors_list(short=True)
        self.tex_authors = self.render_authors()
        self.tex_title = self.render_title()
        self.abstract = self.abstract.strip()

    def dump(self):
        tmplfile = resources.files(templates) / 'article.tmpl'
        with tmplfile.open('rt') as f:
            tmpl = f.read()
        self.template = Template(tmpl, self.__dict__)

        yield str(self.template)

    def authors_list(self, short=False):
        def name(author):
            return short_name(author["name"]) if short else author["name"]

        names = map(name, self.authors)
        return join_and(names)

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
        return title

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

    def render_email(self, email):
        return "(\\texttt{{{}}})".format(email.strip())

    def render_author(self, author):
        lines = [u2tex(author["name"])]
        if "affiliation" in author:
            lines.append(self.render_address(author["affiliation"]))
        if "email" in author:
            lines.append(self.render_email(author["email"]))
        return "\\\\\n".join(lines)

    def render_authors(self):
        if not self.anonymous:
            return "\\and\n".join(map(self.render_author, self.authors))
        else:
            return "Anonymous Author(s)"

