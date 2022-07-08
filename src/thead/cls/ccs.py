from .tex import render_command, render_env, indent


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

