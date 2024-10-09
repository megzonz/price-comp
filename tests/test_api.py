# import requests
# from bs4 import BeautifulSoup
# import json

# # URL of the Gjirafa categories page
# url = 'https://gjirafa50.com/'

# # Make the request
# response = requests.get(url)
# if response.status_code == 200:
#     # Parse the page with BeautifulSoup
#     soup = BeautifulSoup(response.text, 'html.parser')

#     categories = []

#     # Find all <ul> elements with the class 'sublist second-level'
#     for ul in soup.find_all('ul', class_='sublist second-level'):
#         # Loop through all <li> elements inside each <ul>
#         for li in ul.find_all('li', class_='category-item'):
#             a_tag = li.find('a')

#             category_url = a_tag['href'].strip('/')  # Remove leading "/"
#             categories.append({"category_url": category_url})

#     # Save the results to a JSON file
#     with open('gjirafa_categories.json', 'w') as json_file:
#         json.dump(categories, json_file, indent=4)

#     print("Categories scraped and saved to gjirafa_categories.json")
# else:
#     print(f"Failed to retrieve the page. Status code: {response.status_code}")
