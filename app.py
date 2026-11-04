from flask import Flask, request
import requests
import os

app = Flask(__name__)

PAGE_ACCESS_TOKEN = os.environ.get('PAGE_ACCESS_TOKEN')
VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN', 'arafat123')

@app.route('/')
def home():
    return "Bot is running! Token set: {}".format(bool(PAGE_ACCESS_TOKEN))

@app.route('/webhook', methods=['GET'])
def verify():
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    if mode == 'subscribe' and token == VERIFY_TOKEN:
        return challenge, 200
    else:
        return "Verification failed", 403

def send_message(recipient_id, message_text):
    url = f"https://graph.facebook.com/v18.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    requests.post(url, json=payload)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data['object'] == 'page':
        for entry in data['entry']:
            if 'messaging' not in entry:
                continue
            for messaging_event in entry['messaging']:
                if 'message' in messaging_event:
                    sender_id = messaging_event['sender']['id']
                    message_text = messaging_event['message'].get('text')
                    if message_text:
                        send_message(sender_id, f"You said: {message_text}")
    return "ok", 200

if __name__ == '__main__':
    app.run()
