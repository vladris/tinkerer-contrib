# -*- coding: utf-8 -*-
'''
    rss
    ~~~

    A more generic version of tinkerer.ext.rss.generate_feed. Used by
    categories_rss & tags_rss.

    :copyright: Copyright 2013 by Atamert Ölçgen
    :license: BSD license
'''
import email.utils
import time
from tinkerer.ext import patch


def generate_feed(app, feed_name, posts):
    '''
    Generates RSS feed.
    '''
    env = app.builder.env

    context = {
        "items": []
    }

    for post in posts:
        metadata = env.blog_metadata[post]

        link = "%s%s.html" % (app.config.website, post)

        timestamp = email.utils.formatdate(
                        time.mktime(metadata.date.timetuple()), localtime=True)

        categories = [category[1] for category in metadata.filing["categories"]]

        context["items"].append({
            "title": env.titles[post].astext(),
            "link": link,
            "description": patch.strip_xml_declaration(patch.patch_links(
                metadata.body,
                app.config.website + post[:11], # first 11 characters is path (YYYY/MM/DD/)
                post[11:], # following characters represent filename
                replace_read_more_link=not app.config.rss_generate_full_posts)),
            "categories": categories,
            "pubDate": timestamp
        })

    # feed metadata
    context["title"] = "%s - %s" % (app.config.project, feed_name)
    context["link"] = app.config.website
    context["tagline"] = app.config.tagline
    context["language"] = "en-us"

    # feed pubDate is equal to latest post pubDate
    context["pubDate"] = context["items"][0]["pubDate"]

    return (feed_name, context, "rss.html")
