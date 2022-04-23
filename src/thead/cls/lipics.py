from .common import *


def render_title(title, shorttitle = None):
    out = render_command('title', title)
    if shorttitle is not None:
        out += render_command('titlerunning', shorttitle)
    return out


def render_author(author):
    name = author['name']
    email = author['email'] if 'email' in author else ''
    orcid_url = 'https://orcid.org/{}'.format(author['orcid']) if 'orcid' in author else ''
    funding = author['funding'] if 'funding' in author else ''

    if 'affiliation' in author:
        institution = ', '.join(value for _, value in
                author['affiliation'].items())
    else:
        institution = ''

    return f'''\\author{{{name}}}
    {{{institution}}}
    {{{email}}}
    {{{orcid_url}}}
    {{{funding}}}\n'''


def render_authors_running(authors):
    return render_command('authorrunning', authors_list(authors, short=True))


def render_copyright(authors):
    cc = authors_list(authors)
    return render_command('Copyright', cc)


def render_funding(funds):
    note = "\n".join(grant['note'] for grant in funds if 'note' in grant)
    return render_command('funding', note)


def render_acks(acks):
    return render_command('acknowledgements', acks)


def header(data, cname=None, classoptions=[], **kwargs):
    if cname is None:
        cname = 'lipics-v2021'

    if 'anonymous' in kwargs and kwargs['anonymous']:
        classoptions.append('anonymous')

    headers = [
        render_command(
            'documentclass',
            cname,
            ','.join(classoptions)),
        render_encs]

    if 'include' in kwargs:
        headers += [include(file) for file in kwargs['include']]

    if 'shorttitle' in data:
        headers.append(render_title(data['title'], data['shorttitle']))
    else:
        headers.append(render_title(data['title']))

    headers += ['\n'.join(map(render_author, data['authors'])),
            render_authors_running(data['authors']),
            render_copyright(data['authors'])]

    if 'funding' in data:
        headers.append(render_funding(data['funding']))

    headers.append(render_keywords(data['keywords']))

    if 'ccs2012' in data:
        headers.append(render_ccs(data['ccs2012']))

    if 'acknowledgements' in data:
        headers.append(render_acks(data['acknowledgements']))

    headers += [begin_document,
            maketitle,
            render_abstract(data['abstract']),
            '']

    return '\n'.join(headers)


def footer(data, bib):
    footers = ['']
    if bib:
        footers.append(render_bib('plainurl', bib))
    footers.append(end_document)

    return '\n'.join(footers)