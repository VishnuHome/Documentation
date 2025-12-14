import os
import base64
import mimetypes
from pathlib import Path
from PIL import Image

# --- Konfiguration ---
# image_path = Path("media/Trigger_TestJobDescription_json.png")  # Pfad zum Eingabebild
image_path = Path("media/CheckServers_JobDescription_Directory_json_labeled.png")  # Pfad zum Eingabebild
output_path = Path(os.path.splitext(image_path)[0] + ".html")

# Zwischenschritt um 1-Pixel Ränder rechts und unte zu entfernen.
# Diese werden u.U. von ClickChards Pro bei "Abbildung exportieren..." erzeugt,
# obwohl Rand 0 eingestellt ist.
img = Image.open(image_path)
clean = img.crop((0, 0, img.width - 1, img.height - 1))
image_path = Path("bild_ohne_rand.png")
clean.save("bild_ohne_rand.png")

# MIME-Typ automatisch ermitteln (z. B. image/png)
mime_type, _ = mimetypes.guess_type(image_path)
if mime_type is None:
    mime_type = "application/octet-stream"

# Datei lesen und in Base64 umwandeln
with open(image_path, "rb") as f:
    encoded = base64.b64encode(f.read()).decode("utf-8")

# HTML-kompatibler Data-URI
data_uri = f"data:{mime_type};base64,{encoded}"

# Ausgabe auf Konsole
print(data_uri)

# Optional: in HTML-Datei speichern
output_path.write_text(f'<img src="{data_uri}" alt="Embedded Image" />', encoding="utf-8")

print(f"\nData-URI wurde in '{output_path}' gespeichert.")
