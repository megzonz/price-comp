from bs4 import BeautifulSoup
import requests
from abc import ABC, abstractmethod

class BaseScraper(ABC):
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def get_page(self, url):
        response = self.session.get(url)
        response.raise_for_status()  
        return BeautifulSoup(response.text, 'html.parser') 


    @abstractmethod
    def search_products(self, query):
        pass
