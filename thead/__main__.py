import sys, os, codecs, yaml
import re
from itertools import chain
from argparse import ArgumentParser
from .parse import parse


def get_args(args):
    parser = ArgumentParser(prog="python3 -m thead")

    parser.add_argument(
            "-c",
            "--cls",
            help = "Specify the output class of the document",
            required = True)

    parser.add_argument(
            "--cname",
            help = "Use class name CNAME instead of the default for the "
                   "class.",
            default = None)

    parser.add_argument(
            "-o",
            "--out",
            metavar = "OUTFILE",
            help = "Output file",
            default = None)

    parser.add_argument(
            "filename",
            help = "The metadata yaml file")

    parser.add_argument(
            "--opts",
            help = "Options specific for a class, comma separated",
            action = "append",
            default = [])

    parser.add_argument(
            "--no-include",
            help = "Use '\input{...}' instead of including files.",
            dest = "include",
            action = "store_false")

    parser.add_argument(
            "--anonymous",
            help = "Set to anonymous mode for doubly blind reviews",
            action = "store_true")

    pargs = parser.parse_args(args)
    if pargs.out is None:
        m = re.match(r'(.*)\.[a-zA-Z]*', pargs.filename)
        pargs.out = f'{m.group(1)}.tex' if m else f'{pargs.filename}.tex'
    pargs.opts = list(chain(*(opt.split(',') for opt in pargs.opts)))

    return pargs


class Recipe:
    def __init__(self, header, content, appendix, bib):
        self.header = header
        self.content = content
        self.appendix = appendix
        self.bib = bib


def discover_recipe(path='.'):
    ''' Discovers files with the content of the document. '''
    content, appendix, bib, header = ([] for _ in range(4))
    for direntry in os.scandir(path):
        try:
            fmatch = re.match(r'(.+)\.(tex|bib)', direntry.name)
            if not direntry.is_file() or not fmatch:
                continue
        except OSError:
            continue

        name, ftype = fmatch.group(1), fmatch.group(2)
        if ftype == 'bib':
            bib.append(name)
        elif ftype == 'tex':
            if name == 'macro':
                header.append('macro')
            elif re.match(r'(content|[0-9]+[_-])', name):
                content.append(name)
            elif re.match(r'(appendix|[A-Z]+[_-])', name):
                appendix.append(name)

    if 'content' in content:
        content = ['content']
    else:
        content.sort()
    if 'appendix' in appendix:
        appendix = ['appendix']
    else:
        appendix.sort()
    return Recipe(header, content, appendix, bib)


def read_recipe(yaml):
    ''' Reads recipe from a yaml file. '''
    pass


if __name__ == '__main__':
    args = get_args(sys.argv[1:])

    with open(args.filename, 'r') as f:
        data = yaml.safe_load(f)

    recipe = discover_recipe()

    with codecs.open(args.out, mode='w', encoding='utf-8') as ofile:
        for chunk in parse(data, recipe, args):
            ofile.write(chunk)

    print(f'Output written to {args.out}.')
