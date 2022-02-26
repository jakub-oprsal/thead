from common import *

##
# THE TEMPLATE
#
HEADER = '''\\documentclass{{lipics-v2021}}

\\usepackage[utf8]{{inputenc}}
\\usepackage[T1]{{fontenc}}

{include}

\\title{{{title}}}

{authors}

\\authorrunning{{{authorsrunning}}}
\\Copyright{{{_copyright}}}
\\funding{{{funding}}}

\\keywords{{{keywords}}}

{ccs}

\\begin{{document}}

\\maketitle

{abstract}
'''

FOOTER = '''
\\bibliographystyle{{plainurl}}
\\bibliography{{{bibfile}}}

\\end{{document}}
'''


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
    return "\n".join(grant['note']
            for grant in funds
            if 'note' in grant)

def header(data):
    return HEADER.format(
        title = data['title'],
        authors = "\n".join(map(render_author, data['authors'])),
        authorsrunning = authors_list(data['authors'], short=True),
        _copyright = authors_list(data['authors']),
        keywords = ", ".join(data['keywords']),
        ccs = render_ccs(data['ccs2012']) if 'ccs2012' in data else '',
        bibfile = ",".join(data['bibliography']),
        funding = render_funding(data['funding']) if 'funding' in data else '',
        abstract = render_abstract(data['abstract'].strip()),
        include = include_file(data['header_include']) if 'header_include' in
        data else '')


def footer(data):
    return FOOTER.format(bibfile = ",".join(data['bibliography']))
