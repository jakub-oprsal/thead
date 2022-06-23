from .default import Article
from .tex import indent, render_command, render_env, include
from ..u2tex import u2tex


HEADER = r'''\usepackage{amssymb,amsmath}
\newsiamthm{claim}{Claim}
\newsiamthm{conjecture}{Conjecture}
\newsiamremark{example}{Example}
\newsiamremark{remark}{Remark}
'''

class SIAMart(Article):
    provides = ['siamart']

    def __init__(self, meta, **kwargs):
        super(SIAMart, self).__init__(meta, **kwargs)

        if self.cname is None:
            self.cname = 'siamart190516'

        self.headers = [
                self.render_comment,
                self.render_documentclass,
                self.render_encs,
                self.includes,
                self.render_title,
                self.render_authors,
                self.begin_document,
                self.maketitle,
                self.render_abstract,
                self.render_keywords,
                ]

        if 'noheader' in self.opts:
            self.opts.remove('noheader')
        else:
            self.headers.insert(3, self.extra_header)

        self.footers.insert(0, self.render_acknowledgements)
        self.bibstyle = 'siamplain'

    def render_title(self):
        title = u2tex(self.title)
        if hasattr(self, 'funding'):
            title += '%\n' + self.render_funding()
        return render_command('title', title)

    def render_keywords(self):
        try:
            return render_env('keywords', ", ".join(self.keywords))
        except AttributeError:
            return None

    def render_address(self, addr):
        out = []
        if 'department' in addr:
            out.append(addr['department'])
        if 'institution' in addr:
            out.append(addr['institution'])
            if 'city' in addr and addr['city'] not in addr['institution']:
                out.append(addr['city'])
        elif 'city' in addr:
            out.append(addr['city'])
        if 'country' in addr:
            out.append(addr['country'])
        return ', '.join(out)

    def render_author(self, author):
        thanks = []
        if 'affiliation' in author:
            thanks.append(self.render_address(author['affiliation']))
        if 'email' in author:
            thanks.append('({})'.format(
                render_command('email', author['email']).strip()))
        address = render_command('thanks', '\n'.join(thanks)) if thanks else ''
        return u2tex(author['name']) + '%\n' + address

    def render_authors(self):
        return render_command('author',
                              '\\and\n'.join(self.render_author(author)
                                             for author in self.authors))

    def extra_header(self):
        return HEADER

    def render_acknowledgements(self):
        try:
            return r'\subsection*{Acknowledgements}' + '\n\n' + \
                   self.acknowledgements.strip() + '\n'
        except AttributeError:
            return None
