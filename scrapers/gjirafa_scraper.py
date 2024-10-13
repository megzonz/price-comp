import re
from scrapers.base_scraper import BaseScraper

class GjirafaScraper(BaseScraper):
    def __init__(self):
        super().__init__('https://gjirafa50.com')
        self.redirected_category_url = None  # Initialize redirected_category_url

    def search_products(self, query, db):
        page_number = 1
        all_products = []
        category_url = query  # Start with the original category URL

        # Extract the company logo
        soup_main = self.get_page(self.base_url)
        logo_element = soup_main.select_one('img[title="Gjirafa50 KS"]')
        logo_url = logo_element.get('src', '').strip() if logo_element else None
        if logo_url and not logo_url.startswith('http'):
            logo_url = f"{self.base_url}{logo_url}"

        while True:
            search_url = f"{self.base_url}/{category_url}?pagenumber={page_number}&orderby=&hls=false&is=true"
            print(f"Scraping URL: {search_url}")
            response = self.session.get(search_url)

            # Handle redirect if it occurs
            if response.url != search_url:
                new_url = response.url.replace(self.base_url, '').split('?')[0].strip('/')
                print(f"Redirect detected! Updating category_url to: {new_url}")
                self.redirected_category_url = new_url
                category_url = new_url
            else:
                self.redirected_category_url = None  

            soup = self.get_page(search_url)

            # Select all product items
            product_items = soup.select('div.item-box')
            if not product_items:
                print("No more products found.")
                break

            for product_item in product_items:
                # Check if the product is marked as "outlet"
                outlet_element = product_item.select_one('i.icon-outlet')
                if outlet_element:
                    print("Skipping outlet product.")
                    continue  # Skip this product if it's marked as "outlet"

                # Extract product name and URL
                title_element = product_item.select_one('h3.product-title a')
                if not title_element:
                    continue

                name = title_element.get('title', '').strip()
                product_url = title_element.get('href', '')
                if product_url and not product_url.startswith('http'):
                    product_url = f"{self.base_url}{product_url}"

                # Extract the image source
                image_element = product_item.select_one('section.picture img')  # More specific selector
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
                    'category_name': category_url  
                }

                # Save the product to the database using BaseScraper's save_to_db
                self.save_to_db(product_data, db)

                all_products.append(product_data)

            page_number += 1

        return all_products
