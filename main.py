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

commons = []
uncommons = []
rares = []
mythics = []

# Given a list of cards, sort them by rarity
def sort_categories(card_list):
    for card in card_list:
        if card['rarity'] == "common":
            commons.append(card)
        elif card['rarity'] == "uncommon":
            uncommons.append(card)
        elif card['rarity'] == "rare":
            rares.append(card)
        elif card['rarity'] == "mythic":
            mythics.append(card)



num_cards, card_list = read_url(url)

print(card_list[0]['card_faces'])

sort_rarity(card_list)
with open('mh3_cards.txt', 'w') as file:
    file.write("COMMONS\n")
    for i in range(0, len(commons)):
        card = commons[i]
        file.write(str(i+1) + ") " + card['name'] + " " + card['id'] + "\n")
    file.write("---------------------------------------------------------------------------")   
    for i in range(0, len(uncommon)):
        card = uncommons[i]
        file.write(str(i+1) + ") " + card['name'] + " " + card['id'] + "\n")
    file.write("---------------------------------------------------------------------------")     
    for i in range(0, len(rare)):
        card = rares[i]
        file.write(str(i+1) + ") " + card['name'] + " " + card['id'] + "\n")
    file.write("---------------------------------------------------------------------------")    

categories = {
    "mh3_commons" : None,
    "mh3_uncommmons" : None,
    "mdfc_uncommons" : None,
    "ntm_uncommons" : None,
    "mh3_rares" : None,
    "mh3_mythics" : None,
    "retro_mh3_rares" : None,
    "retro_mh3_mythics" : None,
    "retro_ntm_rares/mythics" : None,
    "retro_ntm_commons" : None,
    "retro_ntm_uncommons" : None,
    "borderless" : None,
    "borderless_ntm" : None,
    "profile_borderless" : None,
    "profile_ntm_borderless" : None,
    "framebreak_borderless" : None,
    "framebreak_ntm_borderless" : None,
}

