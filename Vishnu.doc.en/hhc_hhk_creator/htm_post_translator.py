import os
import re
import json
from tqdm import tqdm

#######################################################################
# Nachbearbeitung für alle fertig übersetzten *.htm-Dateien im        #
# Verzeichnis html.en.online.stripped. Benutzt nur noch hart kodierte #
# Dictionaries, kein DeepL mehr.                                      #
#######################################################################

directory = r"html.en.online.stripped"

german_english_regex = [
    r'\(Stand: (\d\d\.\d\d\.\d\d\d\d)\)'
]

german_english_fix = {
    ">Access<": "Quick Start",
    ">Vishnu control<": ">Vishnu Control<",
    ">Vishnu logic<": ">Vishnu Logic<",
    ">details<": ">Details<",
    "Collection of ideas": "Collection of Ideas",
    "Construction sites": "Construction Sites",
    "Dieses Kapitel gibt einen Überblick über die Kommandos: mit denen Vishnu über Maus und Tastatur gesteuert werden kann.": "This chapter gives an overview of the commands that can be used to control Vishnu via mouse and keyboard.",
    "Eigenschaft": "property",
    "Eigenschaften": "properties",
    "Einstieg": "Quick Start",
    "Enumerationsmember": "enumeration member",
    "Ereignis": "event",
    "Ereignisse": "events",
    "Feld": "field",
    "Felder": "fields",
    "Initialisat": "Initializat",
    "Klasse": "class",
    "Known errors and problems": "Known Errors and Problems",
    "Konstruktor": "constructor",
    "List of pages of interest": "Pages of interest",
    "Log checker history": "Log Checker History",
    "Methode": "method",
    "Methoden": "methods",
    "Methodn": "methods",
    "Named triggers and loggers": "Named Triggers and Loggers",
    "Namensraum": "namespace",
    "Own checkers": "Custom Checkers",
    "Own logger": "Custom Loggers",
    "Own parameter reader": "Custom Parameter Reader",
    "Own triggers": "Custom Triggers",
    "<h4>parameter</h4>": "<h4>Parameters</h4>",
    "Privacy policy and imprint": "Privacy Policy and Imprint",
    "Protected Eigenschaft": "Protected Property",
    "Protected Feld": "Protected Field",
    "Protected Klasse": "Protected Class",
    "Protected Methode": "Protected Method",
    "Public Delegat": "Public Delegate",
    "Public Eigenschaft": "Public Property",
    "Public Ereignis": "Public Event",
    "Public Feld": "Public Field",
    "Public Klasse": "Public Class",
    "Public Methode": "Public Method",
    "Public Schnittstelle": "Public Interface",
    "Schnittstelle": "interface",
    "Serialise": "Serialize",
    "Uebersicht": "Overview",
    "Version history": "Version History",
    "Versionshistorie": "Version History",
    "Vishnu - Observe and control processes": "Vishnu - observe and control processes",
    "Vishnu - der logische Prozess-Monitor": "Vishnu - the logical process monitor",
    "Vishnu - technical documentation": "Vishnu - technical Documentation",
    "Vishnu Logik": "Vishnu Logic",
    "Wichtig": "Important",
    "a simple example": "A simple Example",
    "advanced topics": "Advanced Topics",
    "branding-de-DE": "branding-en-US",
    "das Kontext Menü": "Context Menu",
    "de-de": "en-US",
    "ein einfaches Beispiel": "A simple Example",
    "initialise": "initialize",
    "own views": "Custom Views",
    "serialise": "serialize",
    "the context menu": "Context Menu",
    "woher der Name": "Where does the name come from",
    'title="woher der Name"': '"title="Where does the name come from"',
    "Ihre Rückmeldung wird für die Verbesserung der Dokumentation und des Produktes genutzt. Ihre Email-Adresse wird zu keinem anderen Zweck benutzt und wird nach der Behebung des gemeldeten Problems gelöscht. Während der Arbeit an dem Problem kann es sein dass Sie per Email kontaktiert werden für weitergehende Details oder Abklärung zur Rückmeldung von Ihnen. Nachdem das Problem eingegrenzt worden ist kann es sein dass Sie eine Email erhalten zur Problembehebung.": "Your feedback will be used to improve the documentation and the product. Your email address will not be used for any other purpose and will be deleted after the reported issue has been resolved. While working on the problem, you may be contacted by email for further details or clarification of your feedback. After the problem has been isolated, you may receive an email to resolve the issue."
}
german_english_all = german_english_fix.copy()

