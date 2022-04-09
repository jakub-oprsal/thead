import sys, codecs, yaml
import re
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
            metavar = "OPT",
            nargs = "+",
            help = "Options specific for a class",
            action = "extend",
            default = [])

    parser.add_argument(
            "--no-include",
            help = "Include '\input{...}' instead of including content.",
            dest = "include",
            action = "store_false")

    parser.add_argument(
            "--anonymous",
            help = "Set to anonymous mode for doubly blind reviews",
            action = "store_true")

    parsed_args = parser.parse_args(args)
    if parsed_args.out is None:
            m = re.match(r'(.*)\.[a-zA-Z]*', parsed_args.filename)
            parsed_args.out = f'{m.group(1)}.tex' if m else f'{parsed_args.filename}.tex'

    return parsed_args


if __name__ == '__main__':
    args = get_args(sys.argv[1:])

    with open(args.filename, 'r') as f:
        data = yaml.safe_load(f)

    content = dict()
    content['document'] = data['content']
    if 'appendix' in data:
        content['appendix'] = data['appendix']

    with codecs.open(args.out, mode='w', encoding='utf-8') as ofile:
        for chunk in parse(data, content, args):
            ofile.write(chunk)
