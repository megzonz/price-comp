import re
from scrapers.base_scraper import BaseScraper

class StartechScraper(BaseScraper):
    def __init__(self):
        super().__init__('https://startech24.com')  # Base URL for Startech

    def search_products(self, query):
        page_number = 1
        all_products = []

        # Extract the company logo
        soup_main = self.get_page(self.base_url)
        logo_element = soup_main.select_one('img[alt="Startech"]')  # Adjusted selector for logo
        logo_url = logo_element.get('src', '').strip() if logo_element else None
        if logo_url and not logo_url.startswith('http'):
            logo_url = f"{self.base_url}{logo_url}"

        while True:
            search_url = f"{self.base_url}/{query}/page/{page_number}"  # Adjust the URL based on Startech's structure
            print(f"Scraping URL: {search_url}")
            soup = self.get_page(search_url)

            # Select the product containers by ID "brxe-wonecs"
            product_items = soup.select('div#brxe-wonecs')  # Target the div with id "brxe-wonecs"
            print(f"Found {len(product_items)} product items on the page.")
            print(product_items)  # Debug: print the list of product items

            if not product_items:
                print("No more products found.")
                break

            for product_item in product_items:
                # Extract product name and URL
                title_element = product_item.select_one('h3.product-title a')
                if not title_element:
                    continue

                name = title_element.get_text(strip=True)
                product_url_element = product_item.select_one('a')
                product_url = product_url_element.get('href', '')
                if product_url and not product_url.startswith('http'):
                    product_url = f"{self.base_url}{product_url}"

                # Extract the image source
                image_element = product_item.select_one('img')  # Assuming the image is in img tag
                image_src = image_element.get('src', '').strip() if image_element else None

                # Extract and clean the price
                price_element = product_item.select_one('span.price')  # Adjusted for price
                if price_element:
                    price_text = price_element.get_text(strip=True)
                    price = float(re.sub(r'[^\d.]', '', price_text))  # Clean up price string
                else:
                    price = 0.00  # Fallback price if not found

                # Create a dictionary for the product data
                product_data = {
                    'name': name,
                    'price': price,
                    'image_url': image_src,
                    'store_name': "Startech",  # Name of the store
                    'logo_url': logo_url,  # Store logo URL
                    'link_to_product': product_url,
                    'category_name': query  # Add category_name here
                }

                # Print the product data to inspect it
                print(f"Scraped Product: {product_data}")

                # Save the product to the database
                self.save_to_db(product_data)

                all_products.append(product_data)

            # Save the HTML content of the page to inspect what is being scraped
            with open(f"startech_page_{page_number}.html", "w", encoding="utf-8") as f:
                f.write(str(soup))

            page_number += 1

        return all_products
