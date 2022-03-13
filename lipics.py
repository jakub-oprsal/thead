from common import *

##
# THE TEMPLATE
#
HEADER = '''{documentclass}
\\usepackage[utf8]{{inputenc}}
\\usepackage[T1]{{fontenc}}

{include}

{title}
{authors}
{authors_running}
{copy}
{funding}
{keywords}
{ccs}
{acks}

\\begin{{document}}

\\maketitle

{abstract}
'''

FOOTER = '''
\\bibliographystyle{{plainurl}}
\\bibliography{{{bibfile}}}

\\end{{document}}
'''

def render_title(data):
    out = render_command('title', data['title'])
    if 'shorttitle' in data:
        out += render_command('titlerunning', data['shorttitle'])
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
    {{{institution}}}{{{email}}}{{{orcid_url}}}{{{funding}}}\n'''

def render_funding(funds):
    note = "\n".join(grant['note'] for grant in funds if 'note' in grant)
    return render_command('funding', note)

def render_authors_running(authors):
    return render_command('authorrunning', authors_list(authors, short=True))

def render_copyright(authors):
    cc = authors_list(authors)
    return render_command('Copyright', cc)

def render_acks(acks):
    return render_command('acknowledgements', acks)


def header(data, **kwargs):
    cls_opts = list(kwargs[classoptions]) if 'classoptions' in kwargs else []
    if 'anonymous' in kwargs and kwargs['anonymous']:
        cls_opts.append('anonymous')
    documentclass = render_command(
            'documentclass',
            'lipics-v2021',
            ','.join(cls_opts))

    return HEADER.format(
        documentclass = documentclass,
        title = render_title(data),
        authors = "\n".join(map(render_author, data['authors'])),
        authors_running = render_authors_running(data['authors']),
        copy = render_copyright(data['authors']),
        keywords = render_keywords(data['keywords']),
        ccs = render_ccs(data['ccs2012']) if 'ccs2012' in data else '',
        acks = render_acks(data['acknowledgements']) if 'acknowledgements' in
            data else '',
        funding = render_funding(data['funding']) if 'funding' in data else '',
        abstract = render_abstract(data['abstract'].strip()),
        include = include_file(data['header_include']) if 'header_include' in
            data else '')


def footer(data):
    return FOOTER.format(bibfile = ",".join(data['bibliography']))
