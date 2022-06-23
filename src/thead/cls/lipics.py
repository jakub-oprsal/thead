from .default import Article
from .tex import indent, render_command, render_env, include


class LIPIcs(Article):
    provides = ['lipics', 'lipics-v2021']

    def __init__(self, meta, **kwargs):
        super(LIPIcs, self).__init__(meta, **kwargs)

        if self.cname is None:
            self.cname = 'lipics-v2021'

        if self.anonymous and 'anonymous' not in self.opts:
            self.opts.append('anonymous')

        # abstract and keywords are mandatory
        # raise AttributeError if missing
        _ = self.abstract, self.keywords

        #\hideLIPIcs  %to remove references to LIPIcs series (logo, DOI, ...), e.g. when preparing a pre-final version to be uploaded to arXiv or another public repository
        #%\nolinenumbers %uncomment to disable line numbering

        self.headers = [
                self.render_comment,
                self.render_documentclass,
                self.includes,
                self.render_title,
                self.render_shorttitle,
                self.render_authors,
                self.render_authorsrunning,
                self.render_copyright,
                self.render_funding,
                self.render_keywords,
                self.render_ccs2012,
                self.render_acknowledgements,
                self.begin_document,
                self.maketitle,
                self.render_abstract,
                ]

        self.bibstyle = 'plainurl'

    def render_title(self):
        return render_command('title', self.title)

    def render_shorttitle(self):
        try:
            return render_command('titlerunning', self.shorttitle)
        except AttributeError:
            return None

    def render_author(self, author):
        name = author['name']
        if 'affiliation' in author:
            institution = ', '.join(value for _, value in
                    author['affiliation'].items())
        else:
            institution = ''
        email = author.get('email', '')
        orcid_url = 'https://orcid.org/{}'.format(author['orcid']) \
                    if 'orcid' in author else ''
        funding = author.get('funding', '')

        return f'''\\author{{{name}}}
        {{{institution}}}
        {{{email}}}
        {{{orcid_url}}}
        {{{funding}}}\n'''

    def render_authorsrunning(self):
        return render_command('authorrunning', self.authors_list(short=True))

    def render_copyright(self):
        return render_command('Copyright', self.authors_list())

    def render_funding(self):
        return super().render_funding(command='funding')

    def render_acknowledgements(self):
        return render_command('acknowledgements', self.acknowledgements)
