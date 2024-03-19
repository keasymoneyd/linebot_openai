from flask import Flask
app = Flask(__name__)

from flask import request, abort
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import openai
import os

openai.api_key = os.getenv('OPENAI_API_KEY')
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
handler1 = WebhookHandler(os.getenv('CHANNEL_SECRET'))

message_counter = 0  

@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler1.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler1.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global message_counter  
    
    text1=event.message.text
    #職業
    user_ability = {
        "職業" : "教練" ,
        "技能" : "體育"
    }
    response = openai.ChatCompletion.create(
        messages=[
            {"role": "user", "content": text1},
            {"role": "system", "content": "這個GPT的個性資訊:" + str(user_ability)}
        ],
        model="gpt-3.5-turbo-0125",
        temperature = 0.5,
    )
    
    try:
        ret = response['choices'][0]['message']['content'].strip()
        message_counter += 1  
        print("OpenAI回答次數:", message_counter)  
    except:
        ret = '發生錯誤！'
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=ret))

if __name__ == '__main__':
    app.run()
