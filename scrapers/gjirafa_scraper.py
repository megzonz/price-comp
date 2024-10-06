import re
from scrapers.base_scraper import BaseScraper

class GjirafaScraper(BaseScraper):
    def __init__(self):
        super().__init__('https://gjirafa50.com')



    def search_products(self, query):
        page_number = 1
        all_products = []

        # Extract the company logo
        soup_main = self.get_page(self.base_url)
        logo_element = soup_main.select_one('img[title="Gjirafa50 KS"]')
        logo_url = logo_element.get('src', '').strip() if logo_element else None
        if logo_url and not logo_url.startswith('http'):
            logo_url = f"{self.base_url}{logo_url}"

        while True:
            search_url = f"{self.base_url}/{query}?pagenumber={page_number}"
            print(f"Scraping URL: {search_url}")
            soup = self.get_page(search_url)

            # Select all product items
            product_items = soup.select('div.item-box')
            if not product_items:
                print("No more products found.")
                break

            for product_item in product_items:
                # Extract product name and URL
                title_element = product_item.select_one('h3.product-title a')
                if not title_element:
                    continue

                name = title_element.get('title', '').strip()
                product_url = title_element.get('href', '')
                if product_url and not product_url.startswith('http'):
                    product_url = f"{self.base_url}{product_url}"

                # Extract the image source
                image_element = product_item.select_one('img')
                image_src = image_element.get('src', '').strip() if image_element else None

                # Extract and clean the price
                price_element = product_item.select_one('span.price.font-semibold')
                getting_price = price_element.text.strip() if price_element else '0.00'

                price = float(re.sub(r'[^\d.]', '', getting_price))

                


                # Create a dictionary for the product data
                product_data = {
                    'name': name,
                    'price': price,
                    'image_url': image_src,
                    'store_name': "Gjirafa50", 
                    'logo_url': logo_url,
                    'link_to_product': product_url,
                    'category_name': query  # Add category_name here
                }

                # Save the product to the database
                self.save_to_db(product_data)

                all_products.append(product_data)

            page_number += 1
        
        return all_products
