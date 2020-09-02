#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pymongo
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import requests
import shutil
from IPython.display import Image
from pprint import pprint

# Setting the chromedriver path
executable_path = {'executable_path':ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ## NASA Mars News

# In[3]:


# Visiting the following url
Mars_news_url = 'https://mars.nasa.gov/news/'
browser.visit(Mars_news_url)

# Retrieving page
html = browser.html

# Creating a BeautifulSoup object and parsing with html.parser
soup = bs(html, 'html.parser')

# Extracting all news
all_news = soup.find_all('div', class_='list_text')
latest_news = all_news[0]
news_title = print(latest_news.find('div', class_='content_title').text)
news_p = print(latest_news.find('div', class_='article_teaser_body').text)


# ## JPL Mars Featured Image

# In[4]:


# Visiting the following url
JPL_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(JPL_url)

# Retrieving page
html = browser.html

# Creating a BeautifulSoup object and parsing with html.parser
soup = bs(html, 'html.parser')

# Extracting url for page with full resolution image
home_pg_url = JPL_url.split('spaceimages')[0]
short_detail_url = soup.find('a', id='full_image')['data-link'][1:]
detail_url = f'{home_pg_url}{short_detail_url}'

# Extracting featured image url
browser.visit(detail_url)
html = browser.html
soup = bs(html, 'html.parser')
short_image_url = soup.find('img', class_='main_image')['src'][1:]

featured_image_url = f'{home_pg_url}{short_image_url}'
featured_image_url


# ## Mars Facts

# In[5]:


# Visiting the following url
weather_url = 'https://space-facts.com/mars/'
browser.visit(weather_url)

# Retrieving page
html = browser.html

# Extracting Facts table
table = pd.read_html(weather_url)[0].rename(columns={0:'Attribute', 1:'Details'})
table

# # Generate HTML table from DataFrame
html_table = table.to_html().replace('\n','')
html_table


# ## Mars Hemispheres

# In[6]:


# Visiting the following url
hemis_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(hemis_url)

# Retrieving page
html = browser.html

# Initiating variable
hemisphere_image_urls =[]

# Creating a BeautifulSoup object and parsing with html.parser
soup = bs(html, 'html.parser')
results = soup.find_all('div', class_='item')
# pprint(results)

# For looping through all hemispheres
for result in results:
    
    try:
        # Identify and return the title with hemisphere
        title = result.find('h3').text
#         print(title)

        # Identify and return the thumbnail image url
        home_url = hemis_url.split('search')[0]
        short_url = result.find('a', class_='itemLink product-item')['href'][1:]
        detail_url = f'{home_url}{short_url}'
        
        # Navigate to the hemisphere page
        browser.visit(detail_url)
        html = browser.html
        soup = bs(html, 'html.parser')
        image_short_url = soup.find('img', class_='wide-image')['src'][1:]
        img_url = f'{home_url}{image_short_url}'
        
        # Creating a dictionary for title and url
        dictionary = {
                    'Title': title,
                    'Image url': img_url
        }
        
        # Appending dictionary to a list (could have done it all in one step)
        hemisphere_image_urls.append(dictionary)
    
    except:
        pass


# In[7]:


hemisphere_image_urls


# In[ ]:




