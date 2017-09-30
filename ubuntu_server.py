from flask import Flask, request, jsonify
from chatbot import chatbot
from pprint import pprint 
import os
c = chatbot.Chatbot()
c.main()

ubuntu_app = Flask(__name__)

@ubuntu_app.route('/')
def hello():
    return "Welcome to the ubuntu server"

@ubuntu_app.route('/get_answer', methods=['POST'])
def get_answer():
    data = request.get_json()
    message = data['message']
    res = c.daemonPredict(message)
    return jsonify({"result" : res} )

if __name__ == "__main__":
    ubuntu_app.run(host='0.0.0.0',debug=True)