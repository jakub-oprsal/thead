"""
    Extension to `marko` markdown parser to be able to render useful tex files
    for chapters, support of math & theorem environments.

    https://github.com/frostming/marko
"""
import codecs, sys, re
import marko
from marko.ext.latex_renderer import LatexRenderer as MarkoLatexRenderer


class InlineMath(marko.inline.InlineElement):

    priority = 10
    pattern = re.compile(r"\$\s*([^$]+)\s*\$")
    parse_children = False

    def __init__(self, match):
        self.content = match.group(1)


class DisplayMath(marko.inline.InlineElement):

    priority = 10
    pattern = re.compile(r'\\\[\s*(?:{([a-z]*\*?)})?\s*\n((?:(?!\\\]).*\s*\n)*)\\\]\s*$', re.M)
    parse_children = False

    def __init__(self, match):
        self.envname = match.group(1) if match.group(1) else None
        self.content = match.group(2).rstrip()


class Quotes(marko.inline.InlineElement):

    priority = 3
    pattern = re.compile(r'(?<!\S)([\'"])([^\'"]*)\1')
    parse_children = True

    def __init__(self, match):
        if match.group(1) == '"':
            self.content = "``{}''".format(match.group(2))
        else:
            self.content = "`{}'".format(match.group(2))


class Label(marko.inline.InlineElement):

    priority = 4
    pattern = re.compile(r'{#([-_+a-zA-Z0-9:]*)}')
    parse_children = False

    def __init__(self, match):
        self.label = match.group(1)


class RefLabel(marko.inline.InlineElement):

    priority = 4
    pattern = re.compile(r'{@([-_+a-zA-Z0-9:]*)}')
    parse_children = False

    def __init__(self, match):
        self.label = match.group(1)


class Cite(marko.inline.InlineElement):

    priority = 6
    pattern = re.compile(r'\[(?:(@[-_+a-zA-Z0-9:]*(?:,\s*@[-_+a-zA-Z0-9:]*)*)|'
        r'@([-_+a-zA-Z0-9:]*),\s*([^@][^\]]*)?)\]')
    parse_children = False

    def __init__(self, match):
        if match.group(1) is None:
            self.label = match.group(2)
            self.comment = match.group(3)
        else:
            label = match.group(1).split(',')
            self.label = ','.join(map(lambda m: m.strip().lstrip('@'), label))
            self.comment = None


class TheoremEnv(marko.block.BlockElement):

    envs = {"Theorem": "theorem",
            "Lemma": "lemma",
            "Proposition": "proposition",
            "Corollary": "corollary",
            "Claim": "claim",
            "Proof": "proof",
            "Definition": "definition",
            "Example": "example",
            "Remark": "remark",
            "Note": "note",
            "Conjecture": "conjecture"}

    pattern = re.compile(r"({})\. *(?=\S|\n)".format("|".join(envs)))
    priority = 4

    def __init__(self, match):
        self.env = self.envs[match.group(1)]
        self._prefix = re.escape(match.group())
        self._second_prefix = r' {2,4}'

    @classmethod
    def match(cls, source):
        return source.expect_re(cls.pattern)

    @classmethod
    def parse(cls, source):
        state = cls(source.match)
        with source.under_state(state):
            state.children = marko.block.parser.parse(source)
        return state


class ElementsExt:
    elements = [InlineMath, DisplayMath, TheoremEnv, Quotes, Label, RefLabel, Cite]


class LatexRenderer(MarkoLatexRenderer):

    def render_document(self, element):
        return self.render_children(element)

    def render_heading(self, element):
        children = self.render_children(element)
        headers = ["section", "subsection", "subsubsection", "subsubsection*",
                "paragraph*", "subparagraph*"]
        header = headers[element.level - 1]
        return f"\\{header}{{{children}}}\n"

    def render_setext_heading(self, element):
        return self.render_heading(element)

    def render_emphasis(self, element):
        children = self.render_children(element)
        return f"\\emph{{{children}}}"

    def render_inline_math(self, element):
        return f'${element.content}$'

    def render_display_math(self, element):
        content = element.content
        displaytex = ''
        for line in content.split('\n'):
            displaytex += '  ' + line + '\n'
        if element.envname is None:
            return f'\[\n{displaytex}\]'
        else:
            return self._environment(element.envname, displaytex)

    def render_theorem_env(self, element):
        children = self.render_children(element).strip() + '\n'
        return self._environment(element.env, children) + '\n'

    def render_label(self, element):
        return f'\\label{{{element.label}}}'

    def render_ref_label(self, element):
        return f'\\ref{{{element.label}}}'

    def render_cite(self, element):
        if element.comment is not None:
            return f'\\cite[{element.comment}]{{{element.label}}}'
        else:
            return f'\\cite{{{element.label}}}'

    def render_quotes(self, element):
        return element.content

    def render_raw_text(self, element):
        return self._escape_plaintext(element.children)

    @staticmethod
    def _escape_plaintext(text: str) -> str:
        # Special LaTeX Character:  # $ % ^ & _ { } ~ \
        specials = {
            "#": "\\#",
            "$": "\\$",
            "≠": "$\\neq$",
        }

        return "".join(specials.get(s, s) for s in text)


tmarko = marko.Markdown(marko.Parser, LatexRenderer, extensions=[ElementsExt])


if __name__ == "__main__":
    filename = sys.argv[1]
    with codecs.open(filename, encoding="utf-8") as file:
        content = file.read()

    result = tmarko(content)
    print(result)
