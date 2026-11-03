from flask import Flask, request
import requests, os
app = Flask(__name__)
PAGE_TOKEN = os.environ.get("PAGE_TOKEN")
VERIFY_TOKEN = "arafat_royal_bot"

@app.route('/')
def home(): return "ARaFat Bot 24H Running - All Country Support"

@app.route('/webhook', methods=['GET','POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Wrong"
    data = request.get_json()
    if data and data.get('object') == 'page':
        for entry in data['entry']:
            for m in entry['messaging']:
                if 'message' in m and 'text' in m['message']:
                    uid = m['sender']['id']
                    txt = m['message']['text']
                    reply = f"You said: {txt} - I am ARaFat AI, all countries support!"
                    requests.post(f"https://graph.facebook.com/v18.0/me/messages?access_token={PAGE_TOKEN}", json={"recipient":{"id":uid},"message":{"text":reply}})
    return "OK"
