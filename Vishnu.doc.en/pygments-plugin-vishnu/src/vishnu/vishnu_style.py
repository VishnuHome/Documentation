"""
    pygments.styles.vishnu_style
    ~~~~~~~~~~~~~~~~~~~~~

    Style designed for `Vishnu`.

    :copyright: Copyright 2006-2025 by the Pygments team, see AUTHORS
    :and overwritten by Erik Nagel, https://vishnuhome.github.io/Vishnu/en/
    :license: BSD, see LICENSE for details.
"""

from pygments.style import Style, StyleMeta
from pygments.token import Keyword, Name, Comment, String, Error, \
     Number, Operator, Literal

# __all__ = ['VishnuStyle']

class VishnuStyleMeta(StyleMeta):
    def __repr__(cls):
        return f"<{cls.__name__}>"

class VishnuStyle(Style, metaclass=VishnuStyleMeta):
    """
    Style designed for `Vishnu`.
    """

    name = 'vishnu'
    
    styles = {
        Comment:                "#1F5C10",
        Comment.Preproc:        "#933705",

        String:                 "#1192E9",
        String.Char:            '#C41A16',

        Operator:               "#5C3CFF",

        Keyword:                "#2744B8",
        Keyword.Reserved:       "bold #BE5D1D",

        Name:                   "#000000",
        Name.Attribute:         '#836C28',
        Name.Class:             "#468690",
        Name.Function:          "#18B9B1",
        Name.Builtin:           '#A90D91',
        # In Obj-C code this token is used to colour Cocoa types
        Name.Builtin.Pseudo:    "#8548D0",
        Name.Variable:          "#059C64",
        Name.Tag:               "#BE5D1D",
        Name.Decorator:         "#3F61EB",
        # Workaround for a BUG here: lexer treats multiline method signatres as labels
        Name.Label:             "#499C0A",

        Literal:                "#6B57F0",
        Number:                 '#1C01CE',
        Error:                  "#000000", # everything, that's not found
    }
