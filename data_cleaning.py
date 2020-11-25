# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 20:34:41 2020

@author: bdaet
"""
import pandas as pd
import googlemaps
import requests

brew_df = pd.read_csv('https://raw.githubusercontent.com/bryandaetz1/CA_brewery_map/main/breweries_raw.csv')
beer_df = pd.read_csv('https://raw.githubusercontent.com/bryandaetz1/CA_brewery_map/main/beers_raw.csv')

#filling in missing or incorrect values based on actual values from website
brew_df.iloc[3] = ['Ohana Brewing Company',
                   '7 S 1st Street\nAlhambra, California, United States',
                   'http://ohanabrew.com']

brew_df.iloc[279] = ["The Dudes' Brewing Company",
                     '304\n395 Santa Monica Place\nSanta Monica, California, United States',
                     'http://www.thedudesbrew.com']

brew_df.iloc[280] = ['Cooperage Brewing Company',
                     'G\n981 Airway Court\nSanta Rosa, California, United States',
                     'https://cooperagebrewing.com']

brew_df.iloc[288] = ['Culture Brewing Co.',
                     'Ste 200\n111 S Cedros Ave\nSolana Beach, California, United States',
                     'https://culturebrewingco.com']

brew_df.iloc[305] = ['Back Street Brewery',
                     '#B100\n15 Main St.\nVista, California, United States',
                     'http://www.backstreetbrew.com']

brew_df.iloc[317] = ['MadeWest Brewing Company',
                     '1744 Donlon Street\nWestlake Village, California, United States',
                     'https://madewest.com']

#removing Address from the end of each brewery name in brew_df
brew_df['Brewery'] = brew_df['Brewery'].str.replace('Address','').str.strip()

#removing Address from the end of each brewery name in beer_df
beer_df['Brewery'] = beer_df['Brewery'].str.replace('Address','').str.strip()


#appending missing beers to beers_df dataframe
beers_append = pd.DataFrame(data = [['Ohana Brewing Company','Spa Water Saison','Saison / Farmhouse Ale'],
                                     ["The Dudes' Brewing Company",'Blood Orange','American Amber / Red Ale'],
                                     ["The Dudes' Brewing Company",'Boysenberry','American Pale Wheat Ale'],
                                     ["The Dudes' Brewing Company",'CalifornIPA','American IPA'],
                                     ["The Dudes' Brewing Company",'Coconut','American Porter'],
                                     ["The Dudes' Brewing Company",'Double Trunk','American IPA'],
                                     ["The Dudes' Brewing Company","Grandma's Pecan",'English Brown Ale'],
                                     ["The Dudes' Brewing Company","Los Dude's Cerveza",'Light Lager'],
                                     ["The Dudes' Brewing Company",'Most Excellent IPA','American IPA'],
                                     ["The Dudes' Brewing Company",'Peach','Berliner Weissbier'],
                                     ["The Dudes' Brewing Company",'Schitzengiggle','Märzen / Oktoberfest'],
                                     ["The Dudes' Brewing Company",'Wiser Dude','American Double / Imperial Pilsner'],
                                     ['Cooperage Brewing Company','Cultivating Mass','American Double / Imperial Stout'],
                                     ['Culture Brewing Co.','2x Black IPA','American Double / Imperial IPA'],
                                     ['Culture Brewing Co.','2x IPA','American Double / Imperial IPA'],
                                     ['Culture Brewing Co.', '3x IPA','American Double / Imperial IPA'],
                                     ['Culture Brewing Co.', 'Blond Ale','American Blonde Ale'],
                                     ['Back Street Brewery','Tomahawk Double IPA','American Double / Imperial IPA'],
                                     ['Back Street Brewery','Set Sail IPA','American IPA'],
                                     ['Back Street Brewery','Rita Red Ale','American Amber / Red Ale'],
                                     ['Back Street Brewery','Rydin’ Dirty Rye IPA','American IPA'],
                                     ['MadeWest Brewing Company','Donlon IIPA','American Double / Imperial IPA']
                                     ],
                            columns = ['Brewery','Beer','Style'])

beer_df = pd.concat([beer_df,beers_append], axis = 0, sort = False).reset_index(drop = True)

#geocoding addresses using googlemaps

#API key for geocoding API
key = 'insert-API-key-here'

#function to get latitude and longitude from address using Google's geocoding API
def get_lat_lng(address):
    url = ('https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'.format(str(address).replace(' ','+'), key))
    
    try:
        response = requests.get(url)
        resp_json_payload = response.json()
        lat = resp_json_payload['results'][0]['geometry']['location']['lat']
        lng = resp_json_payload['results'][0]['geometry']['location']['lng']
        city = resp_json_payload['results'][0]['address_components'][2]['long_name']
        county = resp_json_payload['results'][0]['address_components'][3]['long_name']
        
    except:
        print('ERROR: {}'.format(address))
        lat = 0
        lng = 0
        city = ''
        county = ''
    return lat, lng, city, county

#iterating through Address column and geocoding latitudes and longitudes
brew_df['latitude'] = ''
brew_df['longitude'] = ''
brew_df['City'] = ''
brew_df['County'] = ''
for i, address in enumerate(brew_df['Address']):
    lat,lng,city,county = get_lat_lng(address)
    brew_df['latitude'][i] = lat
    brew_df['longitude'][i] = lng
    brew_df['City'][i] = city
    brew_df['County'][i] = county

#outputing new dataframes to csv    
brew_df.to_csv('breweries.csv', index = False)
beer_df.to_csv('beers.csv', index = False)






