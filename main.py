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
def organize_categories(input, output, categories):
    input_file = open(input, 'r')
    output_file = open(output, 'w')
    out = {}
    
    for line in input_file:
        # Parse the category/URL and gather the card list
        parsed = line.split(';')
        category_name = parsed[0]
        print("Reading from URL: " + parsed[1])
        cards = read_url(parsed[1])
        
        # Create a dict out of the gathered cards
        category = []
        for i in range(0, len(cards)):
            category.append(cards[i]['name'])
        
        full_category = { 'num_cards' : len(cards), 'cards' : category }
        print(full_category)
        out[category_name] = full_category

    # Write the dict as a JSON file 
    # output_file.write(json.dumps({categories}, indent=4))
    print(json.dumps(out, indent = 4))


category_file = 'mh3_categories.txt'
card_file = 'mh3_cards.txt'
categories = {}
organize_categories(category_file, card_file, categories)
