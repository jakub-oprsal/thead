import re, os, yaml


class Recipe:
    def __init__(self, header=[], content=[], appendix=[], bib=[]):
        self.header = list(header)
        self.content = list(content)
        self.appendix = list(appendix)
        self.bib = list(bib)

    @classmethod
    def discover(cls, path="."):
        """Discovers files with the content of the document."""
        header, content, appendix, bib = ([] for _ in range(4))
        for direntry in os.scandir(path):
            try:
                fmatch = re.match(r"(.+)\.(tex|bib)", direntry.name)
                if not direntry.is_file() or not fmatch:
                    continue
            except OSError:
                continue

            name, ftype = fmatch.group(1), fmatch.group(2)
            if ftype == "bib":
                bib.append(name)
            elif ftype == "tex":
                if name == "macro":
                    header.append("macro")
                elif re.match(r"(content|[0-9]+[_-])", name):
                    content.append(name)
                elif re.match(r"(appendix|[A-Z]+[_-])", name):
                    appendix.append(name)

        if "content" in content:
            content = ["content"]
        else:
            content.sort()
        if "appendix" in appendix:
            appendix = ["appendix"]
        else:
            appendix.sort()

        return cls(header, content, appendix, bib)

    @classmethod
    def read(cls, yamlfile):
        """Reads a recipe from a yaml file."""
        with open(yamlfile, "r") as f:
            data = yaml.safe_load(f)
        return cls(
            data.get("header", []),
            data.get("content", []),
            data.get("appendix", []),
            data.get("bib", []),
        )

    def __add__(self, other):
        if type(self) != type(other):
            raise TypeError
        self.header += other.header
        self.content += other.content
        self.appendix += other.appendix
        self.bib += other.bib

        return self
