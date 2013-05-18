'''
    jinjafilters
    ~~~~~~~~~~~

    Adds extra jinja filters to the HTML builder.

    Example:

      {{ "This is a title"|cleanurl }}

      will be replaced with this_is_a_title

    For Vlad:

      http://comments.gmane.org/gmane.comp.python.sphinx.devel/6137
      This could be an alternative to:
      catlinks = sorted([(c, name_from_title(c)) for c in env.filing["categories"]])
      We could just use {{ category|cleanurl }} instead of {{ catlinks[category]) }}

    :copyright: Copyright 2013 by Christian Jann
    :license: FreeBSD, see LICENSE file
'''

from tinkerer.utils import name_from_title

def add_jinja_filters(app):
    app.builder.templates.environment.filters['cleanurl'] = name_from_title

def setup(app):
    '''
    Adds extra jinja filters.
    '''
    app.connect("builder-inited", add_jinja_filters)
