from .amsart import AMSart
from ..tex import indent, render_command, render_env


def xmltag(tag, content, inline=False):
    if inline:
        return f'<{tag}>{content}</{tag}>\n'
    else:
        text = indent(''.join(content))
        return f'<{tag}>\n{text}</{tag}>\n'


class CCS:
    def __init__(self, concepts):
        self.concepts = concepts

    def tex(self):
        return ''.join(render_command('ccsdesc',
                                      concept['desc'],
                                      concept.get('significance'))
                       for concept in self.concepts)

    def _xml_concept(self, concept):
        return xmltag('concept', (xmltag(f'concept_{key}', value, inline=True)
                                  for key, value in concept.items()))

    def xml(self):
        return xmltag('ccs2012', map(self._xml_concept, self.concepts))

    def render(self):
        return render_env('CCSXML', self.xml().strip()) + self.tex()


class ACMart(AMSart):
    provides = ['acmart']

    def setup(self):
        if self.cname is None:
            self.cname = 'acmart'

        if self.bibstyle is None:
            self.bibstyle = 'ACM-Reference-Format'

        if self.anonymous and 'anonymous' not in self.opts:
            self.opts.append('anonymous')

        self.headers += [
                self.extra_header,
                self.macro,
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

    def extra_header(self):
        return '\\citestyle{acmauthoryear}\n' \
               '\\setcitestyle{nosort}\n' \
               '\\AtEndPreamble{%\n' \
               '    \\theoremstyle{acmdefinition}\n' \
               '    \\newtheorem{claim}[theorem]{Claim}}\n'

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

    def render_ccs2012(self):
        try:
            return CCS(self.ccs2012['concepts']).render()
        except AttributeError:
            return None
