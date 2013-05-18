# -*- coding: utf-8 -*-
"""

    author_url extension
    ~~~~~~~~~~~~~~~~~~~~

    This adds a link to every author name in postmeta.

    :copyright: Copyright 2013 by Vlad Riscutia
    :license: BSD

"""

def author_url(app, pagename, teplatename, context, doctree):
    metadata = context["metadata"]

    if not metadata.is_post:
        return

    metadata.author = "<a href='%s'>%s</a>" % (app.config.author_url, metadata.author)

def setup(app):
    app.add_config_value("author_url", None, True)

    app.connect("html-page-context", author_url)
