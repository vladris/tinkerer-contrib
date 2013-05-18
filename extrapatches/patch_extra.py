'''
    patch_extra
    ~~~~~~~~~~~

    Additional Tinkerer patches for nicer HTML output.

    :copyright: Copyright 2013 by Christian Jann
    :license: FreeBSD, see LICENSE file
'''

import xml.dom.minidom
from tinkerer.ext.patch import convert, strip_xml_declaration

def patch_collected_context_extra(app, name, template, context):
  if template == "aggregated.html":
    for metadata in context["posts"]:
        metadata.body = patch_links_extra(
            metadata.body,
            metadata.link[:11], # first 11 characters is path (YYYY/MM/DD/)
            metadata.link[11:]) # following characters represent filename
        metadata.body = strip_xml_declaration(metadata.body)

def patch_links_extra(body, docpath, docname):
    '''
    Recursively patches links in nodes.
    '''

    in_str = convert(body).encode("utf-8")
    doc = xml.dom.minidom.parseString(in_str)
    patch_node_extra(doc, docpath, docname)
    body = doc.toxml()

    return body

def patch_node_extra(node, docpath, docname):
    '''
    Recursively patches links in nodes.
    '''
    node_name = node.localName

    # if node is hyperlink
    if node_name == "a":
        # http://validator.w3.org
        # Error:  Duplicate ID id1, id2, ...
        ref_id = node.getAttributeNode("id")
        if ref_id != None:
            ref_id.value = ref_id.value + '_' + docname
    elif node_name == "div":
        # Duplicate ID overview.
        # <div class="contents local topic" id="overview">
        node_class = node.getAttributeNode("class")
        if node_class != None:
            if (node_class.value.startswith("contents") or
            node_class.value == "section"):
                node_id = node.getAttributeNode("id")
                node_id.value = node_id.value + '_' + docname

    # recurse
    for node in node.childNodes:
        patch_node_extra(node, docpath, docname)

def setup(app):
    '''
    Sets up node patch handler.
    '''
    # connect event
    app.connect("html-collected-context", patch_collected_context_extra)

