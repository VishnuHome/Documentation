# Pygments plugin for Vishnu

This repository contains a plugin lexer/formatter/style/filter for Vishnu
for the [Pygments](https://pygments.org) syntax highlighter.

Roadmap:

```
.
├── src
│    └── vishnu
│         ├── vishnu_filter.py    # A vishnu filter
│         ├── vishnu_formatter.py # A vishnu formatter
│         ├── vishnu_lexer.py     # A vishnu lexer
│         └── vishnu_style.py     # A vishnu style
├── pyproject.toml      # The Python package metadata file
├── README.md           # You are here
├── CheckAll_JobDescription.xml  # Test files
└── CheckAll_JobDescription.json # for the vishnu lexer
```

To be usable, plugins must be installed. If you are running the `pygmentize`
command, you probably want to use a
[virtual environment](https://docs.python.org/3/library/venv.html)
to avoid installing packages globally. For vishnu, here is how to create
a virtual environment and install this set of plugins into it:

```
python -m venv myvenv/
myvenv/Scripts/pip install . # install the project in current directory into the virtual environment
# myvenv/Scripts/pygmentize ... # use the pygmentize command from the virtual environment

To test the installation use:
python -c "import vishnu; print('OK')"

python -c "from pygments.lexers import get_lexer_by_name; print(get_lexer_by_name('vishnu_lexer'))"
python -c "from pygments.formatters import get_formatter_by_name; print(get_formatter_by_name('vishnu_formatter'))"
python -c "from pygments.styles import get_style_by_name; print(get_style_by_name('vishnu_style'))"
python -c "from pygments.filters import get_filter_by_name; print(get_filter_by_name('vishnu_filter'))"

pygmentize -l vishnu_lexer -O style=vishnu_style -f vishnu_formatter CheckAll_JobDescription.xml
pygmentize -L styles | Select-String Vishnu

To build the package use:
pip install build
python -m build

```

If you are using Pygments from Python, possibly through a tool like Sphinx,
mkdocs, etc., then you just need to install the plugin in the same environment
as the one where you installed Pygments.

If you want to distribute your plugin on PyPI, you should read the
[packaging user guide](https://packaging.python.org/en/latest/tutorials/packaging-projects).

#### License for the originally used template and the Vishnu plugin

There isn't much copyrightable content here, but if you are worried about reuse:

Template: Copyright (C) 2023 by Jean Abou Samra <jean@abou-samra.fr>
Vishnu: Copyright (C) 2025 by Erik Nagel <erik@reallyhuman.net>

Permission to use, copy, modify, and/or distribute this software for any purpose
with or without fee is hereby granted.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF
THIS SOFTWARE.
