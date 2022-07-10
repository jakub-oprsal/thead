from .default import Article
from .tex import indent, render_command, render_env, include


HEADER = r'''\usepackage{tikz}
\definecolor{purple}{cmyk}{0.55,1,0,0.15}
\definecolor{darkblue}{cmyk}{1,0.58,0,0.21}
\usepackage[colorlinks,
  linkcolor=black,
  urlcolor=darkblue,
  citecolor=purple]{hyperref}
\urlstyle{same}

\newtheorem{theorem}{Theorem}[section]
\newtheorem{lemma}[theorem]{Lemma}
\newtheorem{proposition}[theorem]{Proposition}
\newtheorem{corollary}[theorem]{Corollary}
\newtheorem{conjecture}[theorem]{Conjecture}
\newtheorem{claim}[theorem]{Claim}
\theoremstyle{definition}
\newtheorem{definition}[theorem]{Definition}
\newtheorem{example}[theorem]{Example}
\newtheorem{remark}[theorem]{Remark}
'''


class AMSart(Article):
    provides = ['amsart']

    def __init__(self, meta, **kwargs):
        super(AMSart, self).__init__(meta, **kwargs)

        if self.cname is None:
            self.cname = 'amsart'

        self.headers = [
                self.render_comment,
                self.render_documentclass,
                self.includes,
                self.render_pdfmeta,
                self.begin_document,
                self.render_title,
                self.render_authors,
                self.render_funding,
                self.render_abstract,
                self.render_keywords,
                self.maketitle,
                ]

        if 'noheader' in self.opts:
            self.opts.remove('noheader')
        else:
            self.headers.insert(2, self.render_encs)
            self.headers.insert(3, self.extra_header)

        self.footers.insert(0, self.render_acknowledgements)
        self.bibstyle = 'alphaurl'

    def extra_header(self):
        return HEADER

    def render_pdfmeta(self):
        authors = self.authors_list(short=True)
        return f'''\\hypersetup{{%
    pdftitle  = {{{self.title}}},
    pdfauthor = {{{authors}}}}}\n'''

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

    def render_acknowledgements(self):
        try:
            return r'\subsection*{Acknowledgements}' + '\n\n' + \
                   self.acknowledgements.strip() + '\n'
        except AttributeError:
            return None
