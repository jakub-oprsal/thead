from .default import Article
from .tex import indent, render_command, render_env, include


EXTRA_HEADER = r'''\citestyle{acmauthoryear}
\setcitestyle{nosort}
\AtEndPreamble{%
    \theoremstyle{acmdefinition}
    \newtheorem{claim}{Claim}[theorem]}
'''


class ACMart(Article):
    provides = ['acmart']

    def __init__(self, meta, **kwargs):
        super(ACMart, self).__init__(meta, **kwargs)

        if self.cname is None:
            self.cname = 'acmart'

        if self.anonymous and 'anonymous' not in self.opts:
            self.opts.append('anonymous')

        self.headers = [
                self.render_comment,
                self.render_documentclass,
                self.extra_header,
                self.includes,
                self.render_title,
                self.render_authors,
                self.render_ccs2012,
                self.render_keywords,
                self.render_abstract,
                self.render_funding,
                self.begin_document,
                self.maketitle,
                ]
        
        self.footers.insert(0, self.render_acknowledgements)
        self.bibstyle = 'ACM-Reference-Format'

    def extra_header(self):
        return EXTRA_HEADER

    def render_author(self, author):
        out = render_command('author', author['name'])

        if 'email' in author:
            out += render_command('email', author['email'])

        if 'affiliation' in author:
            out += "\\affiliation{%\n"
            out += indent(''.join(
                    render_command(key, value)
                    for key, value in author['affiliation'].items()))
            out += "}\n"
        return out

    def render_acknowledgements(self):
        try:
            return render_env('acks', self.acknowledgements)
        except AttributeError:
            return None
