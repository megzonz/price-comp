from bs4 import BeautifulSoup
import requests
from abc import ABC, abstractmethod
from database.database import insert_product

import sys
import os 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class BaseScraper(ABC):
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def get_page(self, url):
        response = self.session.get(url)
        response.raise_for_status()  
        return BeautifulSoup(response.text, 'html.parser') 


    def save_to_db(self, product_data):
        """
        Saves scraped product data to the database
        """
        try:
            insert_product(product_data)
        except Exception as e:
            print(f"Failed to save product: {e}")

    @abstractmethod
    def search_products(self, query):
        pass
