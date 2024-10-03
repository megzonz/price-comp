from fuzzywuzzy import fuzz

def normalize_string(s):
    return ''.join(char.lower() for char in s if char.isalnum())

def map_products(products):
    mapped_products = {}
    
    for product in products:
        normalized_name = normalize_string(product['name'])
        
        best_match = None
        best_score = 0
        
        for mapped_name in mapped_products:
            score = fuzz.ratio(normalized_name, mapped_name)
            if score > best_score and score > 80:  # Adjust threshold as needed
                best_match = mapped_name
                best_score = score
        
        if best_match:
            mapped_products[best_match].append(product)
        else:
            mapped_products[normalized_name] = [product]
    
    return mapped_products