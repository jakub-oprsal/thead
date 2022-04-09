from .common import *


header_include = r'''\geometry{a4paper}
\citestyle{acmauthoryear}
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


def header(data, **kwargs):
    cls_opts = ['nonacm', '11pt']

    if 'classoptions' in kwargs:
        cls_opts += kwargs['classoptions']

    if 'anonymous' in kwargs and kwargs['anonymous']:
        cls_opts.append('anonymous')

    headers = [
        render_command(
            'documentclass',
            'acmart',
            ','.join(cls_opts)),
        render_encs,
        header_include]

    if 'header_include' in data:
        headers.append(include(data['header_include']))

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


def footer(data):
    footers = ['']

    if 'acknowledgements' in data:
        footers.append(render_env('acks', data['acknowledgements']))

    footers += [
            render_bib('ACM-Reference-Format', data['bibliography']),
            end_document]

    return '\n'.join(footers)
