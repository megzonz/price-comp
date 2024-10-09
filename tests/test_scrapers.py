import json
import unittest
from scrapers.gjirafa_scraper import GjirafaScraper  
from database.models import create_tables  

class TestGjirafaScraper(unittest.TestCase):

    def setUp(self):
        # Create the tables before each test
        create_tables()
        
        # Initialize the scraper
        self.scraper = GjirafaScraper()

    def test_scrape_all_categories(self):
        # Load categories from gjirafa_categories.json
        with open('gjirafa_categories.json', 'r') as file:
            categories = json.load(file)
        
        updated_categories = []

        # Loop over all categories and scrape products
        for category in categories:
            category_url = category['category_url']
            print(f"Scraping category: {category_url}")
            
            # Call the search_products function for each category
            scraped_data = self.scraper.search_products(category_url)

            # Update category_url in case of a redirect
            if self.scraper.redirected_category_url:
                updated_category = {"category_url": self.scraper.redirected_category_url}
                updated_categories.append(updated_category)
            else:
                updated_categories.append(category)

            # Print the output for inspection
            print(f"Scraped Data for category '{category_url}':")
            for product in scraped_data:
                print(product)

            # Optional: Check if the scraped data contains expected fields
            for product in scraped_data:
                self.assertIn('name', product)
                self.assertIn('price', product)
                self.assertIn('image_url', product)
                self.assertIn('store_name', product)
                self.assertIn('link_to_product', product)

        # Save the updated categories back to the file
        with open('gjirafa_categories.json', 'w') as file:
            json.dump(updated_categories, file, indent=4)


if __name__ == "__main__":
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


# # tests/test_scrapers.py

# import unittest
# from scrapers.foleja_scraper import FolejaScraper
# from scrapers.gjirafa_scraper import GjirafaScraper
# from scrapers.mall75_scraper import Mall75Scraper
# from database.models import create_tables, engine

# class TestFolejaScraper(unittest.TestCase):

#     def setUp(self):
#         # Create the tables before each test
#         create_tables()
        
#         # Initialize the scraper
#         self.scraper = FolejaScraper()

#     def test_search_products(self):
#         # Define the product you want to scrape
#         category = "Teknologji/Celulare-Smartwatch/Celulare/Smartphone"

#         # Call the search_products function
#         scraped_data = self.scraper.search_products(category)

#         # Print the output for inspection
#         print("Scraped Data:")
#         for product in scraped_data:
#             print(product)

#         # Optional: Check if the scraped data contains expected fields
#         for product in scraped_data:
#             self.assertIn('name', product)
#             self.assertIn('price', product)
#             self.assertIn('image_url', product)
#             self.assertIn('store_name', product)
#             self.assertIn('link_to_product', product)