# -*- coding: utf-8 -*-
"""

    author_url directive
    ~~~~~~~~~~~~~~~~~~~~

    This adds a link to the author name in postmeta,
    use .. author_url:: http://site.com/ to specify the url,
    or use the default url from conf.py (.. author_url:: default)

      author_url = 'http://site.com/'

    :copyright: Copyright 2013 by Christian Jann
    :license: BSD

"""

from sphinx.util.compat import Directive

class AuthorUrlDirective(Directive):
    '''
    Author URL directive. The directive is not rendered, just stored in the
    metadata and passed to the templating engine.
    '''
    required_arguments = 0
    optional_arguments = 100
    has_content = False

    def run(self):
        '''
        Called when parsing the document.
        '''
        env = self.state.document.settings.env

        # store author in metadata
        author_url = " ".join(self.arguments)
        if author_url == "default":
            author_url = env.config.author_url
        env.blog_metadata[env.docname].author = "<a href='%s'>%s</a>" % \
            (author_url, env.blog_metadata[env.docname].author)

        return []

def setup(app):
    app.add_config_value("author_url", None, True)
    app.add_directive("author_url", AuthorUrlDirective)

