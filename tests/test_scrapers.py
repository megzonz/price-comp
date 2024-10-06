# tests/test_scrapers.py

import unittest
from scrapers.foleja_scraper import FolejaScraper
from scrapers.gjirafa_scraper import GjirafaScraper
from database.models import create_tables, engine  # Import the create_tables function and engine

class TestFolejaScraper(unittest.TestCase):

    def setUp(self):
        # Create the tables before each test
        create_tables()
        
        # Initialize the scraper
        self.scraper = FolejaScraper()

    def test_search_products(self):
        # Define the product you want to scrape
        product_name = "Teknologji/Celulare-Smartwatch/Celulare/Smartphone"

        # Call the search_products function
        scraped_data = self.scraper.search_products(product_name)

        # Print the output for inspection
        print("Scraped Data:")
        for product in scraped_data:
            print(product)

        # Optional: Check if the scraped data contains expected fields
        for product in scraped_data:
            self.assertIn('name', product)
            self.assertIn('price', product)
            self.assertIn('image_url', product)
            self.assertIn('store_name', product)
            self.assertIn('link_to_product', product)

class TestGjirafaScraper(unittest.TestCase):

    def setUp(self):
        # Create the tables before each test
        create_tables()
        
        # Initialize the scraper
        self.scraper = GjirafaScraper()

    def test_search_products(self):
        # Define the product you want to scrape
        product_name = "celular"

        # Call the search_products function
        scraped_data = self.scraper.search_products(product_name)

        # Print the output for inspection
        print("Scraped Data:")
        for product in scraped_data:
            print(product)

        # Optional: Check if the scraped data contains expected fields
        for product in scraped_data:
            self.assertIn('name', product)
            self.assertIn('price', product)
            self.assertIn('image_url', product)
            self.assertIn('store_name', product)
            self.assertIn('link_to_product', product)

if __name__ == "__main__":
    unittest.main()
