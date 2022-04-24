from .common import *


HEADER = r'''\usepackage{tikz}
\definecolor{purple}{cmyk}{0.55,1,0,0.15}
\definecolor{darkblue}{cmyk}{1,0.58,0,0.21}
\usepackage[colorlinks,
  linkcolor=black,
  urlcolor=darkblue,
  citecolor=purple]{hyperref}
\urlstyle{same}

\newtheorem{theorem}{Theorem}[section]
\newtheorem{lemma}[theorem]{Lemma}
\newtheorem{proposition}[theorem]{Proposition}
\newtheorem{corollary}[theorem]{Corollary}
\newtheorem{conjecture}[theorem]{Conjecture}
\newtheorem{claim}[theorem]{Claim}
\theoremstyle{definition}
\newtheorem{definition}[theorem]{Definition}
\newtheorem{example}[theorem]{Example}
\newtheorem{remark}[theorem]{Remark}
'''


def render_pdfmeta(authors, title):
    author_list = authors_list(authors, short=True)
    return f'''\\hypersetup{{%
    pdftitle  = {{{title}}},
    pdfauthor = {{{author_list}}}}}\n'''


def render_author(author):
    out = render_command('author', author['name'])
    if 'affiliation' in author:
        out += render_command('address',
            ", ".join(value for _, value in author['affiliation'].items()))
    if 'email' in author:
        out += render_command('email', author['email'])
    return out


def render_funding(funds):
    funding_note = '\n'.join(grant['note']
            for grant in funds
            if 'note' in grant)
    return render_command('thanks', funding_note)


def render_acks(acks):
    return f'\\subsection*{{Acknowledgements}}\n\n{acks.strip()}\n'


def header(data, cname=None, classoptions=[], **kwargs):
    if cname is None:
        cname = 'amsart'

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

    shorttitle = data['shorttitle'] if 'shorttitle' in data else ''
    headers += [
            render_pdfmeta(data['authors'], data['title']),
            begin_document,
            render_command('title', data['title'], shorttitle),
            '\n'.join(map(render_author, data['authors']))]

    if 'funding' in data:
        headers.append(render_funding(data['funding']))

    if 'abstract' in data:
        headers.append(render_abstract(data['abstract']))

    if 'keywords' in data:
        headers.append(render_keywords(data['keywords']))

    headers += [maketitle, '']

    return '\n'.join(headers)


def footer(data, bib):
    footers = ['']
    if 'acknowledgements' in data: # and not anonymous:
        footers.append(render_acks(data['acknowledgements']))
    if bib:
        footers.append(render_bib('alphaurl', bib))
    footers.append(end_document)

    return '\n'.join(footers)
