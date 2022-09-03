from .article import Article
from ..tex import render_command


class AMSart(Article):
    provides = ['amsart']

    def setup(self):
        if self.cname is None:
            self.cname = 'amsart'

        if 'noheader' in self.opts:
            self.opts.remove('noheader')
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
        self.bibstyle = 'alphaurl'

    def extra_header(self):
        header = render_command(
                'usepackage',
                'hyperref',
                'colorlinks, citecolor=blue, linkcolor=black, urlcolor=red')
        header += render_command('urlstyle', 'same')
        header += '\\newtheorem{theorem}{Theorem}[section]\n' \
                  '\\newtheorem{lemma}[theorem]{Lemma}\n' \
                  '\\newtheorem{proposition}[theorem]{Proposition}\n' \
                  '\\newtheorem{corollary}[theorem]{Corollary}\n' \
                  '\\newtheorem{conjecture}[theorem]{Conjecture}\n' \
                  '\\newtheorem{claim}[theorem]{Claim}\n' \
                  '\\theoremstyle{definition}\n' \
                  '\\newtheorem{definition}[theorem]{Definition}\n' \
                  '\\newtheorem{example}[theorem]{Example}\n' \
                  '\\newtheorem{remark}[theorem]{Remark}\n'
        return header

    def render_pdfmeta(self):
        authors = self.authors_list(short=True)
        return '\\hypersetup{%\n' \
               f'  pdftitle  = {{{self.title}}}\n' \
               f'  pdfauthor = {{{authors}}}}}\n'

    def render_title(self):
        shorttitle = self.__dict__.get('shorttitle', '')
        return render_command('title', self.title, shorttitle)

    def render_author(self, author):
        out = render_command('author', author['name'])
        if 'affiliation' in author:
            out += render_command('address',
                ", ".join(value for _, value in author['affiliation'].items()))
        if 'email' in author:
            out += render_command('email', author['email'])
        return out

    def render_authors(self):
        return '\n'.join(map(self.render_author, self.authors))

    def render_funding(self):
        note = self.funding_note()
        if note is not None:
            return render_command('thanks', note)
        else:
            return None
