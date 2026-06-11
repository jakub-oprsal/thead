from datetime import datetime
from itertools import chain
from importlib import resources
from Cheetah.Template import Template

from .tex import *
from .u2tex import u2tex
from . import templates


class Article:
    provides = ["article"]
    cname_ = "article"
    bibstyle_ = "plainurl"

    def __init__(self, meta, recipe, args):
        self.cls = args.cls
        self.cname = self.cname_ if args.cname is None \
                     else args.cname
        self.bibstyle = self.bibstyle_ if args.bibstyle is None \
                        else args.bibstyle
        self.anonymous = args.anonymous
        self.opts = args.opts
        self.include = args.include
        self.noheader = args.noheader

        self.header_includes = recipe.header
        self.content = recipe.content
        self.appendix = recipe.appendix
        self.bib = recipe.bib

        self.__dict__.update(meta)
        if "keywords" not in meta:
            self.keywords = []
        if "acknowledgements" not in meta:
            self.acknowledgements = []

        self.now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.u8authors = self.author_list(short=True)
        self.setup()

    def setup(self):
        self.TeXauthors = self.render_authors()
        self.TeXtitle = u2tex(self.title)
        self.thanks = self.funding_note()
        self.abstract = self.abstract.strip()


    def dump(self, outfile):
        tmplfile = resources.files(templates) / 'article.tmpl'
        with tmplfile.open('rt') as f:
            tmpl = f.read()
        self.template = Template(tmpl, self.__dict__)

        with codecs.open(outfile, mode="w", encoding="utf-8") as ofile:
            ofile.write(str(self.template))

    def funding_note(self):
        try:
            note='\\\\\n'.join(grant["note"]
                           for grant in self.funding
                           if "note" in grant)
            return '%\n' + r'\thanks{' + note + '}%\n'
        except AttributeError:
            return ""

    def author_list(self, short=False):
        def name(author):
            return short_name(author["name"]) if short else author["name"]

        names = map(name, self.authors)
        return join_and(names)


    def render_author(self, author):
        lines = [u2tex(author["name"])]
        try:
            lines.append(", ".join(map(lambda x: x[1],
                                       author["affiliation"].items())))
        except AttributeError:
            pass
        if "email" in author:
            lines.append(r'(\texttt{' + author["email"].strip() + '})')
        return "\\\\\n".join(lines)

    def render_authors(self):
        if not self.anonymous:
            return "\\and\n".join(map(self.render_author, self.authors))
        else:
            return "Anonymous Author(s)"

