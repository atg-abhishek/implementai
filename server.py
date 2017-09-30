from flask import Flask 
from pymongo import MongoClient
import os

client = MongoClient(os.environ['MONGODB_URI'])
db = client[os.environ['MONGO_DB_NAME']]

users = db['users']

app = Flask(__name__)

@app.route('/')
def hello():
    return "Welcome to the server for the Implement AI hackathon"

@app.route('/db/add_user')
def add_user():
    users.insert_one({'user_id' : "hello"})
    return "done"

if __name__ == "__main__":
    app.run(debug=True)