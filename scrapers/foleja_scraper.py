from scrapers.base_scraper import BaseScraper
from database.models import Category

class FolejaScraper(BaseScraper):
    def __init__(self):
        super().__init__('https://www.foleja.com')

    def search_products(self, category_url, db, order='acris-score-desc'):
        page_number = 1
        all_products = []
        logo_url = self._get_logo_url()

        category = self._get_or_create_category(category_url, db)
        category_id = category.id

        while True:
            search_url = self._build_search_url(category_url, order, page_number)
            print(f"Scraping URL: {search_url}")
            soup = self.get_page(search_url)

            if soup is None:
                print("Failed to retrieve the page. Stopping scraping.")
                break

            product_items = soup.select('div.card.product-box.box-standard')
            if not product_items:
                print("No more products found.")
                break

            for product_item in product_items:
                price = self._extract_price(product_item)
                if price is None:
                    continue

                product_data = self._extract_product_data(product_item, category_id, logo_url, price)
                if product_data:
                    self.save_to_db(product_data, db)
                    all_products.append(product_data)

            page_number += 1

        return all_products

    def _get_logo_url(self):
        homepage_soup = self.get_page(self.base_url)
        if homepage_soup is None:
            print("Failed to retrieve the homepage. Logo URL will be set to None.")
            return None
        
        logo_element = homepage_soup.select_one('picture.header-logo-picture img')
        logo_url = logo_element.get('src', '').strip() if logo_element else None
        if logo_url and not logo_url.startswith('http'):
            logo_url = f"{self.base_url}{logo_url}"
        return logo_url

    def _get_or_create_category(self, category_url, db):
        category = db.query(Category).filter_by(category_url=category_url).first()
        if not category:
            category = Category(category_url=category_url)
            db.add(category)
            db.commit()
        return category

    def _build_search_url(self, category_url, order, page_number):
        return f"{self.base_url}/{category_url}/?order={order}&p={page_number}"

    def _extract_product_data(self, product_item, category_id, logo_url, price):
        title_element = product_item.select_one('div.product-box-rating-name a')
        if not title_element:
            return None

        name = title_element.get('title', '').strip()
        product_url = title_element.get('href', '')
        if product_url and not product_url.startswith('http'):
            product_url = f"{self.base_url}{product_url}"

        image_element = product_item.select_one('div.product-image-wrapper img')
        image_src = image_element.get('src', '').strip() if image_element else None

        return {
            'name': name,
            'price': price,
            'image_url': image_src,
            'store_name': "Foleja",
            'logo_url': logo_url,
            'link_to_product': product_url,
            'category_id': category_id
        }

    def _extract_price(self, product_item):
        price_container = product_item.select_one('div.d-flex')
        if not price_container:
            return None

        try:
            whole_price_element = price_container.contents[2].strip().replace(',', '')
            decimal_price_element = price_container.select_one('span.decimal-rounded-price')
            decimal_price = decimal_price_element.text.strip() if decimal_price_element else '00'
            price_text = f"{whole_price_element}.{decimal_price}"
            return float(price_text.strip())
        except (IndexError, ValueError, AttributeError) as e:
            print(f"Error extracting price: {e}")
            return None