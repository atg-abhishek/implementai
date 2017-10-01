from flask import Flask, request, jsonify
from pprint import pprint 
import os

ubuntu_app = Flask(__name__)

@ubuntu_app.route('/')
def hello():
    return "Welcome to the other server"

if __name__ == "__main__":
    ubuntu_app.run(host='0.0.0.0',debug=True)