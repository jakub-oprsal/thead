from common import *

HEADER = """\\documentclass[a4paper]{{amsart}}

\\usepackage[utf8]{{inputenc}}
\\usepackage[T1]{{fontenc}}

\\usepackage{{tikz}}
\\definecolor{{purple}}{{cmyk}}{{0.55,1,0,0.15}}
\\definecolor{{darkblue}}{{cmyk}}{{1,0.58,0,0.21}}
\\usepackage[colorlinks,
  linkcolor=black,
  urlcolor=darkblue,
  citecolor=purple]{{hyperref}}
\\urlstyle{{same}}

\\newtheorem{{theorem}}{{Theorem}}[section]
\\newtheorem{{lemma}}[theorem]{{Lemma}}
\\newtheorem{{proposition}}[theorem]{{Proposition}}
\\newtheorem{{corollary}}[theorem]{{Corollary}}
\\newtheorem{{conjecture}}[theorem]{{Conjecture}}
\\newtheorem{{claim}}[theorem]{{Claim}}

\\theoremstyle{{definition}}
\\newtheorem{{definition}}[theorem]{{Definition}}
\\newtheorem{{example}}[theorem]{{Example}}
\\newtheorem{{remark}}[theorem]{{Remark}}

{include}
{pdfmeta}

\\begin{{document}}

{title}

{authors}
{thanks}
{abstract}
{keywords}

\\maketitle
"""

FOOTER = """
{acks}
\\bibliographystyle{{alphaurl}}
\\bibliography{{{bibfile}}}

\\end{{document}}
"""

def render_author(author):
    out = render_command('author', author['name'])
    if 'affiliation' in author:
        out += render_command('address',
            ", ".join(value for _, value in author['affiliation'].items()))
    if 'email' in author:
        out += render_command('email', author['email'])
    return out

def render_funding(funds):
    funding_note = "\n".join(grant['note']
            for grant in funds
            if 'note' in grant)
    return render_command('thanks', funding_note)

PDFMETA="""\hypersetup{{%
    pdftitle={{{title}}},
    pdfauthor={{{author_list}}}}}"""

def render_pdfmeta(authors, title):
    return PDFMETA.format(
            title=title,
            author_list=authors_list(authors, short=True))

def render_title(data):
    if 'shorttitle' in data:
        return render_command('title', data['title'], data['shorttitle'])
    else:
        return render_comamnd('title', data['title'])

def render_acks(acks):
    return f'\subsection*{{Acknowledgements}}\n\n{acks}\n'

def header(data):
    return HEADER.format(
        title = render_title(data),
        authors = "\n".join(map(render_author, data['authors'])),
        pdfmeta = render_pdfmeta(data['authors'], data['title']),
        keywords = render_keywords(data['keywords']) if 'keywords' in data else '',
        abstract = render_abstract(data['abstract']) if 'abstract' in data else '',
        thanks = render_funding(data['funding']) if 'funding' in data else '',
        include = include_file(data['header_include']) if 'header_include' in
        data else '')

def footer(data):
    return FOOTER.format(
        bibfile = ",".join(data['bibliography']),
        acks = render_acks(data['acknowledgements']) if 'acknowledgements' in data else '')
