from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os 

app = Flask(__name__)


load_dotenv()

mongo_uri = os.getenv('MONGO_URI')
db_name   = os.getenv('DB_NAME')


# MongoDB connection
client = MongoClient(mongo_uri)
db = client[db_name]
collection = db['Collection-One']

# Route to display the form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    place = request.form.get('place')

    if not name or not place:
        return jsonify({"error": "Missing data"}), 400

    # Insert data into MongoDB
    data = {
      "name": name, 
      "place": place
    }
    collection.insert_one(data)

    return redirect(url_for('index'))

@app.route('/view', methods=['GET'])
def view_collection():

    documents = collection.find({})

    result = []
    for doc in documents:
        doc['_id'] = str(doc['_id'])
        result.append(doc)


    return render_template('view.html', data=result)
    

if __name__ == '__main__':
    app.run(debug=True)