import requests
from bs4 import BeautifulSoup
import json
import time
import math
import pandas as pd
from datetime import date
# Function to extract the amount of pages per brand
def extract_nb_moto(brand):
    '''
    Downloads the total amount of motorcycles available for a certain brand.
    Additionally gives you the total amount of pages for that brand.
    
    Args:
    brand (str) : one of the available brands ['aprilia', 'bmw', 'buell', 'cagiva', 'ducati', 'harley-davidson', 'honda', 'husqvarna', 'hyosung', 'kawasaki', 'ktm', 'mash', 'moto-guzzi', 'mv-agusta', 'piaggio', 'royal-enfield','suzuki', 'triumph', 'yamaha']
    
    Returns: A dictionnary with the total number of motorcycles, amount of pages, the url link, and the brand.
    Example: {'amount_motorycle': 491,
  'amount_page': 17,
  'url': 'https://www.2dehands.be/l/motoren/motoren-ducati',
  'brand': 'ducati'}
  
    '''
    
    url_page = 'https://www.2dehands.be/l/motoren/motoren-' + brand
    r = requests.get(url_page, timeout=5)
    if r.status_code == 200:
        print('The status code of the request is 200')

        bs = BeautifulSoup(r.text,'html.parser')

        number_raw = bs.find('span', attrs = {'class' :'mp-Nav-breadcrumb-item'}).text
        number_raw = number_raw.replace('.','')
        number = number_raw.replace(' resultaten', '')
        number = int(number)

        moto_brand = brand

        nb2 = math.ceil(number/30) 

        dictionary = dict({'amount_motorycle':number,
                          'amount_page' : nb2,
                         'url' : url_page,
                          'brand' : moto_brand})
        
    else:
        print('We do not have access to the website at the moment')  
        dictionary = dict({})
    return dictionary
    


def create_url_list(list_number_pages):
    '''
    Function to create a list of URL per brand for all available pages.
    
    Args:
    list_number_pages (dict) : A list with of dictionnaries with the brand of the motorcycle and the associated amount of pages.
    
    Returns: a list with the right amount of URL for the pages of all the brands.
    example : 'https://www.2dehands.be/l/motoren/motoren-aprilia/p/7/#Language:all-languages|sortBy:SORT_INDEX|sortOrder:DECREASING'
    
    '''
    
    
    full_url_page = []
    part_0 = 'https://www.2dehands.be/l/motoren/motoren-'
    part_2 = '/p/'
    part_3 = '/#Language:all-languages|sortBy:SORT_INDEX|sortOrder:DECREASING'
    
    for j in list_number_pages:
        moto_brand = j['brand']
        amount_page = j['amount_page']
        for p in range(1,amount_page+1):
            link = part_0 +  str(moto_brand) +part_2 + str(p) + part_3
            full_url_page.append(link)
            
    return full_url_page


def extract_moto_id(page_link):
    '''
    Extracts all moto id from a single page (30, most common)
    
    Args:
    page_link (str) : The URL for the specific motorcycle page. 
    Example: https://www.2dehands.be/l/motoren/motoren-bmw/p/15/#Language:all-languages|sortBy:SORT_INDEX|sortOrder:DECREASING
    
    Returns: A list of all the motorcycle ID of the received page.
    For example, one element of the list: 'https://www.2dehands.be/m1829857488'
    
    
    '''
    r = requests.get(page_link)
    
    if r.status_code == 200:
        print('The status code of the request is 200')

    
        bs = BeautifulSoup(r.text,'html.parser')
        script = bs.find('script', type='application/json')
        json_file = json.loads(script.contents[0])
        number_of_motos = len(json_file['props']['pageProps']['searchRequestAndResponse']['listings'])

        list_id = []
        for j in range(0,number_of_motos):
            moto_id = json_file['props']['pageProps']['searchRequestAndResponse']['listings'][j]['itemId']
            moto_id = 'https://www.2dehands.be/' + moto_id
            list_id.append(moto_id)
            
    else:
        print('we failed to receive access to the website')
    
    return list_id