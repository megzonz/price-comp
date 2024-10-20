import json
import unittest
from database.database import insert_or_map_product
from scrapers.foleja_scraper import FolejaScraper
from scrapers.gjirafa_scraper import GjirafaScraper
from database.models import create_tables, Session

class TestGjirafaScraper(unittest.TestCase):

    def setUp(self):
        # Create the tables before each test
        create_tables()
        
        # Initialize the scraper
        self.scraper = GjirafaScraper()

        # Create a new database session for the test
        self.db = Session()

    def tearDown(self):
        # Close the session after each test
        self.db.close()

    def test_scrape_and_insert_data(self):
        # Load categories from gjirafa_categories.json
        with open('gjirafa_categories.json', 'r') as file:
            categories = json.load(file)
        
        updated_categories = []

        # Loop over all categories and scrape products
        for category in categories:
            category_url = category['category_url']
            print(f"Scraping category: {category_url}")
            
            # Call the search_products function for each category, passing the db session
            scraped_data = self.scraper.search_products(category_url, self.db)

            # Update category_url in case of a redirect
            if self.scraper.redirected_category_url:
                updated_category = {"category_url": self.scraper.redirected_category_url}
                updated_categories.append(updated_category)
            else:
                updated_categories.append(category)

            # Insert each product into the database (or map if it already exists)
            for product in scraped_data:
                # Ensure that each product has the expected fields
                self.assertIn('name', product)
                self.assertIn('base_name', product)
                self.assertIn('price', product)
                self.assertIn('image_url', product)
                self.assertIn('store_name', product)
                self.assertIn('link_to_product', product)
                self.assertIn('category_id', product)

                # Insert or map product into the database
                insert_or_map_product(product, self.db)

        # Save the updated categories back to the file (if any redirects happened)
        with open('gjirafa_categories.json', 'w') as file:
            json.dump(updated_categories, file, indent=4)

class TestFolejaScraper(unittest.TestCase):

    def setUp(self):
        # Create the tables before each test
        create_tables()
        
        # Initialize the scraper
        self.scraper = FolejaScraper()

        # Create a new database session for the test
        self.db = Session()

    def tearDown(self):
        # Close the session after each test
        self.db.close()

    def test_scrape_and_insert_data(self):
        # Use the given category path for Foleja
        category_url = "Teknologji/Celulare-Smartwatch/Celulare/Smartphone"
        
        print(f"Scraping category: {category_url}")
        
        # Call the search_products function for the given category, passing the db session
        scraped_data = self.scraper.search_products(category_url, self.db)

        # Insert each product into the database (or map if it already exists)
        for product in scraped_data:
            # Ensure that each product has the expected fields
            self.assertIn('name', product)
            self.assertIn('base_name', product)
            self.assertIn('price', product)
            self.assertIn('image_url', product)
            self.assertIn('store_name', product)
            self.assertIn('link_to_product', product)
            self.assertIn('category_id', product)

            # Insert or map product into the database
            insert_or_map_product(product, self.db)

if __name__ == '__main__':
    unittest.main()




# class TestMall75Scraper(unittest.TestCase):

#     def setUp(self):
#         self.scraper = Mall75Scraper()

#     def test_search_products(self):
#         category = "telefone-and-ora-te-mencura/telefone-mobil-al/smart-telefone-al"
#         scraped_data = self.scraper.search_products(category)

#         for product in scraped_data:
#             self.assertIn('name', product)
#             self.assertIn('price', product)
#             self.assertIn('image_url', product)
#             self.assertIn('store_name', product)
#             self.assertIn('link_to_product', product)
#             self.assertIn('logo_url', product)
#             self.assertIn('category_name', product)


