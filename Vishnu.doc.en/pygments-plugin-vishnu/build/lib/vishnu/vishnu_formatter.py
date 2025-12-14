"""A vishnu plugin formatter for Pygments."""

from pygments.formatter import Formatter

class VishnuFormatter(Formatter): # type: ignore
    """
    Custom HTML formatter for CHM output:
    - inline <span style="color:#xxxxxx">
    - no classes, no CSS files, no JS
    - safe for CHM/IE-style rendering
    """
    # This should be the human-readable name of the format.
    name = "Pygments Plugin Vishnu Formatter"

    # This is a list of names that can be used to select the formatter.
    # In this plugin, we can call the pygmentize command as
    #
    #   pygmentize -f vishnu_formatter
    #
    # Also, doing
    #
    #   pygments.formatters.find_formatter_class("vishnu-formatter")
    #
    # in Python will find the formatter class.
    aliases = ["vishnu_formatter", "vishnu_Html_formatter"]

    # This is a list of file patterns that the formatter will
    # typically be used to produce. In this plugin, calling
    #
    #   pygmentize -o out.vfmt
    #
    # will automatically select this formatter based on the output
    # file name. Similarly,
    #
    #   pygments.formatters.get_formatter_for_filename("out.vfmt")
    #
    # will return an instance of this formatter class.
    filenames = ["*.vhtml"]

    def __init__(self, **options): # type: ignore
        super().__init__(**options) # type: ignore

    def __repr__(self):
        return f"<{self.__class__.__name__}>"

    def format_unencoded(self, tokensource, outfile): # type: ignore
        for ttype, value in tokensource: # type: ignore

            # Fallback: suche bis zum Eltern-Typ einen definierten Style
            while not self.style.styles_token(ttype):
                ttype = ttype.parent # type: ignore

            style = self.style.style_for_token(ttype)
            color = style.get("color")

            # HTML müssen wir escapen
            html = ( # type: ignore
                value.replace("&", "&amp;") # type: ignore
                     .replace("<", "&lt;")
                     .replace(">", "&gt;")
            )

            if color:
                outfile.write(f'<span style="color:#{color}">{html}</span>') # type: ignore
            else:
                outfile.write(html) # type: ignore

'''
    def format_unencoded(self, tokensource, out): # type: ignore
        # This formatter writes each token as [<color>]<string> .
        for ttype, value in tokensource: # type: ignore
            while not self.style.styles_token(ttype):
                ttype = ttype.parent # type: ignore
            color = self.style.style_for_token(ttype)['color']
            out.write("[" + (color or "black") + "]") # type: ignore
            out.write(value) # type: ignore
'''
