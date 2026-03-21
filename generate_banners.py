"""
Generate simple placeholder banner images for each category.
Run from project root: python generate_banners.py
Creates public/assets/banners/ with category placeholders.
Requires: pip install Pillow
"""
import os
try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Pillow not installed. Run: pip install Pillow")
    exit(1)

BANNER_DIR = 'public/assets/banners'
WIDTH, HEIGHT = 800, 500

CATEGORIES = {
    'lead-capture': {'label': 'Lead Capture', 'color': '#1a73e8'},
    'payments': {'label': 'Payments & Invoicing', 'color': '#0d652d'},
    'onboarding': {'label': 'Client Onboarding', 'color': '#7b1fa2'},
    'comparisons': {'label': 'Comparisons', 'color': '#e65100'},
    'automation-strategy': {'label': 'Automation Strategy', 'color': '#00695c'},
    'reporting': {'label': 'Reporting', 'color': '#4527a0'},
    'default': {'label': 'IntegrateHub.io', 'color': '#0868b4'},
}

os.makedirs(BANNER_DIR, exist_ok=True)

for slug, info in CATEGORIES.items():
    img = Image.new('RGB', (WIDTH, HEIGHT), info['color'])
    draw = ImageDraw.Draw(img)
    
    # Simple centered text
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
    except:
        font = ImageFont.load_default()
    
    text = info['label']
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (WIDTH - tw) // 2
    y = (HEIGHT - th) // 2
    draw.text((x, y), text, fill='white', font=font)
    
    filepath = os.path.join(BANNER_DIR, f'{slug}.jpg')
    img.save(filepath, 'JPEG', quality=85)
    print(f"✅ {filepath}")

print(f"\nDone. {len(CATEGORIES)} banners created.")
