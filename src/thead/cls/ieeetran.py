from .article import Article
from ..tex import indent, render_command, render_env


class IEEEtran(Article):
    provides = ['IEEEtran', 'ieeetran']

    def setup(self):
        if self.cname is None:
            self.cname = 'IEEEtran'

        self.headers += [
                self.render_encs,
                self.macro,
                self.render_title,
                self.render_authors,
                self.begin_document,
                self.maketitle,
                self.render_abstract,
                self.render_keywords
                ]

        if 'noheader' in self.opts:
            self.opts.remove('noheader')
        else:
            self.headers.insert(3, self.extra_header)

        self.footers.insert(0, self.render_acknowledgements)
        self.bibstyle = 'IEEEtran'

    def extra_header(self):
        header = render_command('usepackage', 'amsmath, amssymb, amsthm')
        header += render_command('usepackage', 'flushend')
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

    def render_author(self, author):
        addr = author['affiliation']
        add = []
        if 'department' in addr:
            add.append(addr['department'])
        if 'institution' in addr:
            add.append(addr['institution'])
        add.append(addr['city'] + ', ' + addr['country'])
        add.append('Email: {}'.format(author['email']))

        return render_command('IEEEauthorblockN', author['name']) + \
               render_command('IEEEauthorblockA', '\\\\\n'.join(add))

    def render_keywords(self):
        try:
            return render_env('IEEEkeywords', "; ".join(self.keywords))
        except AttributeError:
            return None




