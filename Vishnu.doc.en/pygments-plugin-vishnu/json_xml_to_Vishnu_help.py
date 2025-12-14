# json_xml_to_Vishnu_help.py
from pygments import highlight # type: ignore
from pygments import filters # type: ignore
from pygments.filters import VisibleWhitespaceFilter # type: ignore
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments.styles import get_all_styles
import os
import sys

def work_on_file(input_path: str) -> str:

    # Dateiinhalt lesen
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            data = f.read()
    except FileNotFoundError:
        sys.exit(f"Datei nicht gefunden: {input_path}")

    # Formatter mit Inline-Stilen und korrektem Whitespace
    formatter = HtmlFormatter( # type: ignore
        style='vishnu_style',
        noclasses=True,    # alle Styles inline
        # wrapcode=True,     # erhält Zeilen & Einrückungen
        linenos=False     # optional: True für Zeilennummern
    )
    # Highlighting durchführen
    # html_code: str = highlight(data, lexer, formatter) # type: ignore
    html_code: str = highlight(data, lexer, formatter) # type: ignore

    return html_code.rstrip()

if __name__ == "__main__":
  print(list(get_all_styles())) # type: ignore

  lexer = get_lexer_by_name("vishnu_lexer")
  lexer.add_filter(VisibleWhitespaceFilter(tabs=' ', tabsize=2)) # type: ignore

  # Eingabe- und Ausgabedatei (anpassen oder per Argument übergeben)
  input_path_xml = "NamedTriggerLogger.xml"
  input_path_json = "NamedTriggerLogger.json"
  output_path = os.path.splitext(input_path_xml)[0] + ".html"

  xml_content = work_on_file(input_path_xml)
  json_content = work_on_file(input_path_json)

  html_full = f"""<markup>
  <div id="IDBSection" class="collapsibleSection">
    <div id="IDAB" class="codeSnippetContainer">
      <div class="codeSnippetContainerTabs">
        <div id="IDAB_tab1" class="codeSnippetContainerTab">
          <a href="#" onclick="ChangeTab('IDAB','cs','1','2');return false;">XML</a>
        </div>
        <div id="IDAB_tab2" class="codeSnippetContainerTab">
          <a href="#" onclick="ChangeTab('IDAB','vb','2','2');return false;">Json</a>
        </div>
      </div>
      <div class="codeSnippetContainerCodeContainer">
        <div class="codeSnippetToolBar">
          <div class="codeSnippetToolBarText">
            <a id="IDAB_copyCode" href="#" class="copyCodeSnippet"
               onclick="CopyToClipboard('IDAB');return false;" title="Copy">Copy</a>
          </div>
        </div>
        <div id="IDAB_code_Div1" class="codeSnippetContainerCode" style="display: none">
          <pre xml:space="preserve">{xml_content}</pre>
        </div>
        <div id="IDAB_code_Div2" class="codeSnippetContainerCode" style="display: none">
          <pre xml:space="preserve">{json_content}</pre>
        </div>
      </div>
    </div>
  </div>
</markup>
"""
  # Ausgabe schreiben
  with open(output_path, "w", encoding="utf-8") as f:
      f.write(html_full)

  print(f"✅ Fertig: {output_path}")

  # # HTML-Seite umrahmen
  # html_full = f"""<!DOCTYPE html>
  # <html lang="de">
  # <head>
  # <meta charset="UTF-8">
  # <title>Syntax Highlight – {os.path.basename(input_path)}</title>
  # </head>
  # <body>
  # {html_code}
  # </body>
  # </html>
  # """

