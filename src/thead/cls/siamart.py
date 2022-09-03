from .article import Article
from ..tex import render_command, render_env
from ..u2tex import u2tex


class SIAMart(Article):
    provides = ['siamart']

    def setup(self):
        if self.cname is None:
            self.cname = 'siamart190516'
        super().setup()
        self.bibstyle = 'siamplain'

    def render_keywords(self):
        try:
            return render_env('keywords', ", ".join(self.keywords))
        except AttributeError:
            return None

    def render_author(self, author):
        thanks = []
        if 'affiliation' in author:
            thanks.append(self.render_address(author['affiliation']))
        if 'email' in author:
            thanks.append('({})'.format(
                render_command('email', author['email']).strip()))
        address = render_command('thanks', '\n'.join(thanks)) if thanks else ''
        return u2tex(author['name']) + '%\n' + address

    def extra_header(self):
        return '\\usepackage{amssymb,amsmath}\n' \
               '\\newsiamthm{claim}{Claim}\n' \
               '\\newsiamthm{conjecture}{Conjecture}\n' \
               '\\newsiamremark{example}{Example}\n' \
               '\\newsiamremark{remark}{Remark}\n'
