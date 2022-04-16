import re, os, yaml


class Recipe:
    def __init__(self, header=[], content=[], appendix=[], bib=[]):
        self.header = list(header)
        self.content = list(content)
        self.appendix = list(appendix)
        self.bib = list(bib)

    def discover(self, path='.'):
        ''' Discovers files with the content of the document. '''
        for direntry in os.scandir(path):
            try:
                fmatch = re.match(r'(.+)\.(tex|bib)', direntry.name)
                if not direntry.is_file() or not fmatch:
                    continue
            except OSError:
                continue

            name, ftype = fmatch.group(1), fmatch.group(2)
            if ftype == 'bib':
                self.bib.append(name)
            elif ftype == 'tex':
                if name == 'macro':
                    self.header.append('macro')
                elif re.match(r'(content|[0-9]+[_-])', name):
                    self.content.append(name)
                elif re.match(r'(appendix|[A-Z]+[_-])', name):
                    self.appendix.append(name)

        if 'content' in self.content:
            self.content = ['content']
        else:
            self.content.sort()
        if 'appendix' in self.appendix:
            self.appendix = ['appendix']
        else:
            self.appendix.sort()

    def read(self, yamlfile):
        ''' Reads a recipe from a yaml file. '''

        with open(yamlfile, 'r') as f:
            data = yaml.safe_load(f)

        def rm_ext(fname):
            m = re.match(r'(.*)\.bib')
            return m.group(1) if m else fname

        if 'header' in data:
            self.header = data['header']
        if 'content' in data:
            self.content = data['content']
        if 'appendix' in data:
            self.appendix = data['appendix']
        if 'bib' in data:
            self.bib = list(map(rm_ext, data['bib']))

    def __add__(self, other):
        if type(self) != type(other):
            raise TypeError
        self.header += other.header
        self.content += other.content
        self.appendix += other.appendix
        self.bib += other.bib
