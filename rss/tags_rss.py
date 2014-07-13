# -*- coding: utf-8 -*-
'''
    tags_rss
    ~~~~~~~~

    RSS feeds for tags.

    Based on tinkerer.ext.rss.

    :copyright: Copyright 2013 by Atamert Ölçgen
    :license: BSD license
'''
import os
import rss
from tinkerer import utils


def generate_feeds(app):
    env = app.builder.env
    categories = env.filing["categories"]

    for tag_name, posts in env.filing["tags"].items():
        app.info("Generating RSS feed for tag '%s'." % tag_name)
        name, context, template = rss.generate_feed(app, tag_name, posts)
        slug = utils.name_from_title(name)
        yield ("rss/tags/%s" % slug, context, template)


def on_html_collect_pages(app):
    '''
    Collect html pages and emit event
    '''
    for name, context, template in generate_feeds(app):
        yield (name, context, template)
        app.emit("rss-tag-page-generated", name)


def on_rss_tag_page_generated(app, name):
    src_file = "%s/%s.html" % (app.outdir, name)
    dest_file = "%s/%s.xml" % (app.outdir, name)
    app.info("Renaming: '%s' as '%s'." % (src_file, dest_file))
    os.rename(src_file, dest_file)


def setup(app):
    app.add_event("rss-tag-page-generated")
    app.connect("html-collect-pages", on_html_collect_pages)
    app.connect("rss-tag-page-generated", on_rss_tag_page_generated)
