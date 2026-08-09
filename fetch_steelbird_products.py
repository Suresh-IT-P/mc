import urllib.request
import re
import json

def fetch_category_products(url, category):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    products = []
    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            
        # Let's find all product cards. A product card has class col-lg-3 col-md-4 col-sm-6 col-xs-6 product
        # and contains a product link with title, image, and priceSec
        cards = re.findall(r'<div class="col-lg-3 col-md-4 col-sm-6 col-xs-6 product".*?</a>\s*</div>\s*</div>\s*</div>', html, re.DOTALL)
        if not cards:
            # Fallback if the card boundary is slightly different
            cards = re.findall(r'<div class="col-lg-3 col-md-4 col-sm-6 col-xs-6 product".*?<!--\s*actions-btn\s*-->', html, re.DOTALL)
            if not cards:
                # If still nothing, let's try a regex on the whole HTML for product details
                cards = re.findall(r'<div class="product-item">.*?</div>\s*</div>\s*</div>\s*</div>', html, re.DOTALL)
                
        print(f"Found {len(cards)} HTML product blocks for category: {category}")
        
        for card in cards:
            title_m = re.search(r'class="product-link"\s+title="([^"]+)"', card)
            if not title_m:
                title_m = re.search(r'title="([^"]+)"\s+href="https://www.steelbirdhelmet.com/product/', card)
            if not title_m:
                continue
            title = title_m.group(1).strip()
            
            # Image
            img_m = re.search(r'<img src="([^"]+)"', card)
            img_url = img_m.group(1).strip() if img_m else ""
            
            # Price
            price_m = re.search(r'M\.R\.P\.:.*?&nbsp;([\d,]+(?:\.\d+)?)', card, re.DOTALL)
            price = 0
            if price_m:
                try:
                    price = int(float(price_m.group(1).replace(',', '')))
                except Exception as e:
                    print("Price parse error:", e)
                    
            desc = f"Premium {title} from Steelbird."
            
            products.append({
                "name": title,
                "category": category,
                "price": price,
                "image": img_url,
                "description": desc
            })
    except Exception as e:
        print(f"Error fetching URL {url}: {e}")
    return products

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

    print("Fetching Steelbird Helmets...")
    helmets = fetch_category_products("https://www.steelbirdhelmet.com/search?cat%5B0%5D=554", "Steelbird")
    
    print("Fetching Steelbird Accessories...")
    accessories = fetch_category_products("https://www.steelbirdhelmet.com/search?cat%5B0%5D=773", "Accessories")
    
    new_products = []
    for item in helmets + accessories:
        if item['name'].lower() in existing_titles:
            continue
        max_id += 1
        item['id'] = max_id
        new_products.append(item)
        existing_titles.add(item['name'].lower())

    print(f"Adding {len(new_products)} new products from Steelbird.")
    updated_products = existing_products + new_products
    
    js_content = f"const products = {json.dumps(updated_products, indent=2)};\n\n// Helper to format currency\nfunction formatPrice(price) {{\n  return \"₹\" + price.toLocaleString(\"en-IN\");\n}}\n"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(js_content)
        
    print("js/products.js updated successfully with Steelbird products.")

if __name__ == "__main__":
    main()
