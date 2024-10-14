import requests
from scrapers.base_scraper import BaseScraper

class Mall75Scraper(BaseScraper):
    def __init__(self):
        super().__init__('https://www.75mall.com')

    def search_products(self, query):
        page_number = 1
        all_products = []
        logo_url = self._get_logo_url()

        while True:
            search_url = self._build_search_url(query, page_number)
            print(f"Scraping URL: {search_url}")

            try:
                soup = self.get_page(search_url)
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    print(f"Reached the end of pagination at page {page_number}.")
                    break
                else:
                    raise

            product_cards = soup.find_all('div', class_='ty-column4')
            if not product_cards:
                print("No more products found.")
                break

            for card in product_cards:
                price = self._extract_price(card)
                if price is None:
                    continue

                product_data = self._extract_product_data(card, logo_url, query, price)
                if product_data:
                    self.save_to_db(product_data)
                    all_products.append(product_data)

            page_number += 1

        return all_products

    def _get_logo_url(self):
        soup_main = self.get_page(self.base_url)
        if soup_main is None:
            print("Failed to retrieve the homepage. Logo URL will be set to None.")
            return None
        
        logo_tag = soup_main.find('img', class_='ty-pict', alt='75Mall')
        logo_url = logo_tag['src'] if logo_tag else None
        if logo_url and not logo_url.startswith('http'):
            logo_url = f"{self.base_url}{logo_url}"
        return logo_url

    def _build_search_url(self, query, page_number):
        return f"{self.base_url}/{query}/page-{page_number}/"

    def _extract_product_data(self, card, logo_url, query, price):
        try:
            name_element = card.find('a', class_='product-title')
            if not name_element:
                return None
            name = name_element.get('title', '').strip()

            product_link = name_element.get('href', '').strip()
            if product_link and not product_link.startswith('http'):
                product_link = f"{self.base_url}{product_link}"

            image_url = self._extract_image_url(card)

            return {
                'name': name,
                'price': price,
                'image_url': image_url,
                'store_name': "75Mall",
                'logo_url': logo_url,
                'link_to_product': product_link,
                'category_name': query
            }
        except AttributeError as e:
            print(f"Error processing a product card: {e}")
            return None

    def _extract_price(self, card):
        price_container = card.find('span', id=lambda x: x and x.startswith('discounted_price_'))
        if not price_container:
            return None

        try:
            main_price = price_container.contents[0].strip().replace(',', '')
            decimal_price = price_container.find('sup').text.strip() if price_container.find('sup') else '00'
            price_text = f"{main_price}.{decimal_price}"
            return float(price_text)
        except (IndexError, ValueError, AttributeError) as e:
            print(f"Error extracting price: {e}")
            return None

    def _extract_image_url(self, card):
        img_tag = card.find('img', class_='ty-pict')
        if not img_tag:
            return None

        if 'data-srcset' in img_tag.attrs:
            srcset = img_tag['data-srcset']
            return srcset.split(',')[0].strip().split(' ')[0]
        elif 'srcset' in img_tag.attrs:
            srcset = img_tag['srcset']
            return srcset.split(',')[0].strip().split(' ')[0]
        elif 'src' in img_tag.attrs and not img_tag['src'].startswith('data:'):
            return img_tag['src']

        return None