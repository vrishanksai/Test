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
    name = request.form.get('name').strip()
    place = request.form.get('place').strip()

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
    
@app.route('/get_user/<name>', methods=['GET'])
def get_user(name):
    # Find user by name
    # print (f'name : {type(name)}')
    user_data = collection.find_one({'name': name})
    # Render the user data in the template
    return render_template('user_rec.html', user_data=user_data)


@app.route('/update', methods=['GET', 'POST'])
def update_user():
    name = request.form.get('name')
    new_place = request.form.get('new_place')

    result = collection.update_one(
        {'name': name},
        {'$set': {'place': new_place}}
    )

    return render_template('update_rec.html')

@app.route('/delete-user', methods=['POST', 'GET'])
def delete_user(): 
    if request.method == 'POST':
        username = request.form.get('name')
        
        # Delete the user from MongoDB
        result = collection.delete_one({"name": username})

        if result.deleted_count > 0:
            return f"User '{username}' deleted successfully."
        else:
            return f"User '{username}' not found."

    # Render the HTML form on GET request
    return render_template('delete_user.html')

if __name__ == '__main__':
    app.run(debug=True)