english_english_fix = {
    ">Access<": "Quick Start",
    ">Vishnu control<": ">Vishnu Control<",
    ">Vishnu logic<": ">Vishnu Logic<",
    ">details<": ">Details<",
    "Classn": "classes",
    "Collection of ideas": "Collection of Ideas",
    "Construction sites": "Construction Sites",
    "-2024 Erik Nagel": "-2025 Erik Nagel",
    "Initialisat": "Initializat",
    "Known errors and problems": "Known Errors and Problems",
    "List of pages of interest": "Pages of interest",
    "Log checker history": "Log Checker History",
    "Methodn": "methods",
    "Named triggers and loggers": "Named Triggers and Loggers",
    "Namensraum": "Namespace",
    "Own checkers": "Custom Checkers",
    "Own logger": "Custom Loggers",
    "Own parameter reader": "Custom Parameter Reader",
    "Own triggers": "Custom Triggers",
    "Privacy policy and imprint": "Privacy Policy and Imprint",
    "Serialise": "Serialize",
    "Version history": "Version History",
    "Vishnu - Observe and control processes": "Vishnu - observe and control processes",
    "Vishnu - technical documentation": "Vishnu - technical Documentation",
    "a simple example": "A simple Example",
    "advanced topics": "Advanced Topics",
    "initialise": "initialize",
    "own views": "Custom Views",
    "serialise": "serialize",
    "the context menu": "Context Menu",
}

month_dict = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}

filepath_title = {}

def translate_date(pattern, date):
    day, month, year = date.split(".")
    return f"as of {month_dict[int(month)]} {day}, {year}"

def search_and_translate_items(pattern, file_content):
    hit = None
    full_match = None
    inner_match = None
    translated_hit = None
    # Description content
    match = re.search(pattern, file_content, re.IGNORECASE | re.DOTALL)
    if match:
        full_match = match.group(0)
        inner_match = match.group(1)
        hit = match.group(1).strip()  # Gib den Inhalt des Treffers zurück
    if hit is not None:
        if pattern == r'\(Stand: (\d\d\.\d\d\.\d\d\d\d)\)':
            translated_hit = translate_date(pattern, hit)
            full_match = "(" + inner_match + ")"
        else:
            translated_hit = hit

    if translated_hit is not None:
        # file_content = re.sub(pattern, re.escape(match.group(0).replace(match.group(1), translated_content)), file_content)
        # file_content = re.sub(pattern, match.group(0).replace(match.group(1), translated_content), file_content)
        translated_full_match = full_match.replace(inner_match, translated_hit).replace("\\", "#__#")
        file_content = re.sub(pattern, translated_full_match, file_content.replace("\\", "#__#")).replace("#__#", "\\")

    return file_content, hit, translated_hit

# Funktion zum Verarbeiten einer HTM-Datei
def work_on_file(filepath):
    file_content = ""
    with open(filepath, "r", encoding="utf-8") as file:
        file_content = file.read()

    for pattern in german_english_regex:
        file_content, german, english = search_and_translate_items(pattern, file_content)
        if german:
            german_english_all[german] = english

    for original in german_english_fix:
        english = german_english_fix[original]
        # Ersetzen mit Groß-/Kleinschreibung ignoriert
        file_content = re.sub(original, english, file_content, flags=re.IGNORECASE)

    for original in english_english_fix:
        english = english_english_fix[original]
        # Ersetzen mit Groß-/Kleinschreibung ignoriert
        file_content = re.sub(original, english, file_content, flags=re.IGNORECASE)
        
    if not os.path.exists(filepath + ".org"):
        os.rename(filepath, filepath + ".org")
        _, filename = os.path.split(filepath)
        title = filename  # Falls später kein <title> gefunden wird, verwende den Dateinamen

        # Verwende eine Regex, um den Inhalt des übersetzten <title>-Tags zu finden
        match = re.search(r'<title>(.*?)</title>', file_content, re.IGNORECASE)
        if match:
            title = match.group(1).strip()  # Gib den Inhalt des <title> zurück
        filepath_title[filename] = title

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
    # if filename == "M_Vishnu_Interchange_AppSettings_ReplaceWildcards.htm":
    filepath = os.path.join(directory, filename)
        
    # Übersetzen bestimmter Teile der HTM-Datei
    work_on_file(filepath)
    progress.update(step)
        
print(f"HTM-Dateien erfolgreich verarbeitet.")

with open('filepath_title_hhc_new.json', 'w', encoding='utf-8') as file:
    json.dump(filepath_title, file, ensure_ascii=False, indent=4)

print("Das Dictionary 'filepath_title' wurde als JSON-Datei 'filepath_title_hhc_new.json' gespeichert.")
