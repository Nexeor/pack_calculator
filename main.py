import json
import requests

# card_data: array of dicts, with each dict being a card
# page_data: dict with several elements, including an array of cards (card_data)
def read_url(url):
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        page_data = response.json()
        card_data = read_page(url, [])
        
        return page_data['total_cards'], card_data

    else:
        # Print an error message if the request was not successful
        print('Error:', response.status_code)

def read_page(url, card_data):
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        page_data = response.json()

        # Read the page and add it to json_data
        card_data.extend(page_data['data'])

        # If there is another page, call read_url again
        if page_data['has_more']:
            card_data = read_page(page_data['next_page'], card_data)
        
        return card_data

    else:
        # Print an error message if the request was not successful
        print('Error:', response.status_code)

commons = {}
uncommons = {}
rares = {}
mythics = {}

url = 'https://api.scryfall.com/cards/search?as=grid&order=name&q=%28game%3Apaper%29+set%3Amkm'
num_cards, card_list = read_url(url)

for card in card_list:
    print(card['name'])
