"""SpaLiFT documentation; no model installation or training during builds."""
project = "SpaLiFT"
author = "SpaLiFT contributors"
release = "0.1.0"
version = release
language = "en"
root_doc = "index"
extensions = ["myst_parser", "sphinx_rtd_theme", "sphinx_copybutton", "sphinx.ext.githubpages"]
source_suffix = {".rst": "restructuredtext", ".md": "markdown"}
exclude_patterns = ["_downloads/**"]
myst_enable_extensions = ["colon_fence", "deflist"]
myst_heading_anchors = 4
nitpicky = True
html_theme = "sphinx_rtd_theme"
html_title = "SpaLiFT documentation"
html_short_title = "SpaLiFT"
html_favicon = "_static/favicon.svg"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_js_files = ["navigation.js"]
html_theme_options = {
    "navigation_depth": 3, "collapse_navigation": False,
    "sticky_navigation": True, "style_external_links": False,
    "prev_next_buttons_location": "bottom",
}
html_show_copyright = False
html_show_sphinx = True
html_context = {
    "display_github": True, "github_user": "bxslalala",
    "github_repo": "SpaLiFT-Tutorial", "github_version": "main",
    "conf_py_path": "/docs/source/",
}
html_baseurl = "https://bxslalala.github.io/SpaLiFT-Tutorial/"
copybutton_prompt_text = r">>> |\.\.\. |\$ "
copybutton_prompt_is_regexp = True
copybutton_remove_prompts = True
copybutton_only_copy_prompt_lines = False
