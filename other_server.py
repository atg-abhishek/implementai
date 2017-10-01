from flask import Flask, request, jsonify
from pprint import pprint 
import os

ubuntu_app = Flask(__name__)

@ubuntu_app.route('/')
def hello():
    return "Welcome to the other server"

@ubuntu_app.route('/get_answer', methods=['POST'])
def get_answer():
    data = request.get_json()
    incoming_message = data['message']
    with open('input.test','w') as outfile:
        outfile.write(incoming_message)
    #TODO: interface with the function 
    res = ""
    return jsonify({"result" : res})

if __name__ == "__main__":
    ubuntu_app.run(host='0.0.0.0',debug=True)