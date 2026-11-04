@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data['object'] == 'page':
        for entry in data['entry']:
            # EITA IMPORTANT FIX
            if 'messaging' not in entry:
                continue
            for messaging_event in entry['messaging']:
                if 'message' in messaging_event:
                    sender_id = messaging_event['sender']['id']
                    message_text = messaging_event['message'].get('text')
                    if message_text:
                        send_message(sender_id, message_text)
    return "ok", 200
