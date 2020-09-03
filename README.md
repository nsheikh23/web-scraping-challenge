# Mission to Mars

Built a web application that scrapes various websites for data related to the Mission to Mars and displays the information in a single HTML page. The following summarizes what was done.

## Step 1 - Scraping

Initial scraping was performed using Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter.

### NASA Mars News

* Scraped the [NASA Mars News Site](https://mars.nasa.gov/news/) and collected the latest News Title and short description.

### JPL Mars Space Images - Featured Image

* Visited the url for JPL Featured Space Image [here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).

### Mars Facts

* Visited the Mars Facts webpage [here](https://space-facts.com/mars/) and used Pandas to scrape the Mars Profile table.

* Then used Pandas to convert the data to a HTML table string.

### Mars Hemispheres

* Visited the USGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to obtain high resolution images for each of Mar's hemispheres.

## Step 2 - MongoDB and Flask Application

Used MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped from the URLs above.

* Created a route called `/scrape` that imported `scrape_mars.py` script and called the `scrape` function.

* Stored the return value in MongoDB as a Python dictionary.

* Created a root route `/` that allows visitor to query the MongoDB and pass the mars data into an HTML template to display the data.

* Created a HTML page that takes the mars data and displays all of the data appropriately.

### Copyright

Trilogy Education Services © 2020. All Rights Reserved.
