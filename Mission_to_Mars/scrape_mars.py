import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
from pprint import pprint

def init_browser():

    # Setting the chromedriver path
    executable_path = {'executable_path':ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def scrape():

    browser = init_browser()

    # Initiatilizing a dictionary that we can insert into mongo
    Mars_data = {} 

    # ## NASA Mars News
    # Visiting the following url
    Mars_news_url = 'https://mars.nasa.gov/news/'
    browser.visit(Mars_news_url)

    # Retrieving page
    html = browser.html

    # Creating a BeautifulSoup object and parsing with html.parser
    soup = bs(html, 'html.parser')

    # Extracting news
    latest_news = soup.find('div', class_='list_text')
    # latest_news = soup.find('ul', class_='item_list').find('li', class_='slide').find('div').find('div', class_='list_text')
    news_title = latest_news.find('div', class_='content_title').text
    news_p = latest_news.find('div', class_='article_teaser_body').text

    # Adding to our dictionary
    Mars_data['Title'] = news_title
    Mars_data['Teaser'] = news_p

    # ## JPL Mars Featured Image
    # Visiting the following url
    JPLurl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(JPLurl)

    # Retrieving page
    html = browser.html

    # Creating a BeautifulSoup object and parsing with html.parser
    soup = bs(html, 'html.parser')

    # Extracting url for page with full resolution image
    home_pg_url = JPLurl.split('spaceimages')[0]
    short_detail_url = soup.find('a', id='full_image')['data-link'][1:]
    detail_url = f'{home_pg_url}{short_detail_url}'

    # Extracting featured image url
    browser.visit(detail_url)
    html = browser.html
    soup = bs(html, 'html.parser')
    short_image_url = soup.find('img', class_='main_image')['src'][1:]

    featured_image_url = f'{home_pg_url}{short_image_url}'
    featured_image_url

    # Adding to the dictionary
    Mars_data["Featured_image"]=featured_image_url

    # ## Mars Facts
    # Visiting the following url
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)

    # Retrieving page
    html = browser.html

    # Extracting Facts table
    table = pd.read_html(facts_url)[0].rename(columns={0:'Description', 1:'Mars'}).set_index('Description')

    # # Generate HTML table from DataFrame
    html_table = table.to_html(classes='table table-striped', table_id='html_table', index=True).replace('\n','')

    # Adding to the dictionary
    Mars_data['Facts']=html_table

    # ## Mars Hemispheres
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

    # For looping through all hemispheres
    for result in results:
        
        try:
            # Identify and return the title with hemisphere
            title = result.find('h3').text

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
                        'img_url': img_url
            }
            
            # Appending dictionary to a list
            hemisphere_image_urls.append(dictionary)
        
        except:
            pass

    # Adding to the dictionary
    Mars_data['Hemispheres'] = hemisphere_image_urls

    browser.quit()
    return Mars_data





