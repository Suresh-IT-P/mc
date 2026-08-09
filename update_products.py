import os
import re
import json

existing_products = [
  {
    "id": 1,
    "name": "Axxis Draken Solid Matte Black Helmet",
    "category": "Helmets",
    "price": 3850,
    "image": "https://images.unsplash.com/photo-1558981806-ec527fa84c39?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "description": "The Axxis Draken helmet offers a sleek matte black finish with superior aerodynamic design and DOT certified safety."
  },
  {
    "id": 2,
    "name": "Rynox Stealth Evo V3 Riding Jacket",
    "category": "Riding Gear",
    "price": 6500,
    "image": "https://images.unsplash.com/photo-1544644181-1484b3fdfc62?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "description": "Premium riding jacket with CE Level 2 protectors on shoulders, elbows, and back."
  },
  {
    "id": 3,
    "name": "Raida Aero Riding Gloves",
    "category": "Riding Gear",
    "price": 2200,
    "image": "https://images.unsplash.com/photo-1518131379650-8b17300c73e1?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "description": "Mesh and leather hybrid gloves perfect for summer riding with knuckle protection."
  },
  {
    "id": 4,
    "name": "Bar End Mirrors - Round",
    "category": "Accessories",
    "price": 850,
    "image": "https://images.unsplash.com/photo-1615172282427-9a57ef2d142e?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "description": "CNC machined aluminum bar end mirrors for a cafe racer look."
  },
  {
    "id": 5,
    "name": "MT Thunder 3 Pro Helmet",
    "category": "Helmets",
    "price": 5200,
    "image": "https://images.unsplash.com/photo-1533560904424-a0c61dc306fc?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "description": "Sport touring helmet with integrated sun visor and high impact shell."
  },
  {
    "id": 6,
    "name": "Universal LED Indicators",
    "category": "Accessories",
    "price": 600,
    "image": "https://images.unsplash.com/photo-1558981403-c5f9899a28bc?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "description": "Bright sequential LED turn signals, universal fit for all motorcycles."
  }
]

image_dir = 'g:/mc/image/image'
if os.path.exists(image_dir):
    images = sorted([f for f in os.listdir(image_dir) if f.endswith('.png') or f.endswith('.jpg')])
else:
    images = []

products = existing_products.copy()

with open('g:/mc/extracted_utf8.txt', 'r', encoding='utf8') as f:
    lines = f.read().splitlines()

for line in lines:
    line = line.strip()
    if not line: continue
    
    parts = line.split('.', 1)
    if len(parts) < 2:
        parts = line.split('-', 1)
        if len(parts) < 2:
            continue
            
    try:
        pid = int(parts[0].strip())
    except ValueError:
        continue
    
    rest = parts[1].strip()
    price = 0
    m = re.search(r'-\s*(\d+)\s*$', rest)
    if m:
        price = int(m.group(1))
        name = rest[:m.start()].strip()
        if name.endswith('-'):
            name = name[:-1].strip()
    else:
        m2 = re.search(r'(\d+)(?:/\d+)?$', rest)
        if m2:
            price = int(m2.group(1))
            name = rest[:m2.start()].strip()
            if name.endswith('-'):
                name = name[:-1].strip()
        else:
            name = rest
            
    name = re.sub(r'-\s*\d+\s*(?:pc|pcs)?$', '', name, flags=re.IGNORECASE).strip()
    if name.endswith('-'):
        name = name[:-1].strip()
            
    name_lower = name.lower()
    category = "Accessories"
    if "helmet" in name_lower:
        category = "Helmets"
    elif "jacket" in name_lower or "glove" in name_lower or "boot" in name_lower or "mask" in name_lower:
        category = "Riding Gear"
    elif "exhaust" in name_lower:
        category = "Exhaust"
    elif "light" in name_lower or "fog" in name_lower or "strobe" in name_lower or "indicator" in name_lower or "led" in name_lower or "headlight" in name_lower:
        category = "Lights"
    elif "guard" in name_lower or "crash" in name_lower or "slider" in name_lower or "protector" in name_lower:
        category = "Protection"
        
    new_id = len(products) + 1
    
    acronyms = {'mt', 'ktm', 'mg', 'led', 'pvc', 'hjg', 'ns', 'rs', 'r15', 'v2', 'v3', 'v4', 'cnc', 'lm', 'dsg', 'mrp'}
    words = name.strip(' -').split()
    capitalized_words = []
    for w in words:
        if w.lower() in acronyms:
            capitalized_words.append(w.upper())
        else:
            capitalized_words.append(w.capitalize())
            
    name_clean = ' '.join(capitalized_words)
    
    products.append({
        "id": new_id,
        "name": name_clean,
        "category": category,
        "price": price,
        "image": "",
        "description": "Premium " + name_clean + " for your motorcycle."
    })

js_output = "const products = " + json.dumps(products, indent=2) + ";\n\n// Helper to format currency\nfunction formatPrice(price) {\n  return \"₹\" + price.toLocaleString(\"en-IN\");\n}\n"

with open('g:/mc/js/products.js', 'w', encoding='utf8') as f:
    f.write(js_output)

print(f"Added {len(products)-6} products. Total products: {len(products)}")
