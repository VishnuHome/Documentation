import os
import re
import json
import time
from tqdm import tqdm

# Erzeugt eine englische Content-Datei Vishnu_doc.en.hhc.
# Liest zuerst aus allen englischen *.htm-Dateien im Unterverzeichnis html
# die Titel aus (<title>(.*?)</title>) und schreibt sie mit den zugehörigen
# Dateinamen in einen Hash.
# Zuletzt wird die deutsche Content-Datei Vishnu_doc.de.hhc eingelesen und
# alle Name-Werte mit Hilfe der zugehörigen Local-Werte als Keys in den
# vorher gebildeten Hash in ihr englisches Äquivalent übersetzt und
# das Ergebnis als Vishnu_doc.en.hhc weggeschrieben.
# Hinweis: das Bilden der englischen Vishnu_doc.en.hhc muss über
# Umschreiben der deutschen Vishnu_doc.de.hhc erfolgen, da nur so die
# ursprüngliche Strukturinformation erhalten bleibt.

directory = r"html"
output_file = os.path.join(directory, "../Vishnu_doc.en.hhc")
filepath_title = {}
out_lines = []

# Funktion zum Extrahieren des <title>-Tags aus einer HTML-Datei
def work_on_file(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()

        # Verwende eine Regex, um den Inhalt des <title>-Tags zu finden
        match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
        if match:
            title = match.group(1).strip()  # Gib den Inhalt des <title> zurück
        else:
            title = os.path.basename(filepath)  # Falls kein <title> gefunden wurde, verwende den Dateinamen

    return os.path.basename(filepath), title

# Funktion zum Übersetzen aller <title>-Tags in einer hhc-Datei
def translate_hhc():
    path_in = "Vishnu_doc.de.hhc"
    path_out = "Vishnu_doc.en.hhc"
    name = None
    name_line = None
    key = None
    key_line = None
    with open(path_in, "r", encoding="utf-8") as f_in, open(path_out, 'w') as f_out:
        for line in f_in:
            # line = line.replace(old_word, new_word)
            match = re.search(r'name="Name" value="(.*?)">', line, re.IGNORECASE)
            if match:
                name = os.path.basename(match.group(1).strip()) # Gib den Inhalt von "Name" zurück
                name_line = line
            else:
                match = re.search(r'name="Local" value="(.*?)">', line, re.IGNORECASE)
                if match:
                    key = os.path.basename(match.group(1).strip()) # Gib den Inhalt von "Local" zurück
                    key_line = line
                    out_lines.append(name_line.replace(name, filepath_title[key]))
                    out_lines.append(key_line)
                else:
                    out_lines.append(line)
        f_out.writelines(out_lines)
        return path_out

###########
# M A I N #
###########

# Durchlaufe alle HTM-Dateien im Verzeichnis
all_files = [f for f in os.listdir(directory) if f.endswith(".htm")]
progress = tqdm(total=len(all_files), desc="")
step = 1
progress.clear()
for filename in all_files:
    filepath = os.path.join(directory, filename)
    
    # Extrahiere den <title> aus der HTML-Datei
    filename, title = work_on_file(filepath)
    filepath_title[filename] = title
    time.sleep(0.01)
    progress.update(step)
    # print(".", end="")
        
# Übersetze die Inhalte der deutschen HHC-Datei
path_out = translate_hhc()

print(f"HHC-Datei erfolgreich erstellt: {path_out}")

with open('filepath_title_hhc.json', 'w', encoding='utf-8') as file:
    json.dump(filepath_title, file, ensure_ascii=False, indent=4)

print("Das Dictionary 'filepath_title' wurde als JSON-Datei 'filepath_title_hhc.json' gespeichert.")
