import os
import re
import argparse
import requests
import time
import json
from tqdm import tqdm

#######################################################################
# Übersetzt ausgewählte deutsche *.htm-Dateien als Ganzes über DeepL  #
# (free account) in's Englische (Quelle: ...\html_to_translate).      #
#######################################################################

directory = r"html_to_translate"

german_english_regex = [
    r'\(Stand: (\d\d\.\d\d\.\d\d\d\d)\)',
    r'<meta name="Description" content=\s*"(.*?)"'
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
        if args.simulate:
            translated_hit = hit.upper()
        elif pattern == r'\(Stand: (\d\d\.\d\d\.\d\d\d\d)\)':
            translated_hit = translate_date(pattern, hit)
            full_match = "(" + inner_match + ")"
        else:
            translated_hit = translate_text(hit, "en-US", "de", args.DEEPL_API_KEY)

    if translated_hit is not None:
        # file_content = re.sub(pattern, re.escape(match.group(0).replace(match.group(1), translated_content)), file_content)
        # file_content = re.sub(pattern, match.group(0).replace(match.group(1), translated_content), file_content)
        translated_full_match = full_match.replace(inner_match, translated_hit).replace("\\", "#__#")
        file_content = re.sub(pattern, translated_full_match, file_content.replace("\\", "#__#")).replace("#__#", "\\")

    return file_content, hit, translated_hit

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

def translate_file(input_file_path, output_file_path, auth_key):
    DEEPL_API_URL = "https://api-free.deepl.com/v2/document"  # Use api.deepl.com for Pro users
    document_id, document_key = upload_file(DEEPL_API_URL, auth_key, input_file_path)
    wait_for_translation(DEEPL_API_URL, auth_key, document_id, document_key)
    download_file(DEEPL_API_URL, auth_key, document_id, document_key, output_file_path)

def upload_file(url, auth_key, input_file_path):
    # Step 1: Upload the HTML file to DeepL
    with open(input_file_path, "rb") as file:
        upload_response = requests.post(
            url,
            headers={"Authorization": f"DeepL-Auth-Key {auth_key}"},
            files={"file": file},
            data={
                "target_lang": "EN-US",
                "source_lang": "DE",
                "tag_handling": "html"
            }
        )
    
    if upload_response.status_code == 200:
        document_id = upload_response.json()["document_id"]
        document_key = upload_response.json()["document_key"]
        print("Document uploaded successfully.")
    else:
        print(f"Failed to upload document: {upload_response.status_code} {upload_response.text}")
        exit(1)
    return document_id, document_key
    
def wait_for_translation(url, auth_key, document_id, document_key):
    # Step 2: Check the status of the translation
    status_url = f"{url}/{document_id}"
    status_response = requests.post(
        status_url,
        headers={"Authorization": f"DeepL-Auth-Key {auth_key}"},
        data={"document_key": document_key}
    )
    
    while status_response.status_code == 200 and status_response.json()["status"] != "done":
        print("Waiting for translation to complete...")
        time.sleep(0.05)
        status_response = requests.post(
            status_url,
            headers={"Authorization": f"DeepL-Auth-Key {auth_key}"},
            data={"document_key": document_key}
        )
    
    if status_response.json()["status"] != "done":
        print(f"Translation failed: {status_response.json()}")
        exit(1)
    
def download_file(url, auth_key, document_id, document_key, output_file_path):
    # Step 3: Download the translated document
    download_url = f"{url}/{document_id}/result"
    download_response = requests.post(
        download_url,
        headers={"Authorization": f"DeepL-Auth-Key {auth_key}"},
        data={"document_key": document_key}
    )
    
    if download_response.status_code == 200:
        with open(output_file_path, "wb") as file:
            file.write(download_response.content)
        print(f"Translation successful! Translated file saved to {output_file_path}")
    else:
        print(f"Failed to download translated document: {download_response.status_code} {download_response.text}")
    
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
        file_content = file_content.replace(
            original,
            english)

    if not os.path.exists(filepath + ".org"):
        os.rename(filepath, filepath + ".org")
        tmp_basename, tmp_ext = os.path.splitext(filepath)
        temp_path = tmp_basename + ".tmp" + tmp_ext
        with open(temp_path, 'w', encoding="utf-8") as f_out:
            f_out.write(file_content)
        translate_file(temp_path, filepath, args.DEEPL_API_KEY)
        os.remove(temp_path)
        os.rename(filepath, temp_path)

        # Verwende eine Regex, um den Inhalt des übersetzten <title>-Tags zu finden
        new_content = ""
        with open(temp_path, "r", encoding="utf-8") as file:
            new_content = file.read()
        
        for original in english_english_fix:
            english = english_english_fix[original]
            # Ersetzen mit Groß-/Kleinschreibung ignoriert
            new_content = re.sub(original, english, new_content, flags=re.IGNORECASE)
        
        _, filename = os.path.split(filepath)
        title = filename  # Falls später kein <title> gefunden wird, verwende den Dateinamen

        match = re.search(r'<title>(.*?)</title>', new_content, re.IGNORECASE)
        if match:
            title = match.group(1).strip()  # Gib den Inhalt des <title> zurück
        filepath_title[filename] = title

        with open(filepath, 'w', encoding="utf-8") as f_out:
            f_out.write(new_content)
        os.remove(temp_path)


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

with open('filepath_title_hhc_addon.json', 'w', encoding='utf-8') as file:
    json.dump(filepath_title, file, ensure_ascii=False, indent=4)

print("Das Dictionary 'filepath_title' wurde als JSON-Datei 'filepath_title_hhc_addon.json' gespeichert.")
