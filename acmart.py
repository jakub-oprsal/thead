from common import *

HEADER = '''\\documentclass[{classoptions}]{{acmart}}
\\geometry{{a4paper}}

\\usepackage[utf8]{{inputenc}}
\\usepackage[T1]{{fontenc}}

\\citestyle{{acmauthoryear}}
\\setcitestyle{{nosort}}

{include}
\\AtEndPreamble{{%
    \\theoremstyle{{acmdefinition}}
    \\newtheorem{{claim}}{{Claim}}[theorem]}}

\\title{{{title}}}

{authors}
{ccsdesc}
{keywords}
{abstract}
{thanks}
\\begin{{document}}

\\maketitle

'''

FOOTER = '''
\\bibliographystyle{{ACM-Reference-Format}}
\\bibliography{{{bibfile}}}

\\end{{document}}
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


def header(data):
    return HEADER.format(
        classoptions = 'nonacm,11pt',
        title = data['title'],
        authors = "\n".join(map(render_author, data['authors'])),
        ccsdesc = render_ccs(data['ccs2012']) if 'ccs2012' in data else '',
        keywords = render_keywords(data['keywords']) if 'keywords' in data else '',
        abstract = render_abstract(data['abstract']) if 'abstract' in data else '',
        thanks = render_funding(data['funding']) if 'funding' in data else '',
        include = include_file(data['header_include']) if 'header_include' in data else '')

def footer(data):
    return FOOTER.format(bibfile = ",".join(data['bibliography']))
