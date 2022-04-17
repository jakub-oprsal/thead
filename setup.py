#!/usr/bin/env python3
from setuptools import setup

setup(
        name = 'thead',
        version = '0.0.3-alpha-4',
        description = 'Tools for generating LaTeX files from metadata',
        author = 'Jakub Opršal',
        author_email = 'jakub.oprsal@cs.ox.ac.uk',
        url = 'https://github.com/jakub-oprsal/thead',
        license = 'MIT',
        packages = ['thead', 'thead/cls'],
)
