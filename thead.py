import sys, codecs, yaml
import re
import acmart, lipics, amsart
from datetime import datetime
from common import *

def read_args(*args):
    """Usage: make [-c CLASS] [-o OUTFILE] FILENAME"""
    cls, filename, outfile = None, None, None
    include = True

    argi = iter(args)
    for arg in argi:
        if arg == '-c' and cls is None:
            cls = next(argi)
        elif arg == '-o' and outfile is None:
            outfile = next(argi)
        elif arg == '--no-include':
            include = False
        elif re.match(r'[^-].*', arg) and filename is None:
            filename = arg
        else:
            raise Exception(f"Invalid argument '{arg}'")

    if filename is None:
        raise Exception("No input filename!")
    elif outfile is None:
        m = re.match(r'(.*)\.[a-zA-Z]*', filename)
        if m:
            outfile = m.group(1) + '.tex'
        else:
            outfile = filename + '.tex'

    return cls, filename, outfile, include


def main():
    cls, filename, outfile, include = read_args(*sys.argv[1:])

    with open(filename, 'r') as yfile:
        data = yaml.safe_load(yfile)

    if cls == 'acmart':
        header = acmart.header(data)
        footer = acmart.footer(data)
    elif cls == 'lipics':
        header = lipics.header(data)
        footer = lipics.footer(data)
    elif cls == 'amsart':
        header = amsart.header(data)
        footer = amsart.footer(data)
    else:
        raise Exception(f"Unrecongnised class '{cls}'")

    ## make the body of the document
    body = ''

    if include == True:
        add_file = lambda fname: "\n\n" + include_file(fname)
    else:
        add_file = lambda fname: render_command('input', fname)
    
    for filename in data['content']:
        body += add_file(filename)
    
    if 'appendix' in data:
        body += '\\appendix\n'
        for filename in data['appendix']:
            body += add_file(filename)

    ## ship the results
    now = datetime.now()

    with codecs.open(outfile, mode='w', encoding='utf-8') as ofile:
        ofile.write(f'% Generated on {now}\n')
        ofile.write(header)
        ofile.write(body)
        ofile.write(footer)

if __name__ == '__main__':
    main()
