import os
import re
import argparse
import requests
import time
import json
from tqdm import tqdm

#######################################################################
# Einmal-Anwendung: die modifizierten *.htm-Dateien wurden nach Lauf  #
# dieses Scripts von Hand nach html.en.online.stripped zurückkopiert. #
# Die ursprünglichen *.htm-Dateien (vor diesem Script) sind in        #
# html.en.online.stripped noch als *.org vorhanden.                   #
#######################################################################

raise Exception("Diese Einmal-Anwendung ist schon einmal gelaufen!")

# Übersetzt bestimmte Teile der (über DeepL vorübersetzten)
# *.htm-Dateien nachträglich in's Englische.
# Quelle: ...\private4\Python\hhc_hhk_creator\html.en.online.stripped.

directory = r"html"

german_english_regex = [
    r'<meta name="Description" content=\s*"(.*?)"'
]

german_english_fix = {
    'title="woher der Name"': '"title="Where does the name come from"',
    "de-de": "en-US",
    "branding-de-DE": "branding-en-US",
    ">Vishnu control<": ">Vishnu Control<",
    "Dieses Kapitel gibt einen Überblick über die Kommandos: mit denen Vishnu über Maus und Tastatur gesteuert werden kann.": "This chapter gives an overview of the commands that can be used to control Vishnu via mouse and keyboard.",
    "Vishnu - Observe and control processes": "Vishnu - observe and control processes",
    "Vishnu - der logische Prozess-Monitor": "Vishnu - the logical process monitor",
    "Einstieg": "Quick Start",
    ">Access<": "Quick Start",
    "advanced topics": "Advanced Topics",
    "Versionshistorie": "Version History",
    "Version history": "Version History",
    "Construction sites": "Construction Sites",
    "Own checkers": "Custom Checkers",
    "Own triggers": "Custom Triggers",
    "Own logger": "Custom Loggers",
    "own views": "Custom Views",
    "Own parameter reader": "Custom Parameter Reader",
    "Log checker history": "Log Checker History",
    "Known errors and problems": "Known Errors and Problems",
    "Collection of ideas": "Collection of Ideas",
    "Named triggers and loggers": "Named Triggers and Loggers",
    "ein einfaches Beispiel": "A simple Example",
    "a simple example": "A simple Example",
    "woher der Name": "Where does the name come from",
    ">details<": ">Details<",
    "Wichtig": "Important",
    "Uebersicht": "Overview",
    "Privacy policy and imprint": "Privacy Policy and Imprint",
    "Vishnu - technical documentation": "Vishnu - technical Documentation",
    "List of pages of interest": "Pages of interest",
    "das Kontext Menü": "Context Menu",
    "the context menu": "Context Menu",
    "Vishnu Logik": "Vishnu Logic",
    ">Vishnu logic<": ">Vishnu Logic<",
    "Serialise": "Serialize",
    "serialise": "serialize",
    "Initialisat": "Initializat",
    "initialise": "initialize",
    "Public Methode": "Public Method",
    "Protected Methode": "Protected Method",
    "Public Eigenschaft": "Public Property",
    "Protected Eigenschaft": "Protected Property",
    "Public Feld": "Public Field",
    "Protected Feld": "Protected Field",
    "Public Klasse": "Public Class",
    "Protected Klasse": "Protected Class",
    "Public Schnittstelle": "Public Interface",
    "Public Delegat": "Public Delegate",
    "Public Ereignis": "Public Event"
}
german_english_all = german_english_fix.copy()

def search_and_translate_items(pattern, file_content):
    hit = None
    translated_hit = None
    # Description content
    match = re.search(pattern, file_content, re.IGNORECASE | re.DOTALL)
    if match:
        hit = match.group(1).strip()  # Gib den Inhalt des Treffers zurück
    if hit is not None:
        if args.simulate:
            translated_hit = hit.upper()
        else:
            translated_hit = translate_text(hit, "en-US", "de", args.DEEPL_API_KEY)

    if translated_hit is not None:
        # file_content = re.sub(pattern, re.escape(match.group(0).replace(match.group(1), translated_content)), file_content)
        # file_content = re.sub(pattern, match.group(0).replace(match.group(1), translated_content), file_content)
        full_match = match.group(0)
        inner_match = match.group(1)
        translated_full_match = full_match.replace(inner_match, translated_hit).replace("\\", "#__#")
        file_content = re.sub(pattern, translated_full_match, file_content.replace("\\", "#__#")).replace("#__#", "\\")

    return file_content, hit, translated_hit

# Funktion zum Verarbeiten einer HTM-Datei
def work_on_file(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        file_content = file.read()

    for pattern in german_english_regex:
        file_content, german, english = search_and_translate_items(pattern, file_content)
        if german:
            german_english_all[german] = english

    for german in german_english_fix:
        english = german_english_fix[german]
        file_content = file_content.replace(
            german,
            english)

    if not os.path.exists(filepath + ".org"):
        os.rename(filepath, filepath + ".org")
        with open(filepath, 'w', encoding="utf-8") as f_out:
            f_out.write(file_content)

def translate_text(text, target_lang, source_lang, auth_key):
    url = "https://api-free.deepl.com/v2/translate"
    
    # Die erforderlichen Parameter für die API
    params = {
        "text": text,
        "target_lang": target_lang,
        "source_lang": source_lang
    }
    
    # Der Authentication Header
    headers = {
        "Authorization": f"DeepL-Auth-Key {auth_key}"
    }
    
    time.sleep(0.05)

    try:
        # POST-Anfrage senden
        response = requests.post(url, params=params, headers=headers)
        
        # Prüfen ob die Anfrage erfolgreich war
        response.raise_for_status()
        
        # JSON-Antwort verarbeiten
        result = response.json()
        
        # Übersetzung zurückgeben
        return result["translations"][0]["text"]
    
    except requests.exceptions.RequestException as e:
        print(f"Fehler bei der API-Anfrage: {e}")
        return None

###########
# M A I N #
###########

parser = argparse.ArgumentParser(description='html_translator args')
parser.add_argument('-s', '--simulate', action='store_true', default=False, help='true=only change to uppercase, default=False (call DeepL)')
parser.add_argument('--DEEPL_API_KEY', '--DEEPL_API_KEY', help='Key for accessing DeepL-Api', default='')

args = parser.parse_args()

print(f"simulate: {args.simulate}")
# print(f"Key: {args.DEEPL_API_KEY}")

# Durchlaufe alle HTM-Dateien im Verzeichnis
all_files = [f for f in os.listdir(directory) if f.endswith(".htm")]
progress = tqdm(total=len(all_files), desc="")
step = 1
progress.clear()
for filename in all_files:
    # if filename == "M_Vishnu_Interchange_AppSettings_ReplaceWildcards.htm":
    filepath = os.path.join(directory, filename)
        
    # Übersetzen bestimmter Teile der HTM-Datei
    work_on_file(filepath)
    progress.update(step)
    if args.simulate:
        time.sleep(0.01)
    # print(".", end="")
        
print(f"HTM-Dateien erfolgreich verarbeitet.")

with open('german_english.json', 'w', encoding='utf-8') as file:
    json.dump(german_english_all, file, ensure_ascii=False, indent=4)

print("Das Dictionary 'german_english_all' wurde als JSON-Datei 'german_english.json' gespeichert.")
