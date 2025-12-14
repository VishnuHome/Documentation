# check_image_borders.py
from PIL import Image

img = Image.open("media/Trigger_TestJobDescription_json.png")
print(img.size)
print(img.getbbox())

pixels = img.load()

w, h = img.size
right_column = [pixels[w-1, y] for y in range(h)] # type: ignore
bottom_row = [pixels[x, h-1] for x in range(w)] # type: ignore

print("Rechts:", set(right_column)) # type: ignore
print("Unten:", set(bottom_row)) # type: ignore

# img = Image.open("bild.png")
clean = img.crop((0, 0, img.width - 1, img.height - 1))
clean.save("bild_ohne_rand.png")