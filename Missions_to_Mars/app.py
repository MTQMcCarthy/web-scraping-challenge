from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape

app = Flask(__name__)

# establish connection
app.config["MONGO_URI"]="mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars = mongo.db.collection.find_one()
    return render_template("index.html", mars = mars_data)

@app.route("/scrape")
def scrape():
    #mars = mongo.db.mars 
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    
    #redirect to home page
    return redirect("http://localhost:5000/")

if __name__ == "__main__":
    app.run(debug=True)