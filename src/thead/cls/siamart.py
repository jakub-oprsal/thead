from .article import Article
from ..tex import render_command, render_env
from ..u2tex import u2tex


class SIAMart(Article):
    provides = ['siamart','siamart190516','siamart220329']

    def setup(self):
        if self.cname is None:
            self.cname = 'siamart220329' if self.cls == 'siamart' else self.cls
        super().setup()

        self.headers.insert(4, self.running_heads)
        self.bibstyle = 'siamplain'

    def running_heads(self):
        try:
            title = self.shorttitle
        except AttributeError:
            title = self.title
        authors = u2tex(self.authors_list(short=True))
        return f'\\headers{{{title}}}{{{authors}}}'

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

    def title_note(self):
        try:
            note = self.note
        except AttributeError:
            note = ''
        try:
            funding = '\n'.join(u2tex(grant['note'])
                                for grant in self.funding
                                if 'note' in grant)
            note += render_command('funding', funding)
        except AttributeError:
            pass
        return note

    def render_title(self):
        title = u2tex(self.title)
        note = self.title_note()
        if note:
            title += '%\n' + render_command('thanks', note)
        return render_command('title', title)

    def extra_header(self):
        return '\\usepackage{amssymb,amsmath}\n' \
               '\\newsiamthm{claim}{Claim}\n' \
               '\\newsiamthm{conjecture}{Conjecture}\n' \
               '\\newsiamremark{example}{Example}\n' \
               '\\newsiamremark{remark}{Remark}\n'
