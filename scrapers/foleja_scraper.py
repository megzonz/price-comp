from scrapers.base_scraper import BaseScraper

class FolejaScraper(BaseScraper):
    def __init__(self):
        super().__init__('https://www.foleja.com')

    def search_products(self, category_url, order='acris-score-desc'):
        page_number = 1
        all_products = []

        # Scrape the logo of the website
        homepage_soup = self.get_page(self.base_url)
        logo_element = homepage_soup.select_one('picture.header-logo-picture img')
        logo_url = logo_element.get('src', '').strip() if logo_element else None
        if logo_url and not logo_url.startswith('http'):
            logo_url = f"{self.base_url}{logo_url}"

        while True:
            search_url = f"{self.base_url}/{category_url}/?order={order}&p={page_number}"
            print(f"Scraping URL: {search_url}")
            soup = self.get_page(search_url)

            product_items = soup.select('div.card.product-box.box-standard')
            if not product_items:
                print("No more products found.")
                break

            for product_item in product_items:
                title_element = product_item.select_one('div.product-box-rating-name a')
                if not title_element:
                    continue

                name = title_element.get('title', '').strip()
                product_url = title_element.get('href', '')
                if product_url and not product_url.startswith('http'):
                    product_url = f"{self.base_url}{product_url}"

                image_element = product_item.select_one('div.product-image-wrapper img')
                image_src = image_element.get('src', '').strip() if image_element else None

                # Extract the price
                price_container = product_item.select_one('div.d-flex')
                if price_container:
                    currency_symbol = price_container.select_one('span.currency-symbol')
                    currency = currency_symbol.text.strip() if currency_symbol else ''

                    # Handle whole and decimal parts
                    try:
                        whole_price_element = price_container.contents[2].strip()
                        decimal_price_element = price_container.select_one('span.decimal-rounded-price')
                        decimal_price = decimal_price_element.text.strip() if decimal_price_element else '00'
                        price_text = f"{whole_price_element}.{decimal_price}"  # No currency symbol here
                        price = float(price_text.replace(',', '.').strip())  # Convert to float
                    except (IndexError, ValueError) as e:
                        print(f"Error extracting price: {e}")
                        price = 0.00  # Default price when not available
                else:
                    price = 0.00  # Default price when not available

                # Create a dictionary for the product data
                product_data = {
                    'name': name,
                    'price': price,
                    'image_url': image_src,
                    'store_name': "Foleja",  
                    'logo_url': logo_url,
                    'category_name': category_url,
                    'link_to_product': product_url
                }

                # Save the product to the database
                self.save_to_db(product_data)

                # Add to all_products for return if needed
                all_products.append(product_data)

            page_number += 1

        return all_products
