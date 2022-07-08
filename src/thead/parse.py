from .cls import IdentifyClass
from .cls.tex import include


def parse(meta, recipe, args):
    """ Parses metadata, creates headers, content, and footer, and yields
        these to be written into a file consecutively """

    Class = IdentifyClass(args.cls)

    article = Class(
            meta,
            cname=args.cname,
            anonymous=args.anonymous,
            classoptions=args.opts,
            include=recipe.header,
            bib=recipe.bib)

    ## HEADER
    yield '\n'.join(article.header())
    yield '\n'

    ## BODY
    _include = lambda fn: include(fn, end='\n', soft=not args.include)
    yield from map(_include, recipe.content)
    if recipe.appendix:
        yield '\n\\appendix\n\n'
        yield from map(_include, recipe.appendix)

    ## FOOTER
    yield '\n'.join(article.footer())
    return
