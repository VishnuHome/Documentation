import os
import re
import time
import json
from tqdm import tqdm

# Fügt wird einen englischer pageHeader ein.
# Und es wird aus allen *.htm-Dateien die HTML-Navigation
# auf der linken Seite (leftNav-Einträge) entfernt.
# Achtung: Es muss von Hand auch styles\branding-Website.css editiert werden.

directory = r"html"

# Funktion zum Verarbeiten einer HTM-Datei
def work_on_file(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        file_content = file.read()

        # englischen PageHeader einfügen

        file_content = file_content.replace(
            '<div class="pageBody">',
            '<div id="PageHeader" class="pageHeader">'
             + 'Vishnu - logical monitoring job controller</div><div class="pageBody">')

        # HTML-Navigation auf der linken Seite entfernen
        # (Es muss von Hand auch styles\branding-Website.css editiert werden)

        pattern = r'(?m)<div class="leftNav" id="leftNav">(.*?)<div id="TopicContent"' # geht
        file_content = re.sub(pattern, f'<div id="TopicContent"', file_content, flags=re.DOTALL)

    if not os.path.exists(filepath + ".sav"):
        os.rename(filepath, filepath + ".sav")
        with open(filepath, 'w', encoding="utf-8") as f_out:
            f_out.write(file_content)

###########
# M A I N #
###########

# Durchlaufe alle HTM-Dateien im Verzeichnis
all_files = [f for f in os.listdir(directory) if f.endswith(".htm")]
progress = tqdm(total=len(all_files), desc="")
step = 1
progress.clear()
for filename in all_files:
    # if filename == "62ca75a8-ba50-4115-93df-b1e76bf6e5f7.htm":
    filepath = os.path.join(directory, filename)
        
    # Verarbeiten der HTM-Datei
    work_on_file(filepath)
    progress.update(step)
    # print(".", end="")
        
print(f"HTM-Dateien erfolgreich verarbeitet.")
