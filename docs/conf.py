# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import circuitpython_mocks.board

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "CircuitPython-mocks"
copyright = "2024, Brendan Doherty"
author = "Brendan Doherty"
release = "0.1.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx_immaterial",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx_jinja",
]

# autodoc_class_signature = "separated"
autodoc_default_options = {
    "exclude-members": "__new__",
}

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

jinja_contexts = {
    "board": {
        "pins": [
            x
            for x in dir(circuitpython_mocks.board)
            if not x.startswith("_") and x not in ("Pin", "board_id")
        ]
    }
}
intersphinx_mapping = {
    "circuitpython": ("https://circuitpython.readthedocs.io/en/latest/", None),
    "python": ("https://docs.python.org/3/", None),
    "pytest": ("https://docs.pytest.org/en/latest/", None),
}

default_role = "any"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_immaterial"
html_static_path = ["_static"]
html_favicon = "_static/favicon.ico"
html_title = "CircuitPython-mocks"

html_theme_options = {
    "site_url": "https://circuitpython-mocks.readthedocs.io",
    "repo_url": "https://github.com/2bndy5/CircuitPython-mocks",
    "icon": {
        "repo": "fontawesome/brands/github",
        "edit": "material/file-edit-outline",
        "logo": "material/code-tags-check",
    },
    "features": [
        "navigation.top",
        "search.share",
        "toc.follow",
    ],
    "palette": [
        {
            "media": "(prefers-color-scheme: light)",
            "scheme": "default",
            "primary": "deep-purple",
            "accent": "cyan",
            "toggle": {
                "icon": "material/toggle-switch-off-outline",
                "name": "Switch to dark mode",
            },
        },
        {
            "media": "(prefers-color-scheme: dark)",
            "scheme": "slate",
            "primary": "deep-purple",
            "accent": "cyan",
            "toggle": {
                "icon": "material/toggle-switch",
                "name": "Switch to light mode",
            },
        },
    ],
}
