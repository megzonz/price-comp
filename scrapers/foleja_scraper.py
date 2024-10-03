from scrapers.base_scraper import BaseScraper

class FolejaScraper(BaseScraper):
    def __init__(self):
        super().__init__('https://www.foleja.com')

    def search_products(self, category_url, order='acris-score-desc'):
        """
        category_url: The URL part after the base domain for the category.
        order: The order parameter for sorting (default is 'acris-score-desc').
        """
        page_number = 1
        all_products = []

        while True:
            search_url = f"{self.base_url}/{category_url}/?order={order}&p={page_number}"
            print(f"Scraping URL: {search_url}")
            soup = self.get_page(search_url)

            # Select all product items
            product_items = soup.select('div.card.product-box.box-standard')
            if not product_items:
                print("No more products found.")
                break

            for product_item in product_items:
                # Extract product name and URL
                title_element = product_item.select_one('div.product-box-rating-name a')
                if not title_element:
                    continue

                name = title_element.get('title', '').strip()
                product_url = title_element.get('href', '')
                if product_url and not product_url.startswith('http'):
                    product_url = f"{self.base_url}{product_url}"

                # Extract the image source
                image_element = product_item.select_one('div.product-image-wrapper img')
                image_src = image_element.get('src', '').strip() if image_element else None

                # Extract the price
                price_element = product_item.select_one('span.decimal-rounded-price')
                price = price_element.text.strip() if price_element else 'Price not available'

                # Add the extracted data to the product list
                all_products.append({
                    'name': name,
                    'price': price,
                    'url': product_url,
                    'image': image_src
                })

            page_number += 1

        return all_products
