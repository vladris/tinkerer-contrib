"""An extension which pack css files, typed in blog config into
single 'all.css' file
"""

import os


def compressassets_extension(app, exception):
    "Wrapped up as a Sphinx Extension"

    if app.builder.name not in ("html", "dirhtml"):
        return

    static = os.path.join(app.srcdir, 'blog', 'html', '_static')
    if not os.path.isdir(static):
        print("ERROR: compressassetes static dir '%s' not exists" % static)
        return

    files = app.config.assets_css
    if files:
        files = " ".join([os.path.join(static, f) for f in files])
        o = os.system("cat {0} > {1}".format(files,
                                             os.path.join(static, 'all.css')))
        if o:
            print("ERROR: compressassets can't pack css files, \
return code: %d" % o)
        else:
            print("packing css files to single all.css")
    else:
        print("WARNING: no 'assets_css' conf value specified")


def setup(app):
    "Setup function for Sphinx Extension"
    app.add_config_value("assets_css", [], 'List of css files to pack')
    app.connect("build-finished", compressassets_extension)
