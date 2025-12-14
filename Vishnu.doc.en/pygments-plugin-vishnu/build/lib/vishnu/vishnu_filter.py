"""A vishnu filter for Pygments."""

from pygments.filters import Filter # type: ignore
from pygments.token import Token # type: ignore

class VishnuFilter(Filter): # type: ignore

    def __repr__(self):
        return f"<{self.__class__.__name__}>" # type: ignore

    # This filter replaces all tabs with "<tab>".
    def filter(self, lexer, stream): # type: ignore
        for ttype, value in stream: # type: ignore
            parts = value.split("\t") # type: ignore
            yield ttype, "<tab>".join(parts) # type: ignore
