from ..u2tex import u2tex
from .common import *
from .amsart import render_acks


HEADER = r'''\usepackage{amssymb,amsmath}
\newsiamthm{claim}{Claim}
\newsiamthm{conjecture}{Conjecture}
\newsiamremark{example}{Example}
\newsiamremark{remark}{Remark}
'''


def render_keywords(keywords):
    return render_env('keywords', ", ".join(keywords))


def render_address(addr):
    out = []
    if 'department' in addr:
        out.append(addr['department'])
    if 'institution' in addr:
        out.append(addr['institution'])
        if 'city' in addr and addr['city'] not in addr['institution']:
            out.append(addr['city'])
    elif 'city' in addr:
        out.append(addr['city'])
    if 'country' in addr:
        out.append(addr['country'])
    return ', '.join(out)


def render_author(author):
    thanks = []
    if 'affiliation' in author:
        thanks.append(render_address(author['affiliation']))
    if 'email' in author:
        thanks.append('({})'.format(render_command('email', author['email'])))
    address = render_command('thanks', '\n'.join(thanks)) if thanks else ''
    return u2tex(author['name']) + '%\n' + address


def render_authors(authors):
    return render_command(
            'author',
            '\\and\n'.join(render_author(author) for author in authors))


def render_funding(funds):
    funding_note = '\n'.join(grant['note']
            for grant in funds
            if 'note' in grant)
    return render_command('thanks', funding_note)


def header(data, cname=None, classoptions=[], **kwargs):
    if cname is None:
        cname = 'siamart190516'

    if 'noheader' in classoptions:
        classoptions.remove('noheader')
        include_header = False
    else:
        include_header = True

    headers = [
        render_command(
            'documentclass',
            cname,
            ','.join(classoptions)),
        render_encs]

    if include_header:
        headers.append(HEADER)

    if 'include' in kwargs:
        headers += [include(file) for file in kwargs['include']]

    if 'funding' in data:
        title = render_command('title',
            u2tex(data['title']) + '%\n' + render_funding(data['funding']))
    else:
        title = render_command('title', data['title'])

    headers += [
            title,
            render_authors(data['authors']),
            begin_document,
            maketitle,
            ]

    if 'abstract' in data:
        headers.append(render_abstract(data['abstract']))

    if 'keywords' in data:
        headers.append(render_keywords(data['keywords']))

    headers.append('')

    return '\n'.join(headers)


def footer(data, bib):
    footers = ['']
    if 'acknowledgements' in data:
        footers.append(render_acks(data['acknowledgements']))
    if bib:
        footers.append(render_bib('alphaurl', bib))
    footers.append(end_document)

    return '\n'.join(footers)
