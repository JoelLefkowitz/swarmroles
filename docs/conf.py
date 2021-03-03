import re
import sys
import datetime
import pypandoc

sys.path.append("..")

"""
    Sphinx core settings
"""
project = "swarmroles"
version = "1.4.0"
author = "Joel Lefkowitz"

master_doc = "index"

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "venv"]

extensions = [
    "sphinx.ext.autodoc",
    "sphinx_autodoc_annotation",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinxcontrib.apidoc",
]

"""
    Sphinx autodoc settings
    -> Declares apidoc_module_dir if defined
"""
autodoc_typehints = "description"
typehints_fully_qualified = True
autodoc_default_flags = ["members", "undoc-members"]
napoleon_google_docstring = True

"""
    Yummy sphinx theme settings
"""
html_theme = "yummy_sphinx_theme"
html_title = "Swarmroles"

static_dir = "static"

html_favicon = "static/favicon.ico"
html_css_files = "static/styles.css"

html_add_permalinks = ""
html_theme_options = {
    "navbar_icon": "spin fa-book",
    "github_url": "JoelLefkowitz/swarmroles"
}

"""
    Runtime work
    -> Generates a copyright for this year
    -> Converts the project readme to HTML
"""
copyright = f"{datetime.datetime.now().year} {author}"

with open("../README.md", "r") as stream:
    html = re.sub(
        "<h1.*>.*?</h1>",
        "",
        pypandoc.convert(stream.read(), "html", format="md"),
        flags=re.DOTALL
    )

with open("README.html", "w") as stream:
    stream.write(html)
