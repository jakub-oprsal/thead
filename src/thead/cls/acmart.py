from .default import Article
from .tex import indent, render_command, render_env, include


HEADER_INCLUDE = r'''\citestyle{acmauthoryear}
\setcitestyle{nosort}
\AtEndPreamble{%
    \theoremstyle{acmdefinition}
    \newtheorem{claim}{Claim}[theorem]}
'''


class Acmart(Article):
    provides = ['acmart']

    def __init__(self, meta, **kwargs):
        super(Acmart, self).__init__(meta, **kwargs)

        if self.cname is None:
            self.cname = 'acmart'
        self.bibstyle = 'ACM-Reference-Format'

        if self.anonymous and 'anonymous' not in self.opts:
            self.opts.append('anonymous')


        self.headers = [
                self.render_comment,
                self.render_documentclass,
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
        self.biblopgraphystyle = 'ACM-Reference-Format'

    def check(self):
        if self.title is None or self.authors is None:
            raise KeyError
        else:
            return True

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

    def render_funding(self):
        try:
            funding_note = '\n'.join(grant['note']
                    for grant in self.funding
                    if 'note' in grant)
            return render_command('thanks', funding_note)
        except AttributeError:
            return None

    def render_acknowledgements(self):
        try:
            return render_env('acks', self.acknowledgements)
        except AttributeError:
            return None

    def includes(self):
        out = [HEADER_INCLUDE]
        out += (include(file) for file in self.include)
        return ''.join(out)
