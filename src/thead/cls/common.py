'''
Basic functions for building (more) complicated class compilers.
'''
import re, codecs
from textwrap import indent


def indent_two(lines):
    return indent(lines, ' '*2)


def render_command(command, a, b=''):
    atr = f'[{b}]' if b != '' else ''
    return f'\\{command}{atr}{{{a}}}\n'


def render_env(envname, content):
    return render_command('begin', envname) + \
           f'{indent_two(content)}\n' + \
           render_command('end', envname)

maketitle = '\\maketitle\n'
begin_document = render_command('begin', 'document')
end_document = render_command('end', 'document')
render_encs = render_command('usepackage', 'inputenc', 'utf8') + \
              render_command('usepackage', 'fontenc', 'T1')

## CCS CLASIFICATION

def render_ccs_tex(concepts):
    return ''.join(render_command('ccsdesc',
                concept['desc'],
                concept.get('significance'))
            for concept in concepts)

def xmltag(tag, text, inline=False):
    return f'<{tag}>{text}</{tag}>\n' if inline \
           else f'<{tag}>\n{indent_two(text)}</{tag}>\n'

def concept_xml(concept):
    content = ''.join(xmltag(f'concept_{key}', value, inline=True)
                      for key, value in concept.items())
    return xmltag('concept', content)

def render_ccs_xml(concepts):
    return xmltag('ccs2012', ''.join(map(concept_xml, concepts)))

def render_ccs(ccs):
    concepts = ccs['concepts']
    return render_env('CCSXML', render_ccs_xml(concepts).strip()) + \
           render_ccs_tex(concepts)


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

def _and(strs):
    list_strs = list(strs)
    if len(list_strs) == 1:
        return list_strs[0]
    elif len(list_strs) == 2:
        return ' and '.join(list_strs)
    else:
        return ', and '.join((', '.join(list_strs[:-1]), list_strs[-1]))

def authors_list(authors, short=False):
    names = map(lambda author: author['name'], authors)
    return _and(map(shorten_name, names)) if short else _and(names)


def include(filename, end=''):
    ''' Includes content of a file given by name with or without ".tex"
        extension. '''
    if not re.match(r'.*\.tex', filename):
        filename += '.tex'
    with codecs.open(filename, encoding='utf-8') as file:
        return file.read().strip() + '\n' + end

## BIB

def render_bib(bibstyle, bibfiles):
    out = render_command('bibliographystyle', bibstyle)
    out += render_command('bibliography', ','.join(bibfiles))
    return out
