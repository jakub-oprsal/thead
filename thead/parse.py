from datetime import datetime
from .cls import cls_module
from .cls.common import include, render_command, authors_list


COMMENT = '''% Generated by <https://github.com/jakub-oprsal/thead> on {now}
%
% {title}
% by {authors}
%
'''

def parse(meta, recipe, args):
    """ Parses metadata, creates headers, content, and footer, and yields
        these to be written into a file consecutively """

    clsmodule = cls_module(args.cls)

    ## HEADER
    yield COMMENT.format(
            now = datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            title = meta['title'].upper(),
            authors = authors_list(meta['authors'], short = True))
    yield clsmodule.header(
            meta,
            cname=args.cname,
            anonymous=args.anonymous,
            classoptions=args.opts,
            include=recipe.header)

    ## BODY
    _include = include if args.include else \
            lambda fn, end: render_command('input', fn) + end
    for filename in recipe.content:
        yield _include(filename, '\n')
    if recipe.appendix:
        body += '\n\\appendix\n\n'
        for filename in recipe.appendix:
            yield include(filename, '\n')

    ## FOOTER
    yield clsmodule.footer(meta, recipe.bib)
    return
