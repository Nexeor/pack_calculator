import json
import requests
import random

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
        name, url, foil = line.split(';')
        print("Reading from URL: " + url)
        url_cards_full = read_url(url)
        
        # Create a seperate list with only the needed information
        url_cards_simple = []
        for i in range(0, len(url_cards_full)):
            url_cards_simple.append((str(url_cards_full[i]['name'] + " #" + url_cards_full[i]['collector_number']), url_cards_full[i]['prices']))
        
        # Format the list correctly and add it to the larger set
        # TODO: Grab specific price (foil v nonfoil) rather than entire array
        full_category = { 'num_cards' : len(url_cards_full), 'cards' : url_cards_simple }
        set[name] = full_category

    # Write the set to a JSON file
    output.write(json.dumps(set, indent = 4))

def build_product(num_boosters, template_JSON, card_JSON):
    product = []
    for pack in range(num_boosters):
        product.append(build_pack(template_JSON, card_JSON))
    
    return product

# Given a pack_template JSON and a category JSON, build a pack
def build_pack(template_JSON, card_JSON):
    template = json.load(open(template_JSON, 'r'))
    card_list = json.load(open(card_JSON, 'r'))
    pack = []

    # Iterate over each slot
    for slot, data in template.items():
        # Select a card for each time the slot is repeated
        for i in range(data["num_slots"]):
            pack.append((slot, select_card(data["rng_table"], card_list)))
    
    pack_ev = 0.0
    print("\nNew Pack:")
    for card in pack:
        card_ev = card[1][1]['usd']
        if (card_ev == None):    
            card_ev = 0

        card_ev = round(float(card_ev), 4)
        print(card[1][0] + " worth " + str(card_ev))
        pack_ev += card_ev

    pack_ev = round(pack_ev, 4)
    print("total value: " + str(pack_ev))
    return pack

def select_card(rng_table, card_list):
    # Choose the category based on rng_table
    rng = random.random() * 100.0
    i = 0

    while rng > float(rng_table["chance"][i]):
        rng -= float(rng_table["chance"][i])
        i += 1

    category = rng_table["category"][i]

    # Randomly choose card from selected category 
    card = random.choice(card_list[category]["cards"])
    
    return card
    
category_file = 'mh3_categories.txt'
card_file = 'mh3_cards.json'
# organize_categories(category_file, card_file)
booster_box = build_product(36, 'mh3_pb_template.json', 'mh3_cards.json')