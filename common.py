# common.py
#
# Common functions for rendering TeX headers and content
#
import re, codecs
from itertools import chain


def indent(string):
    return "\n".join(map(lambda line: "  " + line, string.split("\n")))


def render_env(envname, content):
    return (f'\\begin{{{envname}}}\n'
            f'{indent(content)}\n'
            f'\\end{{{envname}}}\n')

render_encs = r'''\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
'''
maketitle = '\\maketitle\n'
begin_document = '\\begin{document}\n'
end_document = '\\end{document}\n'


def render_command(command, a, b=''):
    atr = f'[{b}]' if b != '' else ''
    return f'\\{command}{atr}{{{a}}}\n'


## CCS CLASSIFICATION

def render_ccs_tex(ccs):
    return ''.join(render_command('ccsdesc',
                concept['desc'],
                concept['significance'] if 'significance' in concept else None)
            for concept in ccs['concepts'])

CCS_CONCEPT = '''  <concept>
    <concept_id>{_id}</concept_id>
    <concept_desc>{_desc}</concept_desc>
    <concept_significance>{_significance}</concept_significance>
  </concept>'''

def render_ccs_xml(ccs):
    concepts = '\n'.join(CCS_CONCEPT.format(
            _id = concept['id'],
            _desc = concept['desc'],
            _significance = concept['significance'])
        for concept in ccs['concepts'])
    return render_env('CCSXML', f'<ccs2012>\n{concepts}\n</ccs2012>')

def render_ccs(ccs):
    return render_ccs_xml(ccs) + render_ccs_tex(ccs)


## ABSTRACT AND KEYWORDS

def render_abstract(abstract):
    return render_env('abstract', abstract.strip())

def render_keywords(keywords):
    return render_command('keywords', ", ".join(keywords))


## AUTHORS AND LISTS OF AUTHOR NAMES

def shorten_name(name):
    names = name.split(' ')
    initials = ".".join(map(lambda x: x[0], names[:-1]))
    return initials + ". " + names[-1]

def join_names(names):
    list_names = list(names)
    if len(list_names) == 1:
        return list_names[0]
    elif len(list_names) == 2:
        return ' and '.join(list_names)
    else:
        return ', and '.join((', '.join(list_names[:-1]), list_names[-1]))

def authors_list(authors, short=False):
    if short:
        return join_names(map(
            lambda author: shorten_name(author['name']),
            authors))
    else:
        return join_names(map(lambda author: author['name'], authors))

## HEADER INCLUDE

def include(filename, end=''):
    if not re.match(r'.*\.tex', filename):
        filename += '.tex'
    with codecs.open(filename, encoding='utf-8') as file:
        return file.read().strip() + '\n' + end

## BIB

def render_bib(bibstyle, bibfiles):
    out = render_command('bibliographystyle', bibstyle)
    out += render_command('bibliography', ','.join(bibfiles))
    return out
