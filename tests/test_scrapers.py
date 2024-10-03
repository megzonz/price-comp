from scrapers.gjirafa_scraper import GjirafaScraper
from scrapers.foleja_scraper import FolejaScraper

# if __name__ == "__main__":
#     scraper = GjirafaScraper()
#     products = scraper.search_products('apple-watch')

#     # Print the scraped products
#     for product in products:
#         print(f"Name: {product['name']}")
#         print(f"Price: {product['price']}")
#         print(f"URL: {product['url']}")
#         print(f"Image: {product['image']}")  # Print the image source
#         print('---')

if __name__ == "__main__":
    scraper = FolejaScraper()
    products = scraper.search_products('Teknologji/Kompjuter-Laptop-Tablet/Gaming/Tastiere', order='acris-score-desc')

    # Print the scraped products
    for product in products:
        print(f"Name: {product['name']}")
        print(f"Price: {product['price']}")
        print(f"URL: {product['url']}")
        print(f"Image: {product['image']}")  # Print the image source
        print('---')
