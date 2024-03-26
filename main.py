import json
import requests


def read_url(url, json_data):
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        page = response.json()
        if (json_data is {}):
            json_data.update(page['total_cards'])
        
        # Read the page and add it to json_data
        json_data.update(page)

        # If there is another page, call read_url again
        if json_data['has_more']:
            json_data = read_url(json_data['next_page'], json_data)
        
        return json_data

    else:
        # Print an error message if the request was not successful
        print('Error:', response.status_code)

url = 'https://api.scryfall.com/cards/search?as=grid&order=name&q=%28game%3Apaper%29+set%3Amkm'
data = read_url(url, {})
print(data['total_cards'])