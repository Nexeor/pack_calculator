import json
import requests

# card_data: array of dicts, with each dict being a card
# page_data: dict with several elements, including an array of cards (card_data)
def read_url(url):
    collected_data = []
    url_data = read_page(url)
    collected_data.extend(url_data['data'])

    while url_data['has_more']:
        url_data = read_page(url_data['next_page'])
        collected_data.extend(url_data['data'])

    return collected_data

# Given a URL, return the cards  
def read_page(url):
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        page_data = response.json()
        return(page_data)

    else:
        # Print an error message if the request was not successful
        print('Error:', response.status_code)
        return None


card_list = read_url('https://api.scryfall.com/cards/search?q=+set%3Amh3+r%3Ac+-type%3Abasic&unique=cards&as=grid&order=name')
for i in range(1, len(card_list) + 1):
    print(str(i) + ") " + card_list[i - 1]['name'])
