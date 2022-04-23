from .common import *


header_include = r'''\citestyle{acmauthoryear}
\setcitestyle{nosort}

\AtEndPreamble{%
    \theoremstyle{acmdefinition}
    \newtheorem{claim}{Claim}[theorem]}
'''


def render_author(author):
    out = render_command('author', author['name'])

    if 'email' in author:
        out += render_command('email', author['email'])

    if 'affiliation' in author:
        out += "\\affiliation{%\n"
        for key, value in author['affiliation'].items():
            out += "  " + render_command(key, value)
        out += "}\n"
    return out


def render_funding(funds):
    funding_note = "\n".join(grant['note']
            for grant in funds
            if 'note' in grant)
    return render_command('thanks', funding_note)


def header(data, cname=None, classoptions=[], **kwargs):
    if cname is None:
        cname = 'acmart'

    if 'anonymous' in kwargs and kwargs['anonymous']:
        classoptions.append('anonymous')

    headers = [
        render_command(
            'documentclass',
            cname,
            ','.join(classoptions)),
        header_include]

    if 'include' in kwargs:
        headers += [include(file) for file in kwargs['include']]

    headers += [
        render_command('title', data['title']),
        '\n'.join(map(render_author, data['authors']))]

    if 'ccs2012' in data:
        headers.append(render_ccs(data['ccs2012']))

    if 'keywords' in data:
        headers.append(render_keywords(data['keywords']))

    if 'abstract' in data:
        headers.append(render_abstract(data['abstract'])),

    if 'funding' in data:
        render_funding(data['funding'])

    headers += [begin_document, maketitle, '']

    return '\n'.join(headers)


def footer(data, bib):
    footers = ['']
    if 'acknowledgements' in data:
        footers.append(render_env('acks', data['acknowledgements']))
    if bib:
        footers.append(render_bib('ACM-Reference-Format', bib))
    footers.append(end_document)

    return '\n'.join(footers)