import sys, codecs, yaml, re
from itertools import chain
from argparse import ArgumentParser
from .parse import parse
from .recipe import Recipe


def get_args(args):
    parser = ArgumentParser(prog="thead")

    parser.add_argument(
            "-c",
            "--cls",
            help = "Specify the target class of the document "
                   "(more precisely the class driver)",
            required = True)

    parser.add_argument(
            "--cname",
            help = "Use class name CNAME instead of the default for the "
                   "class driver",
            default = None)

    parser.add_argument(
            "-o",
            "--out",
            metavar = "OUTFILE",
            help = "Output file",
            default = None)

    parser.add_argument(
            "filename",
            help = "The input metadata yaml file")

    parser.add_argument(
            "--opts",
            help = "Options specific for a class, comma separated",
            action = "append",
            default = [])

    parser.add_argument(
            "--header-file",
            metavar = "macro.tex",
            dest = "header",
            help = "TeX file(s) to be included in the header",
            action = "append",
            default = [])

    parser.add_argument(
            "--content",
            help = "TeX file(s) with the content of the document",
            action = "append",
            default = [])

    parser.add_argument(
            "--appendix",
            help = "TeX file(s) with the appendix",
            action = "append",
            default = [])

    parser.add_argument(
            "--bib",
            help = "Additional bibliography source",
            action = "append",
            default = [])

    parser.add_argument(
            "--recipe",
            help = "Recipe in a yaml file",
            default = None)

    parser.add_argument(
            "--include",
            help = "Include the content of files instead of \\input.",
            dest = "include",
            action = "store_true")

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


def main():
    args = get_args(sys.argv[1:])

    with open(args.filename, 'r') as f:
        data = yaml.safe_load(f)

    if args.recipe is not None:
        recipe = Recipe.read(args.recipe)
    else:
        recipe = Recipe(args.header, args.content, args.appendix, args.bib)
        if not recipe.content:
            recipe = Recipe.discover() + recipe

    with codecs.open(args.out, mode='w', encoding='utf-8') as ofile:
        for chunk in parse(data, recipe, args):
            ofile.write(chunk)

    print(f'Output written to {args.out}.')
