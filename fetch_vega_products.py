import urllib.request
import json
import re
import subprocess
import html

def clean_html(raw_html):
    if not raw_html:
        return ""
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    cleantext = html.unescape(cleantext)
    return re.sub(r'\s+', ' ', cleantext).strip()

def fetch_products():
    page = 1
    all_products = []
    while True:
        url = f"https://vegaauto.com/products.json?limit=250&page={page}"
        print(f"Fetching page {page}...")
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                products = data.get('products', [])
                if not products:
                    break
                all_products.extend(products)
                page += 1
        except Exception as e:
            print(f"Error fetching page {page}: {e}")
            break
    return all_products

def main():
    # Fetch existing products from js/products.js natively in Python
    try:
        with open('g:/mc/js/products.js', 'r', encoding='utf-8') as f:
            content = f.read()
        json_str = content[content.find('['):content.rfind(']')+1]
        existing_products = json.loads(json_str)
    except Exception as e:
        print(f"Error reading existing products: {e}")
        existing_products = []

    existing_titles = {p['name'].lower() for p in existing_products}
    max_id = max([p['id'] for p in existing_products]) if existing_products else 0
    
    vega_raw = fetch_products()
    print(f"Fetched {len(vega_raw)} raw products from Vega.")

    new_products = []
    for p in vega_raw:
        title = p['title'].strip()
        if title.lower() in existing_titles:
            continue
            
        # Determine category
        prod_type = p.get('product_type', '').lower()
        tags = [t.lower() for t in p.get('tags', [])]
        
        category = "Accessories"
        if "helmet" in prod_type or any("helmet" in t for t in tags):
            category = "Vega"
        elif "visor" in prod_type or "spoiler" in prod_type or "cushion" in prod_type:
            category = "Accessories"
            
        # Price
        variants = p.get('variants', [])
        price = 0
        if variants:
            try:
                price = int(float(variants[0].get('price', 0)))
            except:
                pass
                
        # Image
        images = p.get('images', [])
        image_url = ""
        if images:
            image_url = images[0].get('src', '')
            
        desc = clean_html(p.get('body_html', ''))
        if not desc:
            desc = f"Premium {title} from Vega."
            
        max_id += 1
        new_products.append({
            "id": max_id,
            "name": title,
            "category": category,
            "price": price,
            "image": image_url,
            "description": desc
        })
        existing_titles.add(title.lower())

    print(f"Adding {len(new_products)} new products.")
    updated_products = existing_products + new_products
    
    js_content = f"const products = {json.dumps(updated_products, indent=2)};\n\n// Helper to format currency\nfunction formatPrice(price) {{\n  return \"₹\" + price.toLocaleString(\"en-IN\");\n}}\n"
    
    with open('g:/mc/js/products.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
        
    print("js/products.js updated successfully with Vega products.")

if __name__ == "__main__":
    main()
