from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri='mongodb://localhost:27017/mars_app')

# Route to render index.html template using data from Mongo
@app.route('/')
def home():

    Mars_data = mongo.db.Mars_data.find_one()

    return render_template('index.html', Mars_data=Mars_data)


# Route that will trigger the scrape function
@app.route('/scrape')
def scrape():

    # Running the scrape function
    Mars_data = scrape_mars.scrape()

    # Update the Mongo database using updated and upsert=True
    mongo.db.Mars_data.update({}, Mars_data, upsert=True)

    # Redirect back to home page
    return redirect('/', code=302)

if __name__ == "__main__":
    app.run(debug=True)
    
