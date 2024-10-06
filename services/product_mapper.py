from fuzzywuzzy import process

class CategoryMapper:
    def __init__(self, gjirafa_categories):
        self.gjirafa_categories = gjirafa_categories  
        
    def get_best_match(self, foleja_category):
        match, score = process.extractOne(foleja_category, self.gjirafa_categories)
        return match if score >= 80 else None  