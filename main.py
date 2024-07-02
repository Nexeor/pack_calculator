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
    
# Given a list of URLS, read the cards from them and organize it in an output file
def organize_categories(input, output):
    input_file = open(input, 'r')
    output_file = open(output, 'a')
    
    for line in input_file:
        parsed = line.split(';')
        print(parsed[1])
        cards = read_url(parsed[1])
        output_file.write(parsed[0] + "("+ str(len(cards)) + ")" + '\n')

        for i in range(0, len(cards)):
            output_file.write(str(i + 1) + ") " + cards[i]['name'] + '\n')

category_file = 'mh3_categories.txt'
card_file = 'mh3_cards.txt'
organize_categories(category_file, card_file)
