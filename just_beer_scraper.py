# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 16:21:06 2020

@author: bdaet
"""

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

#initializing webdriver
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options = options)
driver.set_window_size(1120, 1000)

url = 'https://justbeerapp.com/guides/us/ca/breweries'

#max delay for WebDriverWait function
max_delay = 20

driver.get(url)

#total number of brewery links on page
num_breweries = len(driver.find_elements_by_css_selector('h3.title'))

brew_dict = {'Brewery':[],
             'Address':[],
             'Contact_Info':[]
             }

beer_dict = {'Brewery':[],
             'Beer':[],
             'Style':[]}

for i in range(num_breweries):

    WebDriverWait(driver, max_delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'section-header')))
    breweries = driver.find_elements_by_css_selector('h3.title')
    
    try:
        breweries[i].click()
    
    #sometimes ads would pop up and throw of the web scraper. easiest workaround was to reload the original web page when that happens
    except ElementNotInteractableException:
        driver.get(url)
        WebDriverWait(driver, max_delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'section-header')))
        breweries = driver.find_elements_by_css_selector('h3.title')
        breweries[i].click()
    
    #letting brewery web page load before scraping
    WebDriverWait(driver, max_delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'section-header')))
    
    #getting brewery name
    try:
        brewery = driver.find_element_by_xpath("//div[@class='item-content']/h5").text
    
    except NoSuchElementException:
        brewery = ''
        
    brew_dict['Brewery'].append(brewery)
    
    #getting brewery address
    try:
        brew_dict['Address'].append(driver.find_element_by_xpath("//p[@class='dek']/a").text)
    
    except NoSuchElementException:
        brew_dict['Address'].append('')
     
    #getting website link if available, phone number if not
    try:
        link_list = driver.find_elements_by_class_name('link')
        
    except NoSuchElementException:
        link_list = []
    
    if len(link_list) > 1:
        brew_dict['Contact_Info'].append(link_list[1].text)
    else:
        brew_dict['Contact_Info'].append('')
    
    
    #getting beer data
    if brewery == '':
        continue
    else:
        try:
            beers = driver.find_elements_by_xpath("//h3[@class='title']")
            styles = driver.find_elements_by_css_selector("span.txt-details")
            for i in range(len(styles)):
                beer_dict['Brewery'].append(brewery)
                beer_dict['Beer'].append(beers[i].text)
                beer_dict['Style'].append(styles[i].text)
    
        except NoSuchElementException:
            continue
        
    
    driver.back()


brew_df = pd.DataFrame(brew_dict)
brew_df.to_csv('breweries_raw.csv', index = False)

beer_df = pd.DataFrame(beer_dict)
beer_df.to_csv('beers_raw.csv', index = False)
