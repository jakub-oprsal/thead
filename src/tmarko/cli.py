""" Command line interface for tmarko """
import sys
import codecs
from . import tmarko

def main():
    filename = sys.argv[1]
    with codecs.open(filename, encoding="utf-8") as file:
        content = file.read()

    result = tmarko(content)
    print(result)
