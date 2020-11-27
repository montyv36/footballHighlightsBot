' #!/usr/bin/python3 '

import random
from flask import Flask, request
from pymessenger.bot import Bot
import threading
import os

app = Flask(__name__)
apiConfig = returnConfig()
fb_page_access_token = apiConfig.get("api_keys","fb_page_access_token")
fb_verify_token = apiConfig.get("api_keys","fb_page_verify_token")
file_location = apiConfig.get("storage","filePath")

bot = Bot(fb_page_access_token)


def generate_video(team,recipient_id):
    print(team+"ariij")
    print(recipient_id+"ss")
    command = "python3 "+file_location+"/mergeHighlights.py "+team+" "+recipient_id
    os.system(command)

def send_fixtures(r):
    command = "python3 "+file_location+"/createFixtures.py "+r
    os.system(command)

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       print(output)
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                print(recipient_id)
                if message.get('message') and  message['message'].get('text'):
                    response_sent_text = str(message['message'].get('text'))
                    if response_sent_text == "show fixtures":
                        send_message(recipient_id,"Looking for fixtures")
                        tr = threading.Thread(target = send_fixtures,name="Send Fixtures",args = [recipient_id])
                        tr.start()
                    else:
                        print(response_sent_text)
                        send_message(recipient_id, "We're looking for your video!")
                        tr = threading.Thread(target=generate_video, name="Video generator", args=[response_sent_text,recipient_id])
                        tr.start()
                if message.get('postback') and  message['postback'].get('payload'):
                    response_sent_text = str(message['postback'].get('payload'))
                    print(response_sent_text)
                    send_message(recipient_id, "Showing highlights for " + message['postback']['title'])
                    tr = threading.Thread(target=generate_video, name="Video generator", args=[response_sent_text,recipient_id])
                    tr.start()

    return "Message Processed"


def verify_fb_token(token_sent):
    if token_sent == fb_verify_token:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def send_message(recipient_id, response):
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()
