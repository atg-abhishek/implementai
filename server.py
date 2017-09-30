from flask import Flask, request
from pymongo import MongoClient
import os, json, requests
from pprint import pprint 
from random import randint

client = MongoClient(os.environ['MONGODB_URI'])
db = client[os.environ['MONGO_DB_NAME']]

users = db['users']

app = Flask(__name__)

@app.route('/')
def hello():
    return "Welcome to the server for the Implement AI hackathon"

@app.route('/test/add_user')
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
                try: 
                    if "sticker_id" in messaging_event['message'].keys():
                        send_message(sender_id, "Please don't send me stickers, emoji or non-text stuff, I'm boring that way :(")
                        return "ok", 200

                    message_text = messaging_event["message"]["text"]  # the message's text

                    if message_text == "Reset":
                        users.remove({'user_id' : sender_id})

                    if users.find_one({'user_id' : sender_id}) is None:
                        # User was not found in the database, create them 
                        users.insert_one({'user_id' : sender_id, 'state' : 0})


                    item = users.find_one({'user_id' : sender_id})
                    if item['state'] == 0: 
                        send_message(sender_id, "Welcome to the ToastMaster! I can do many things! ")
                        send_quick_reply(sender_id, "Let's start with one of the following options ", [
                                {"content_type" : "text", "title" : "Jokes", "payload" : "0"},
                                {"content_type" : "text", "title" : "Talk to me!", "payload" : "1"}
                            ]
                        )
                        users.update_one({'user_id' : sender_id}, {'$set' : {'state' : 1} })

                    if item['state'] == 1:
                        #TODO: need to process the quick reply chosen 
                        send_message(sender_id, "Ok well let's just chat for a bit now!")

                    with open('samples.txt','w') as outfile:
                        outfile.writelines(message_text)


                    #TODO: get rid of the following once the actual model is plugged in 
                    mess_list = [
                        "How you doing?",
                        "My man what's good!",
                        "Let's make some stuff happen",
                        "So this hackathon is a lot of fun isn't it?",
                        "tell me a joke and I will judge how funny it is"
                    ]
                    send_message(sender_id, mess_list[randint(0,4)])

                except:
                    send_message(sender_id ,"Encountered an error, check the logs")
                    return "ok", 200

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

def send_quick_reply(recipient_id, message_text, content):
    # Content needs to be a list of dicts
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
            "text": message_text, 
            "quick_replies" : content
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)


if __name__ == "__main__":
    app.run(debug=True)