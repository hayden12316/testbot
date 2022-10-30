from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

from flask_sqlalchemy import SQLAlchemy

import random
import os

db = SQLAlchemy()
app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://sql12530467:DtkfuNPVjS@sql12.freemysqlhosting.net:3306/sql12530467"

db.init_app(app)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('b+sTKdho12m4+yfB4tv2/2E7Qpetf3qgOPi0cOpwwe+vQeXE3zs0K+6VKlcu0C6HkmwVchvXubrxjqJk0nRkd4n10bhs1ZQ4lG+i2YpGOnAGaIAREzxeAQf71iQELK2FnwhlgnU+0gUHdDIvhZYpzAdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('203521a641695c4d7110debaf7b1ecb2')

line_bot_api.push_message('U93285018abb1284972b72cd643b1ce41', TextSendMessage(text='你可以開始了'))
# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    print('call callback()')
    app.logger.info('logger call callback()')
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        print('call handle')
        handler.handle(body, signature)
    except InvalidSignatureError as e:
        print('throw InvalidError')
        print(e)
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    sql_cmd = """select * from Customer; """
    query_data = db.engine.execute(sql_cmd)
    # print(db.engine.execute(sql_cmd).fetchall())
    # print('#########   ', query_data.fetchone()[0])
    message = TextSendMessage(text=event.message.text + ' 只有一筆資料  ' + query_data.fetchall())
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    print('start~~~~~~~~')
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
