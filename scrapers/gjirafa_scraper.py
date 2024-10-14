import re
from scrapers.base_scraper import BaseScraper

class GjirafaScraper(BaseScraper):
    def __init__(self):
        super().__init__('https://gjirafa50.com')
        self.redirected_category_url = None

    def search_products(self, category_url, category_id, db):
        page_number = 1
        all_products = []
        logo_url = self._get_logo_url()

        while True:
            search_url = self._build_search_url(category_url, page_number)
            print(f"Scraping URL: {search_url}")
            response = self.session.get(search_url)

            # Handle redirect if it occurs
            category_url = self._handle_redirect(response, search_url, category_url)

            soup = self.get_page(search_url)
            product_items = soup.select('div.item-box')
            
            if not product_items:
                print("No more products found.")
                break

            for product_item in product_items:
                product_data = self._extract_product_data(product_item, category_id, logo_url)
                if product_data:
                    self.save_to_db(product_data, db)
                    all_products.append(product_data)

            page_number += 1

        return all_products

    def _get_logo_url(self):
        """Extract the company logo URL from the main page."""
        soup_main = self.get_page(self.base_url)
        logo_element = soup_main.select_one('img[title="Gjirafa50 KS"]')
        logo_url = logo_element.get('src', '').strip() if logo_element else None
        if logo_url and not logo_url.startswith('http'):
            logo_url = f"{self.base_url}{logo_url}"
        return logo_url

    def _build_search_url(self, category_url, page_number):
        """Construct the search URL for the given category and page number."""
        return f"{self.base_url}/{category_url}?pagenumber={page_number}&orderby=&hls=false&is=true"

    def _handle_redirect(self, response, search_url, category_url):
        """Handle redirects if they occur and update the category URL."""
        if response.url != search_url:
            new_url = response.url.replace(self.base_url, '').split('?')[0].strip('/')
            print(f"Redirect detected! Updating category_url to: {new_url}")
            self.redirected_category_url = new_url
            return new_url
        else:
            self.redirected_category_url = None
            return category_url

    def _extract_product_data(self, product_item, category_id, logo_url):
        """Extract product data from a product item element."""
        # Check if the product is marked as "outlet"
        if product_item.select_one('i.icon-outlet'):
            print("Skipping outlet product.")
            return None

        # Extract product name and URL
        title_element = product_item.select_one('h3.product-title a')
        if not title_element:
            return None

        name = title_element.get('title', '').strip()
        product_url = title_element.get('href', '')
        if product_url and not product_url.startswith('http'):
            product_url = f"{self.base_url}{product_url}"

        # Extract the image source
        image_element = product_item.select_one('section.picture img')
        image_src = image_element.get('src', '').strip() if image_element else None

        # Extract and clean the price
        price_element = product_item.select_one('span.price.font-semibold')
        getting_price = price_element.text.strip() if price_element else '0.00'
        price = float(re.sub(r'[^\d.]', '', getting_price))

        # Create a dictionary for the product data
        return {
            'name': name,
            'price': price,
            'image_url': image_src,
            'store_name': "Gjirafa50",
            'logo_url': logo_url,
            'link_to_product': product_url,
            'category_id': category_id
        }