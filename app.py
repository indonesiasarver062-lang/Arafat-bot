from flask import Flask, request
import requests, os

app = Flask(__name__)
PAGE_TOKEN = os.environ.get("PAGE_TOKEN")
VERIFY_TOKEN = "arafat_royal_bot"

@app.route('/')
def home(): 
    return "ARaFat Bot Live - All Country Supported!"

@app.route('/webhook', methods=['GET','POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Verification Failed"
    
    data = request.get_json()
    if data and data.get('object') == 'page':
        for entry in data['entry']:
            for m in entry['messaging']:
                if 'message' in m and 'text' in m['message']:
                    uid = m['sender']['id']
                    txt = m['message']['text']
                    low = txt.lower()
                    
                    # All replies in English - All Country Support
                    if any(x in low for x in ["hi","hello","hey","hlw","salam","hola","bonjour"]):
                        reply = "Hello! 👑 This is ARaFat 2.0 AI! I support all countries and languages! How can I help you today?"
                    elif any(x in low for x in ["price","dam","koto","cost","how much"]):
                        reply = "For price details, please tell me the product name! We have worldwide delivery! 🌍"
                    elif any(x in low for x in ["love","bhalobashi"]):
                        reply = "Love you too! ❤️ You are my favorite person!"
                    elif any(x in low for x in ["who are you","who r u","tumi ke"]):
                        reply = "I am ARaFat 2.0 AI, your 24/7 smart assistant! I understand all languages and support all countries! 👑"
                    elif any(x in low for x in ["help","support"]):
                        reply = "Sure! I am here to help you 24/7! Tell me what you need! I support all countries! 🚀"
                    else:
                        # Universal Reply for ANY question in English
                        reply = f"You said: '{txt}' - I got it! I am ARaFat 2.0 AI, I support all languages and all countries! Tell me more, how can I assist you? 😎🌍"

                    requests.post(f"https://graph.facebook.com/v18.0/me/messages?access_token={PAGE_TOKEN}",
                        json={"recipient": {"id": uid}, "message": {"text": reply}})
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
