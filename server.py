from flask import Flask, request
from pymongo import MongoClient
import os, json, requests
from pprint import pprint 

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

@app.route('/facebook_incoming')
def facebook_incoming():
    return request.args['hub.challenge']

@app.route('/facebook_incoming', methods=['POST'])
def webhook():

    # NOTE: code needed to be adapted to remove PASS and put return, 200 ok and ordering of the code, handling stickers, etc. hence removing the citation 
    data = request.get_json()
    for entry in data["entry"]:
        for messaging_event in entry["messaging"]:


            if messaging_event.get("delivery"):  # delivery confirmation
                return "ok", 200

            if messaging_event.get("optin"):  # optin confirmation
                return "ok", 200

            if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                return "ok", 200

            pprint(messaging_event)
            if messaging_event.get("message"):  # someone sent us a message
                
                sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID



                if "sticker_id" in messaging_event['message'].keys():
                    send_message(sender_id, "Please don't send me stickers, emoji or non-text stuff, I'm boring that way :(")
                    return "ok", 200

                message_text = messaging_event["message"]["text"]  # the message's text

                send_message(sender_id, "roger that!")

                

    return "ok", 200

def send_message(recipient_id, message_text):
    # CITATION :  version based on https://github.com/hartleybrody/fb-messenger-bot/blob/master/app.py
    params = {
        "access_token": os.environ["FB_PAGE_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)


if __name__ == "__main__":
    app.run(debug=True)