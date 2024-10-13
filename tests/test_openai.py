# import openai

# # Set up your OpenAI API key
# openai.api_key = "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"

# def compare_products_with_openai(existing_products, new_products):
#     """
#     Use OpenAI to map new products to existing base products.
    
#     Args:
#         existing_products: List of dictionaries representing existing products from BaseProduct.
#         new_products: List of dictionaries representing newly scraped products.

#     Returns:
#         A list of tuples (new_product, base_product).
#     """
#     prompt = generate_openai_prompt(existing_products, new_products)
    
#     response = openai.completions.create(
#         model="gpt-3.5-turbo-instruct",  # Assuming you're using GPT-4 or the latest model.
#         prompt=prompt,
#         max_tokens=1000,  # Adjust as needed
#         temperature=0.0  # Set to 0 for more deterministic results
#     )

#     # Parse the response to extract match results
#     return parse_openai_response(response)

# def generate_openai_prompt(existing_products, new_products):
#     """
#     Generates a prompt to send to OpenAI for product mapping.
#     """
#     existing_list = "\n".join([f"{prod['name']}, {prod['category']}, {prod['price']}" for prod in existing_products])
#     new_list = "\n".join([f"{prod['name']}, {prod['category']}, {prod['price']}" for prod in new_products])

#     prompt = f"""
#     You are tasked with mapping products from a new source to existing products in a database.
#     Each new product should be mapped to the most similar existing product based on name, category, and price.
#     Products may have very similar names, but the details such as storage, model type, and color may differ. 
#     So in cases like this, for example 256gb and 512gb you should know those are different products, and not map them.
#     For example, "iPhone 15 Pro Max" and "iPhone 15 Pro" are different products. So we need to be careful with that.
#     If a new product matches an existing one, return the following:
#     "New Product: [new product name] -> Matched with: [existing product name]".
#     If no match is found, return: "No match for: [new product name]".

#     Existing Products:
#     {existing_list}

#     New Products:
#     {new_list}

#     For each new product, return in the format:
#     "New Product: [new product name] -> Matched with: [existing product name]"
#     If no match is found, return: "No match for: [new product name]".
#     """
#     return prompt

# def parse_openai_response(response):
#     """
#     Parse the OpenAI response to extract product mapping information.
    
#     Returns a list of tuples (new_product, base_product).
#     """
#     results = []
#     for line in response.choices[0].text.strip().split("\n"):
#         if "No match" in line:
#             # Handle no match case
#             new_product = line.split("No match for: ")[1]
#             results.append((new_product, None))  # No match
#         else:
#             # Extract the mapping details
#             parts = line.split("-> Matched with:")
#             new_product = parts[0].split("New Product: ")[1].strip()
#             base_product = parts[1].strip()
#             results.append((new_product, base_product))
#     return results

# # Example usage
# existing_products = [
#     {"name": "Maus Logitech G Pro X Superlight, i zi", "category": "gaming-mouse", "price": 120.99},
#     {"name": "Apple iPhone 15 Pro 256GB", "category": "smartphone", "price": 1299.99},
#     {"name": "Apple iPhone 15 Pro Max 512GB", "category": "smartphone", "price": 1299.99},
#     {"name": "Samsung Galaxy S23 Ultra 512GB", "category": "smartphone", "price": 1199.99},
#     {"name": "Sony WH-1000XM5 Wireless Headphones", "category": "headphones", "price": 399.99},
#     {"name": "Microsoft Surface Laptop 5 15''", "category": "laptop", "price": 1499.99},
#     {"name": "LG 4K OLED Smart TV 65''", "category": "television", "price": 1999.99},
#     {"name": "NVIDIA GeForce RTX 4090", "category": "graphics-card", "price": 1499.99},
#     {"name": "Dell UltraSharp 27'' 4K Monitor", "category": "monitor", "price": 899.99},
#     {"name": "Apple MacBook Pro 16'' M1 Max", "category": "laptop", "price": 3499.99},
#     {"name": "Razer BlackWidow V3 Pro", "category": "gaming-keyboard", "price": 179.99},
#     {"name": "Logitech MX Master 3", "category": "mouse", "price": 99.99},
#     {"name": "Sony PlayStation 5", "category": "gaming-console", "price": 499.99},
#     {"name": "Nintendo Switch OLED", "category": "gaming-console", "price": 349.99},
#     {"name": "Canon EOS R6 Full-Frame Mirrorless Camera", "category": "camera", "price": 2499.99},
#     {"name": "Bose QuietComfort Earbuds II", "category": "earbuds", "price": 279.99},
#     {"name": "Dyson V15 Detect Cordless Vacuum Cleaner", "category": "vacuum-cleaner", "price": 749.99},
#     {"name": "GoPro Hero 11 Black", "category": "action-camera", "price": 399.99},
#     {"name": "Samsung Galaxy Tab S8 Ultra", "category": "tablet", "price": 1099.99},
#     {"name": "Fitbit Charge 5", "category": "fitness-tracker", "price": 129.99},
#     {"name": "HP Envy x360 15.6'' 2-in-1 Laptop", "category": "laptop", "price": 999.99}
# ]

