from datetime import datetime
from .cls import cls_module
from .cls.common import include, render_command

COMMENT = '''% Generated by `thead.py` <https://github.com/jakub-oprsal/thead>
% on {now}
'''

def parse(meta, content, args):
    """ parses metadata, creates headers, content, and footer, and yields
        these to be written into a file consecutively """

    clsmodule = cls_module(args.cls)

    ## HEADER
    yield COMMENT.format(now = datetime.now())
    yield clsmodule.header(
            meta,
            anonymous=args.anonymous,
            classoptions=args.opts)

    ## BODY
    include = include if args.include else \
            lambda fn, end: render_command('input', fn) + end
    for filename in content['document']:
        yield include(filename, '\n')
    if 'appendix' in content:
        body += '\n\\appendix\n\n'
        for filename in content['appendix']:
            yield include(filename, '\n')

    ## FOOTER
    yield clsmodule.footer(meta)
    return
