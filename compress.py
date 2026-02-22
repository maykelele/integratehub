import os
from PIL import Image

def compress_images(directory, quality=70):
    # Prolazi kroz sve fajlove u folderu
    for filename in os.listdir(directory):
        if filename.endswith((".png", ".jpg", ".jpeg")):
            filepath = os.path.join(directory, filename)
            
            # Otvaranje slike
            img = Image.open(filepath)
            
            # Konverzija u RGB (ako je PNG sa transparentnošću, a čuvaš kao JPG)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            
            # Čuvanje sa kompresijom (zamenjuje stari fajl)
            img.save(filepath, "JPEG", optimize=True, quality=quality)
            print(f"Komprimovano: {filename}")

# Koristi putanju do tvog assets foldera
compress_images('public/assets/screenshots')