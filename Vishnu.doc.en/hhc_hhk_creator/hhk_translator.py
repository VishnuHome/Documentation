import os
import re
import time
import json
from tqdm import tqdm

# Erzeugt eine englische Key-Datei Vishnu_doc.en.hhk.
# Liest zuerst aus allen *.htm-Dateien im Unterverzeichnis html
# die Titel aus (<title>(.*?)</title>) und schreibt sie mit den zugehörigen
# Dateinamen in einen Hash.
# Dann wird die deutsche Content-Datei Vishnu_doc.de.hhc eingelesen und
# die Local-Werte (Dateinamen) mit den zugehörigen 
# Name-Werten als Keys in einen zweiten Hash geschrieben.
# Zuletzt wird die deutsche Key-Datei Vishnu_doc.de.hhk eingelesen und
# mit Hilfe der deutschen Name-Werte als Keys aus dem zweiten Hash die
# zugehörigen Dateipfade geholt. Diese werden dann als Keys in den ersten
# Hash verwendet, um letztendlich die englischen Übersetzungen für die
# Name-Werte zu holen.
# Das Ergebnis als Vishnu_doc.en.hhk weggeschrieben.
# Hinweis: das Bilden der englischen Vishnu_doc.en.hhk muss über
# Umschreiben der deutschen Vishnu_doc.de.hhk erfolgen, da nur so die
# ursprüngliche Strukturinformation erhalten bleibt.

directory = r"html"
output_file = os.path.join(directory, "../Vishnu_doc.en.hhk")
filepath_title = {}
german_filepath = {}
german_english = {
    "Methode": "method",
    "Methoden": "methods",
    "Klasse": "class",
    "Eigenschaft": "property",
    "Eigenschaften": "properties",
    "Konstruktor": "constructor",
    "Feld": "field",
    "Felder": "fields",
    "Ereignis": "event",
    "Ereignisse": "events",
    "Namensraum": "namespace",
    "Schnittstelle": "interface",
    "Enumerationsmember": "enumeration member"
}
out_lines = []

def last_word(text):
    # Den String in Wörter aufteilen
    words = text.split()
    # Das letzte Wort zurückgeben
    return words[-1] if words else None

# Funktion zum Extrahieren des <title>-Tags aus einer HTML-Datei
def extract_filepath_title_from_htmls(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()

        # Verwende eine Regex, um den Inhalt des <title>-Tags zu finden
        match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
        if match:
            title = match.group(1).strip()  # Gib den Inhalt des <title> zurück
        else:
            title = os.path.basename(filepath)  # Falls kein <title> gefunden wurde, verwende den Dateinamen

    return os.path.basename(filepath), title

# Funktion zum Extrahieren aller Name-Values und Local-Values in einer hhc-Datei
# und Füllen des Hashes "german_filepath".
def extract_german_filepath_from_hhc():
    path_in = "Vishnu_doc.de.hhc"
    key = None
    path = None
    with open(path_in, "r", encoding="utf-8") as f_in:
        for line in f_in:
            # line = line.replace(old_word, new_word)
            match = re.search(r'name="Name" value="(.*?)">', line, re.IGNORECASE)
            # print(".", end="")
            if match:
                key = (match.group(1).strip()) # Gib den Inhalt von "Name" zurück
            else:
                match = re.search(r'name="Local" value="(.*?)">', line, re.IGNORECASE)
                if match:
                    path = os.path.basename(match.group(1).strip()) # Gib den Inhalt von "Local" zurück
                    german_filepath[key] = path

# Funktion zum Übersetzen aller Name-Values in einer hhk-Datei
def translate_hhk():
    path_in = "Vishnu_doc.de.hhk"
    path_out = "Vishnu_doc.en.hhk"
    name = None
    name_line = None
    path = None
    path_line = None
    with open(path_in, "r", encoding="utf-8") as f_in, open(path_out, 'w') as f_out:
        for line in f_in:
            match = re.search(r'name="Name" value="(.*?)">', line, re.IGNORECASE)
            if match:
                name = (match.group(1).strip()) # Gib den Inhalt von "Name" zurück
                name_line = line
                last = last_word(name)
                if last in german_english:
                    out_lines.append(line.replace(last, german_english[last]))
                else:
                    if name in german_filepath:
                        path = german_filepath[name]
                        out_lines.append(line.replace(name, filepath_title[path]))
                    else:
                        out_lines.append(name_line)
            else:
                match = re.search(r'name="Local" value="(.*?)">', line, re.IGNORECASE)
                if match:
                    path_line = line
                    path = os.path.basename(match.group(1).strip()) # Gib den Inhalt von "Local" zurück
                    # out_lines.append(name_line.replace(name, filepath_title[path]))
                    out_lines.append(path_line)
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
    filename, title = extract_filepath_title_from_htmls(filepath)
    filepath_title[filename] = title
    time.sleep(0.01)
    progress.update(step)
    # print(".", end="")

# Lies die deutsche Content-Datei Vishnu_doc.de.hhc und fülle
# die Local-Werte (Dateinamen) mit den zugehörigen 
# Name-Werten als Keys in den Hash german_filepath.
extract_german_filepath_from_hhc()

# Übersetze die Inhalte der deutschen HHC-Datei
path_out = translate_hhk()

print(f"HHK-Datei erfolgreich erstellt: {path_out}")

with open('filepath_title_hhk.json', 'w', encoding='utf-8') as file:
    json.dump(filepath_title, file, ensure_ascii=False, indent=4)

print("Das Dictionary 'filepath_title' wurde als JSON-Datei 'filepath_title_hhk.json' gespeichert.")

with open('german_filepath_hhk.json', 'w', encoding='utf-8') as file:
    json.dump(german_filepath, file, ensure_ascii=False, indent=4)

print("Das Dictionary 'german_filepath' wurde als JSON-Datei 'german_filepath_hhk.json' gespeichert.")
