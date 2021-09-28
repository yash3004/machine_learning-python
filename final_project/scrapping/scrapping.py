#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 15:14:40 2021

@author: yash
"""

#importing the libraries 
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from lxml import html
from time import sleep
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
from lxml import etree
#init the webpage
url = 'https://www.etsy.com/in-en/c/jewelry?ref=pagination&explicit=1'
browser = webdriver.Chrome(ChromeDriverManager().install())
browser.maximize_window()
browser.get(url)

#creating the funciton for the links in the webpage
Links = []
reviews = []
overall= []


from bs4 import BeautifulSoup
from lxml import etree
import requests
  
#fucntion for changing the page
def change_page():
    
    previous_height = browser.execute_script('return document.body.scrollHeight')
    count = 2
    
    #starting a loop 
    while True:
        browser.execute_script('window.scrollTo(0,document.body.scrollHeight);')
       
        new_height = browser.execute_script('return document.body.scrollHeight')
        # getting an item clicked
        
        url1 = 'https://www.etsy.com/in-en/c/jewelry?ref=pagination&explicit=1&page='+str(count)+''
        if new_height == previous_height:
            
            browser.get(url1)
            
            
            #code for moving on the next page 
        previous_height = new_height
        
        get_links()
        sleep(2)
        count += 1
        print(count)
        if count == 200:
            break

def get_links():
    count = 1
    while True:
        
        x_path_link = '//*[@id="content"]/div/div[1]/div/div[3]/div[2]/div[2]/div[6]/div/div/div/ul/li['+str(count)+']/div'
        link = browser.find_element_by_xpath(x_path_link)
        linkText = link.get_attribute('innerHTML')
        #using the regwx for the data
        import re
        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        url1 = re.findall(regex,linkText)  
        links = url1[0][0]
        Links.append(links)
        #browser.get(links)
        
        
        
        #browser.back()
        
        count += 1 
        print(count)
        if count == 64:
         
            break
   

    
    
 
      
      
change_page()    
      
countr = 0
while True:
    page = requests.get(Links[countr])

    soup = BeautifulSoup(page.content,'html.parser')
    review = soup.find_all("p" , class_ = 'wt-text-truncate--multi-line wt-break-word' )
    for i in range(0,4):
        try:
            reviews.append(review[i].get_text())
        except:
            pass
    countr += 1 
    
    print(countr)
    if countr == len(Links):
        break
reviews[:] = [review.lstrip('\n') for review in reviews]

