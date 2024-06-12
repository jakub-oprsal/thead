from .amsart import AMSart
from ..tex import render_command


class SNKart(AMSart):
    provides = ["snkart"]

    def setup(self):
        if self.cname is None:
            self.cname = "snkart"

        if self.bibstyle is None:
            self.bibstyle = "alphaurl"

        self.headers += [
            self.macro,
            self.render_pdfmeta,
            self.begin_document,
            self.render_title,
            self.render_authors,
            self.render_funding,
            self.render_abstract,
            self.render_keywords,
            self.maketitle,
            self.render_acknowledgements,
        ]
