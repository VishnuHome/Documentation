import re

content = """Lorem ipsum dolor sit amet, 
[start]
Text, den du ersetzen möchtest.
und noch Text zu ersetzen,
und der auch noch.
  [end]
Consectetur adipiscing elit."""

# Neuen Inhalt definieren
new_text = "Dies ist der neue Text."

# Regex definieren, um den Bereich zwischen [start] und [end] zu finden und zu ersetzen
pattern = r'\[start\](.*?)(?m)\s*\[end\]'
new_content = re.sub(pattern, f"[start]\n{new_text}\n[end]", content, flags=re.DOTALL)
print(new_content)