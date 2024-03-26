import json
import requests

def read_page(json_data, card_count):
    # Print the response data (usually JSON)
    for i in range(0, len(json_data['data'])):
        card_count += 1
        card = json_data['data'][i]
        print("Card", card_count, "out of", json_data['total_cards'], card['name'])
    
    return card_count

def read_url(url, card_count):
    response = requests.get(url)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Print the response data (usually JSON)
        json_data = response.json()
        card_count = read_page(json_data, card_count)

        if (json_data['has_more']):
            read_url(json_data['next_page'], card_count)

    else:
        # Print an error message if the request was not successful
        print('Error:', response.status_code)

url = 'https://api.scryfall.com/cards/search?as=grid&order=name&q=%28game%3Apaper%29+set%3Amkm'
read_url(url, 0)