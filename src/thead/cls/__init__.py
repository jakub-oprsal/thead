'''
Contains modules for supported LaTeX classes
'''
from .article import Article
from .acmart import ACMart
from .amsart import AMSart
from .lipics import LIPIcs
from .siamart import SIAMart
from .ieeetran import IEEEtran


def identify_class(cls):
    for Class in [Article,
                  ACMart,
                  AMSart,
                  LIPIcs,
                  SIAMart,
                  IEEEtran]:
        if cls in Class.provides:
            return Class
    raise Exception(f"Unrecognised class '{cls}'!")


def ArticleCls(meta, recipe, args):
    Class = identify_class(args.cls)
    return Class(meta, recipe, args)
