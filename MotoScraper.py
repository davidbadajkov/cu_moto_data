import requests
from bs4 import BeautifulSoup
import json
import time
import math
import pandas as pd
from datetime import date
import requests
from requests_ip_rotator import ApiGateway, EXTRA_REGIONS

from TopSecret import AWS_ACCESS_KEY_ID
from TopScret import AWS_SECRET_ACCESS_KEY

gateway = ApiGateway(site="https://www.2dehands.be/", access_key_id = AWS_ACCESS_KEY_ID, access_key_secret = AWS_SECRET_ACCESS_KEY)
gateway.start()
session = requests.Session()
session.mount("https://www.2dehands.be/", gateway)



class MotoDownloader:
    '''
    Download manager class for https://www.2dehands.be
    
    It contains methods for collection of characteristics of a given motorcycle id and stores the results.
    '''
    def __init__(self):
        '''
        Creates MotoDownload object with self.link , self.request, and self.bs to store necessary objects to perform the data collection.
        
        Additionnally it has self.maint_attributes, ... self.image to store the motorcycle characteristics.
        
        '''
        self.link = None
        self.request = None
        self.bs = None
        
        self.main_attributes = None
        self.extra_attributes = None
        self.text = None
        self.brand = None
        self.id = None
        self.extracted_date = None
        self.price = None
        self.location = None
        self.seller_name = None
        self.image = None
        
        
    def get_soup(self,moto_url):
        '''
        Make a GET request to the website.
        Creates a BeautifulSoup object to allow for easier data extraction.
        
        Args (str) : URL of a specific motorycle. Example : https://www.2dehands.be/m1818452499
        
        Returns: Nothing
        '''
        self.link = moto_url
        self.request = session.get(moto_url)
        self.request.encoding = 'UTF-8'
        self.bs = BeautifulSoup(self.request.text,'html.parser')
        
    def get_main_attributes(self):
        '''
        A method that extracts the main attributes of the motorcycle.
        
        Returns: A dictionary with the key attributes of the motorcycle.
        '''
        list_attributes_value = self.bs.findAll('span', attrs =
                {'class' : 'Attributes-value'})

        list_attributes_label = self.bs.findAll('strong', attrs =
                {'class' : 'Attributes-label'})


        res_label = [i.text for i in list_attributes_label]
        res_value = [i.text for i in list_attributes_value]

        dictionnary = dict(zip(res_label,res_value))
        
        self.main_attributes = dictionnary

        return dictionnary
    
    def get_extra_attributes(self):
        '''
        A method that extracts the extra attributes of the motorcycle.
        
        Returns: A dictionary with the extra attributes of the motorcycle.
        '''
        add_char = self.bs.find('div', 
                                attrs = {'class' : 'Stats-root'})
        head_stat_summary = add_char.find_all('span', {'class' : 'Stats-summary'})
        viewed = head_stat_summary[0].text
        liked = head_stat_summary[1].text
        posted = head_stat_summary[2].text

        title = self.bs.find('h1',
               attrs = {'class' : 'Listing-title'}).text.strip()

        dictionary = dict({'viewed':viewed,
              'liked':liked,
              'posted':posted,
              'title':title})
        
        self.extra_attributes = dictionary

        return dictionary


    def get_text(self):
        '''
        A method that extracts the text description of the motorcycle.
        
        Returns: A dictionary with the text description of the motorcycle.
        '''
        text_description = self.bs.find('div', attrs = {'class' : 'Description-description'}).text
        text = dict({'description' : text_description})
        self.text = text
        return text

    def get_brand(self):
        
        '''
        A method that extracts the brand of the motorcycle from the BeautifulSoup object.
        
        Returns: A dictionary with the brand of the motorcycle.
        '''
        
        
        brand = self.bs.findAll('nav',
                attrs = {'class': 'Breadcrumbs-root'})[0].findAll('a',
                                                               attrs = {'class': 'hz-Link'})[2].text

        brand = brand.replace('Motoren | ','')
        
        brand = dict({'brand' : brand})

        self.brand = brand
        return brand
    
    def get_id(self):
        '''
        Method that creates a dictionary with the link of the given motorcycle.
        
        Returns: Dictionary with moto id.
        
        '''
        moto_id = dict({'id' : self.link})
        self.id = moto_id
        return moto_id
    
    def get_extracted_date(self):
        
        '''
        Method that creates a datetime object of the day the data was extracted.
        
        Returns: A dictionary with the date when the data was collected for the specific motorcycle.
        '''
        today = dict({'extracted_on' : date.today()})
        self.extracted_date = today
        return today
    def get_price(self):
        
        '''
        Method that extracts the price of the specific motorcycle from the BeautifulSoup object.
        
        Returns: A dictionary with the price of the specific motorcycle.
        '''
        
        price = self.bs.find('div',
                            attrs = {'class' : "Listing-price"}).text.strip().replace('€\xa0','').replace('.','').replace(',','')
        price_dict = dict({'price_eur':price})
        self.price = price_dict
        return price_dict
    
    def get_location(self):
        '''
        Method that extracts the location of the specific motorcycle from the BeautifulSoup object.
        
        Returns: A dictionary with the location of the specific motorcycle.
        '''
        location = self.bs.find('div',
                                attrs = {'class':'SellerInfo-rowWithIcon'}).text
        
        location_dict = dict({'location' : location})
        
        self.location = location_dict

        
        return location_dict
    
    def get_seller_name(self):
        
        '''
        Method that extracts the seller name of the specific motorcycle from the BeautifulSoup object.
        
        Returns: A dictionary with the seller name of the specific motorcycle.
        '''
        
        seller_name = self.bs.find('span',
                                   attrs = {'class':'SellerInfo-name'}).text
        
        
        seller_name_dict = dict({'seller_name' : seller_name })
        
        self.seller_name = seller_name_dict

        
        return seller_name_dict
    
    def get_image(self):
        
        '''
        Method that extracts all the available links of the specific motorcycle images, from the BeautifulSoup object.
        
        Returns: A dictionary with all the available links of the specific motorcycle images.
        '''
        
        image_all = self.bs.findAll('span',
                       attrs = {'class':'Thumbnails-item'})

        list_image = []

        for image in image_all:
            try:
                first =image['style'].replace('background-image:url("', 'https')
                link_image = first.replace('_14.JPG")', '_84.JPG')
            except:
                link_image = 'missing'

            list_image.append(link_image)

        image_dict = dict({'images' : list_image})
        self.image = image_dict
        return image_dict
        
    def parse_all(self):
        '''
        Merges all the available characteristics and creates a Pandas DataFrame.
        
        Returns: Pandas DataFrame
        '''
        
        moto_main_attributes = self.main_attributes
        moto_extra_attributes = self.extra_attributes
        moto_text = self.text
        moto_brand = self.brand
        moto_id = self.id
        today = self.extracted_date
        price = self.price
        location = self.location
        seller_name = self.seller_name
        image = self.image
        
        list_of_attributes = [moto_id, price ,moto_brand, moto_main_attributes, moto_extra_attributes, moto_text,today,location,seller_name,image]
        
        merged_dictionary = {k:v for x in list_of_attributes for k,v in x.items()}
        
        full_data = pd.DataFrame([merged_dictionary])
        
        return full_data