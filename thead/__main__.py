import sys, codecs, yaml, re
from itertools import chain
from argparse import ArgumentParser
from .parse import parse
from .recipe import Recipe


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
            "--header-include",
            dest = "header",
            help = "TeX file(s) to be included in the header",
            action = "append",
            default = [])

    parser.add_argument(
            "--content",
            help = "Content of the document",
            action = "append",
            default = [])

    parser.add_argument(
            "--appendix",
            help = "Appendix",
            action = "append",
            default = [])

    parser.add_argument(
            "--bib",
            help = "Additional bibliography source",
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


if __name__ == '__main__':
    args = get_args(sys.argv[1:])

    with open(args.filename, 'r') as f:
        data = yaml.safe_load(f)

    recipe = Recipe()
    recipe.discover()

    with codecs.open(args.out, mode='w', encoding='utf-8') as ofile:
        for chunk in parse(data, recipe, args):
            ofile.write(chunk)

    print(f'Output written to {args.out}.')
