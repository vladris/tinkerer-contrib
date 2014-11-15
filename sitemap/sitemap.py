"""
Sitemap

Sitemap generation extension for Tinkerer.

:copyright: Copyright (c) 2014 Julien Lamy
:license: BSD

"""
import os
import xml.etree.ElementTree

namespace = "http://www.sitemaps.org/schemas/sitemap/0.9"

def setup(app):
    app.connect("build-finished", generate_sitemap)

def generate_sitemap(app, exception):
    if exception:
        return

    urls = []

    env = app.builder.env
    for page in env.blog_posts+env.blog_pages:
        url = {}
        url["loc"] = "{}{}.html".format(app.config.website, page)

        lastmod = env.blog_metadata[page].date
        if lastmod:
            url["lastmod"] = lastmod.isoformat()[:10]

        urls.append(url)

    urlset = xml.etree.ElementTree.Element("urlset", {"xmlns": namespace})
    for url in urls:
        url_element = xml.etree.ElementTree.SubElement(urlset, "url")

        loc = xml.etree.ElementTree.SubElement(url_element, "loc")
        loc.text = url["loc"]

        if "lastmod" in url:
            lastmod = xml.etree.ElementTree.SubElement(url_element, "lastmod")
            lastmod.text = url["lastmod"]


    tree = xml.etree.ElementTree.ElementTree(urlset)
    tree.write(os.path.join(app.outdir, "sitemap.xml"), "UTF-8", True)

