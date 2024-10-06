from scrapers.gjirafa_scraper import GjirafaScraper
from scrapers.foleja_scraper import FolejaScraper
from database.database import clear_old_data, insert_product, create_tables  # Import the necessary functions

def scrape_and_update_gjirafa(category_name):
    # Clear old data for the category
    clear_old_data(category_name)

    # Initialize the Gjirafa scraper and perform the search
    gjirafa_scraper = GjirafaScraper()
    products = gjirafa_scraper.search_products(category_name)

    # Insert new products into the database
    for product_data in products:
        insert_product(product_data) 

    print("Gjirafa scraping completed.")

def scrape_and_update_foleja(category_name):
    # Clear old data for the category
    clear_old_data(category_name)

    # Initialize the Foleja scraper and perform the search
    foleja_scraper = FolejaScraper()
    products = foleja_scraper.search_products(category_name, order='acris-score-desc')

    # Insert new products into the database
    for product_data in products:
        insert_product(product_data)  # Make sure to adapt the product_data structure as needed

    print("Foleja scraping completed.")

if __name__ == "__main__":
    create_tables()
    scrape_and_update_gjirafa('gaming-maus')
    scrape_and_update_foleja('Teknologji/Kompjuter-Laptop-Tablet/Gaming/Maus')
