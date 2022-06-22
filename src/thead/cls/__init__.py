'''
Contains modules for supported LaTeX classes
'''
from .acmart import Acmart


def IdentifyClass(cls):
    for Class in [Acmart]:
        if cls in Class.provides:
            return Class
    raise Exception(f"Unrecognised class '{cls}'!")

