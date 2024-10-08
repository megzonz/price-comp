import re
from scrapers.base_scraper import BaseScraper

class Mall75Scraper(BaseScraper):
    def __init__(self):
        super().__init__('https://www.75mall.com')

    def search_products(self, query):
        page_number = 1
        all_products = []

        # Extract the company logo
        soup_main = self.get_page(self.base_url)
        logo_tag = soup_main.find('img', class_='ty-pict', alt='75Mall')
        logo_url = logo_tag['src'] if logo_tag else None
        if logo_url and not logo_url.startswith('http'):
            logo_url = f"{self.base_url}{logo_url}"

        while True:
            search_url = f"{self.base_url}/{query}/page-{page_number}/"
            print(f"Scraping URL: {search_url}")
            soup = self.get_page(search_url)

            # Select all product items
            product_cards = soup.find_all('div', class_='ty-column4')
            if not product_cards:
                print("No more products found.")
                break

            for card in product_cards:
                try:
                    # Product name
                    name_element = card.find('a', class_='product-title')
                    if not name_element:
                        continue
                    name = name_element.get('title', '').strip()

                    # Product link
                    product_link = name_element.get('href', '').strip()
                    if product_link and not product_link.startswith('http'):
                        product_link = f"{self.base_url}{product_link}"

                    # Extract the price container by targeting the span with a specific ID pattern
                    price_container = card.find('span', id=lambda x: x and x.startswith('discounted_price_'))

                    if price_container:
                        # Get the full price text and clean it
                        price_text = price_container.get_text(strip=True)
                        price_text = re.sub(r'[^\d.,]', '', price_text).replace(',', '.')
                        try:
                            price = float(price_text)
                        except ValueError:
                            price = 0.0
                    else:
                        price = 0.0

                    # Extract image URL
                    img_tag = card.find('img', class_='ty-pict')
                    image_url = None
                    if img_tag:
                        if 'data-srcset' in img_tag.attrs:
                            srcset = img_tag['data-srcset']
                            image_url = srcset.split(',')[0].strip().split(' ')[0]
                        elif 'srcset' in img_tag.attrs:
                            srcset = img_tag['srcset']
                            image_url = srcset.split(',')[0].strip().split(' ')[0]
                        elif 'src' in img_tag.attrs and not img_tag['src'].startswith('data:'):
                            image_url = img_tag['src']
                    if image_url and not image_url.startswith('http'):
                        image_url = f"{self.base_url}{image_url}"

                    # Create a dictionary for the product data
                    product_data = {
                        'name': name,
                        'price': price,
                        'image_url': image_url,
                        'store_name': "75Mall", 
                        'logo_url': logo_url,
                        'link_to_product': product_link,
                        'category_name': query 
                    }

                    # Save the product to the database
                    self.save_to_db(product_data)

                    all_products.append(product_data)
                except AttributeError as e:
                    print(f"Error processing a product card: {e}")

            page_number += 1

        return all_products
