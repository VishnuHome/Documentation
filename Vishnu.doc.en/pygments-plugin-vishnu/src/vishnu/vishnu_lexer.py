"""
A vishnu plugin lexer for Pygments.
The lexer is responsible for the recognition of here adressed tokens
in the input-file.
"""

from pygments.lexer import RegexLexer
from pygments.token import Comment, Number, Name, Operator, Keyword

class VishnuLexer(RegexLexer):
    # Human-readable name of the lexer.
    # doing
    #   pygments.lexers.find_lexer_class("Pygments Plugin Vishnu Lexer")
    # will return the VishnuLexer class.
    name = "Pygments Plugin Vishnu Lexer"

    # This is a list of names that can be used to select the language.
    # In this example, we can call the pygmentize command as
    #
    #   pygmentize -l vishnu_lexer
    #
    # Also, doing
    #
    #   pygments.lexers.find_lexer_class_by_name("vishnu_lexer")
    #
    # in Python will find the lexer class. This is what many documentation or
    # site generation tools implicitly do with code blocks, e.g., this in Sphinx
    # reST:
    #
    #   .. code-block:: vishnu_lexer
    #
    #      your code here
    #
    # or this in Markdown:
    #
    #   ```vishnu_lexer
    #   your code here
    #   ```
    #
    aliases = ["vishnu_lexer"]

    # This is a list of file patterns that will automatically be highlighted
    # with this lexer. In this example, calling
    #
    #   pygmentize file.xml or file.json
    #
    # will automatically highlight file.xml or file.json with this lexer, without needing
    # to pass `-l vishnu_lexer`. Similarly,
    #
    #   pygments.lexers.find_lexer_class_for_filename("file.xml") or
    #   pygments.lexers.find_lexer_class_for_filename("file.json")
    #
    # will return the VishnuLexer class.
    filenames = ["*.xml", "*.json"]

    # This is a list of MIME types for the language. In this example,
    #
    #   pygments.lexers.get_lexer_for_mimetype("text/x-exmpl")
    #
    # will return the VishnuLexer class.
    mimetypes = ["text/x-exmpl"]

#     tokens = {
#         'root': [
#             (r'\b(CanRunDllPath|Checker|Checkers|ConstantNodeUserControlPath|\
# Format|IsGlobal|IsMirror|Job|JobConnectorUserControlPath|JobLogger|\
# JobListUserControlPath|JobSnapshotTrigger|JobTrigger|LockName|\
# Logger|Loggers|LogicalExpression|LogicalName|NodeListUserControlPath|\
# Parameters|PhysicalPath|Reference|SingleNodeUserControlPath|Snapshot|\
# Snapshots|SnapshotUserControlPath|StartCollapsed|SubJob|SubJobs|\
# SubWorker|SubWorkers|ThreadLocked|Trigger|Triggers|Type|\
# UserControlPath|ValueModifier|ValueModifiers|Worker|Workers)\b', Keyword.Reserved),
#             (r'\b(def|class|if|else|return|import|for|while|in|and|or|not|true|false)\b', Keyword),
#             (r'\b\d+\b', Number),
#             (r'[a-zA-Z0-9_]*', Name),
#             (r'(?<=<)\w+', Name.Tag),  # Lookbehind: nur \w+ nach
#             (r'[=+\-*/\{\}]', Operator),
#             (r'<!--.*?-->', Comment),
#             (r'".*?"', String),
#             (r'\s+', Text),
#         ]
#     }

    # last ok:
    tokens = {
        'root': [
            (r'<!--.*?-->', Comment),
            (r'<\?.*?\?>', Comment),
            (r'[=+\-*\{\}]', Operator),
            (r'\/(?!\>)]', Operator),
            (r'[\<\>]', Operator),
            (r'\b\d+\b', Number),
            (r'\b(Checker|JobDescription|Job|Logger|Snapshot|SubJob|SubWorker|Trigger|ValueModifier|Worker)\b', Keyword.Reserved),
            (r'\b(true|false)\b', Keyword),
            (r'(?<=<)\w+', Name.Tag),
            (r'(?<=\/)\w+', Name.Tag),
            (r'(\w+)(?=\"*:)', Name.Tag),  # Lookbehind: only \w+ followed by 
            (r'[a-zA-Z0-9_]+', Name), # this must occur, otherwise pygments masks each individual letter
            # not working, but destroying former results:
            # (r'".+?"', String),
            # (r'.*\n', Text),
        ]
    }

    def __repr__(self):
        return f"<{self.__class__.__name__}>"
