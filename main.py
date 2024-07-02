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
    
# Given a list of URLs, read the cards from them and organize it in a JSON file
def organize_categories(input_file, output_file):
    input = open(input_file, 'r')
    output = open(output_file, 'w')
    set = {}
    
    for line in input:
        # Parse the category/URL to gather the card list
        print(line.split(';'))
        name, url = line.split(';')
        print("Reading from URL: " + url)
        url_cards_full = read_url(url)
        
        # Create a seperate list with only the needed information
        url_cards_simple = []
        for i in range(0, len(url_cards_full)):
            url_cards_simple.append(url_cards_full[i]['name'])
        
        # Format the list correctly and add it to the larger set
        full_category = { 'num_cards' : len(url_cards_full), 'cards' : url_cards_simple }
        set[name] = full_category

    # Write the set to a JSON file
    output.write(json.dumps(set, indent = 4))


category_file = 'mh3_categories.txt'
card_file = 'mh3_cards.json'
organize_categories(category_file, card_file)
