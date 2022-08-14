'''
Contains modules for supported LaTeX classes
'''
from .acmart import ACMart
from .amsart import AMSart
from .lipics import LIPIcs
from .siamart import SIAMart


def identify_class(cls):
    for Class in [ACMart, AMSart, LIPIcs, SIAMart]:
        if cls in Class.provides:
            return Class
    raise Exception(f"Unrecognised class '{cls}'!")


def ArticleCls(meta, recipe, args):
    Class = identify_class(args.cls)
    return Class(meta, recipe, args)
