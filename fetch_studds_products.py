import urllib.request
import json
import ssl
import html
import re

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
    ssl_context = ssl._create_unverified_context()
    while True:
        url = f"https://shop.studds.com/wp-json/wc/store/v1/products?per_page=100&page={page}"
        print(f"Fetching page {page}...")
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, context=ssl_context) as response:
                products = json.loads(response.read().decode('utf-8'))
                if not products:
                    break
                all_products.extend(products)
                page += 1
        except Exception as e:
            print(f"Error fetching page {page}: {e}")
            break
    return all_products

def main():
    # Read existing products
    filepath = 'g:/mc/js/products.js'
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        json_str = content[content.find('['):content.rfind(']')+1]
        existing_products = json.loads(json_str)
    except Exception as e:
        print(f"Error reading existing products: {e}")
        existing_products = []

    existing_titles = {p['name'].lower() for p in existing_products}
    max_id = max([p['id'] for p in existing_products]) if existing_products else 0

    raw_products = fetch_products()
    print(f"Fetched {len(raw_products)} raw products from Studds API.")

    new_products = []
    for p in raw_products:
        name = html.unescape(p.get("name", "")).strip()
        if name.lower() in existing_titles:
            continue
            
        # Determine category
        categories = [c.get("name", "").lower() for c in p.get("categories", [])]
        category = "Accessories"
        
        # If category name contains helmet, or name contains helmet
        if any("helmet" in c for c in categories) or "helmet" in name.lower():
            category = "Studds"
            
        price_val = p.get("prices", {}).get("price", "0")
        try:
            price = int(float(price_val) / 100.0)
        except:
            price = 0
            
        images = p.get("images", [])
        image_url = images[0].get("src", "") if images else ""
        
        desc = clean_html(p.get("description", "") or p.get("short_description", ""))
        if not desc:
            desc = f"Premium {name} from Studds."

        max_id += 1
        new_products.append({
            "id": max_id,
            "name": name,
            "category": category,
            "price": price,
            "image": image_url,
            "description": desc
        })
        existing_titles.add(name.lower())

    print(f"Adding {len(new_products)} new products from Studds.")
    updated_products = existing_products + new_products
    
    js_content = f"const products = {json.dumps(updated_products, indent=2)};\n\n// Helper to format currency\nfunction formatPrice(price) {{\n  return \"₹\" + price.toLocaleString(\"en-IN\");\n}}\n"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(js_content)
        
    print("js/products.js updated successfully with Studds products.")

if __name__ == "__main__":
    main()
