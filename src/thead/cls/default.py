'''
New approach to classes and class handling
'''
import textwrap
from datetime import datetime
from .ccs import CCS
from .tex import *


COMMENT = '''% Generated by <https://github.com/jakub-oprsal/thead> on {now}
%
% {title}
% by {authors}
%'''


class Article:
    provides = []

    def __init__(self, meta, **kwargs):
        self.cname = kwargs.get('cname', None)
        self.anonymous = kwargs.get('anonymous', False)
        self.opts = kwargs.get('classoptions', [])
        self.include = kwargs.get('include', [])
        self.bib = kwargs.get('bib', [])
        self.__dict__.update(meta)
        
        self.headers = [self.render_comment]
        self.footers = [self.render_bib, self.end_document]

    def authors_list(self, short=False):
        def name(author):
            return short_name(author['name']) if short else author['name']
        names = map(name, self.authors)
        return join_and(names)

    def render_comment(self):
        return COMMENT.format(now = datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
            title = self.title.upper(),
            authors = self.authors_list(short=True))

    def render_documentclass(self):
        return render_command(
                'documentclass',
                self.cname,
                ','.join(self.opts))

    def maketitle(self):
        return '\\maketitle\n'

    def begin_document(self):
        return render_command('begin', 'document')

    def end_document(self):
        return render_command('end', 'document')

    def includes(self):
        return ''.join((include(file) for file in self.include))

    def render_encs(self):
        return render_command('usepackage', 'inputenc', 'utf8') + \
               render_command('usepackage', 'fontenc', 'T1')

    def render_title(self):
        return render_command('title', self.title)

    def render_authors(self):
        return '\n'.join(map(self.render_author, self.authors))

    def render_abstract(self):
        try:
            return render_env('abstract', self.abstract.strip())
        except AttributeError:
            return None

    def render_keywords(self):
        try:
            return render_command('keywords', ", ".join(self.keywords))
        except AttributeError:
            return None

    def render_ccs2012(self):
        try:
            return CCS(self.ccs2012['concepts']).render()
        except AttributeError:
            return None

    def render_funding(self, command='thanks'):
        try:
            funding_note = '\n'.join(grant['note']
                    for grant in self.funding
                    if 'note' in grant)
            return render_command(command, funding_note)
        except AttributeError:
            return None

    def render_bib(self):
        if self.bib:
            return render_command('bibliographystyle', self.bibstyle) + \
                render_command('bibliography', ','.join(self.bib))
        else:
            return '% no bibliography information\n'

    def header(self):
        headers = (f() for f in self.headers if f() is not None)
        return '\n'.join(headers)

    def footer(self):
        footers = (f() for f in self.footers if f() is not None)
        return '\n'.join(footers)
