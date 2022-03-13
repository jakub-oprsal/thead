from common import *


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


def header(data, **kwargs):
    cls_opts = list(kwargs['classoptions']) if 'classoptions' in kwargs else []

    if 'anonymous' in kwargs and kwargs['anonymous']:
        cls_opts.append('anonymous')

    headers = [
        render_command(
            'documentclass',
            'lipics-v2021',
            ','.join(cls_opts)),
        render_encs]

    if 'header_include' in data:
        headers.append(include_file(data['header_include']))

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

    headers += [render_begin,
            '\\maketitle\n',
            render_abstract(data['abstract']),
            '']

    return '\n'.join(headers)


def footer(data):
    return '\n'.join(('',
            render_bib('plainurl', data['bibliography']),
            render_end))