# new_products = [
#     {"name": "Logitech G PRO Wireless Gaming Mouse Superlight", "category": "it-and-elektronike/mause-and-tastier/maus", "price": 105.99},
#     {"name": "iPhone 15 Pro Max 512GB", "category": "smartphone", "price": 1399.99},
#     {"name": "Samsung Galaxy S23 Ultra 1TB", "category": "telefona-smart", "price": 1299.99},
#     {"name": "Sony WH1000XM4 Noise Cancelling Headphones", "category": "audio/aksesore-audio/kufje", "price": 299.99},
#     {"name": "Microsoft Surface Laptop 4 13.5''", "category": "kompjutera-dhe-tablete/laptop", "price": 1299.99},
#     {"name": "LG OLED 55'' 4K Smart TV", "category": "televizore", "price": 1499.99},
#     {"name": "NVIDIA GeForce RTX 4080", "category": "hardware/grafik-aqma", "price": 1199.99},
#     {"name": "Dell P2721Q 4K UltraSharp Monitor", "category": "elektronike/monitore", "price": 799.99},
#     {"name": "MacBook Pro 14'' M2 Pro", "category": "laptop", "price": 2799.99},
#     {"name": "Razer Huntsman Elite Gaming Keyboard", "category": "gaming-periferals", "price": 199.99},
#     {"name": "Logitech MX Master 3S", "category": "periferike", "price": 119.99},
#     {"name": "Sony PlayStation 5 Digital Edition", "category": "gaming-consoles", "price": 399.99},
#     {"name": "Nintendo Switch Lite", "category": "elektronike/konzole-gaming", "price": 199.99},
#     {"name": "Canon EOS R5 Mirrorless Camera", "category": "kamera-dhe-pajisje/kamera-fotografike", "price": 3799.99},
#     {"name": "Bose Noise Cancelling Headphones 700", "category": "elektronike/kufje", "price": 379.99},
#     {"name": "Dyson V11 Absolute Cordless Vacuum Cleaner", "category": "electroshtepiake/pastrimi", "price": 649.99},
#     {"name": "GoPro Hero 10 Black", "category": "kamerë-dhe-pajisje/kamera-veprimi", "price": 349.99},
#     {"name": "Samsung Galaxy Tab S7+", "category": "elektronike/tablete", "price": 899.99},
#     {"name": "Fitbit Versa 3", "category": "elektronike/ora-smart", "price": 199.99},
#     {"name": "HP Spectre x360 14'' 2-in-1 Laptop", "category": "kompjutera-dhe-tablete/laptop", "price": 1599.99},
#     {"name": "Tastierë SteelSeries Apex 3 (64795), e zezë", "category": "kompjutera-dhe-tablete/laptop", "price": 1599.99}
# ]

# results = compare_products_with_openai(existing_products, new_products)

# for new_product, base_product in results:
#     if base_product:
#         print(f"New Product: {new_product} matched with {base_product}. Inserting into database.")
#     else:
#         print(f"No match for new product: {new_product}. Creating new entry.")