from flask import Flask, request
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = "arafat123"
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN") or os.environ.get("PAGE_TOKEN") or os.environ.get("PAGE_")

@app.route('/')
def home():
    return f"Bot is running! Token set: {bool(PAGE_ACCESS_TOKEN)}"

@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get('hub.verify_token') == VERIFY_TOKEN:
        return request.args.get('hub.challenge'), 200
    return "Verification failed", 403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                if messaging_event.get('message'):
                    sender_id = messaging_event['sender']['id']
                    message_text = messaging_event['message'].get('text')
                    if message_text:
                        send_message(sender_id, f"Hi! Tumi likhecho: {message_text}")
    return "EVENT_RECEIVED", 200

def send_message(recipient_id, message_text):
    url = f"https://graph.facebook.com/v18.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    payload = {"recipient": {"id": recipient_id}, "message": {"text": message_text}}
    requests.post(url, json=payload)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
