from . import amsart, acmart, lipics

CLS_MODULES = {
        'amsart': amsart,
        'acmart': acmart,
        'lipics': lipics,
        }

def cls_module(cls):
    if cls not in CLS_MODULES:
        raise Exception(f"Unrecognised class '{cls}'!")
    return CLS_MODULES[cls]
