import twstock
import time
import requests

def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {'message': msg }
    notify = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
    return notify.status_code

def sendline(mode, realprice, counterline, token):
    print('建榮目前股價:' + str(realprice))
    if mode == 1:
        message = '現在建榮股價為' + str(realprice) + '元，可以賣出股票了!'
    else:
        message = '現在建榮股價為' + str(realprice) + '元，可以買入股票了!'
    code = lineNotifyMessage(token, message)
    if code == 200:
        counterline = counterline + 1
        print('第' + str(counterline) + '次發送line訊息。')
    else:
        print('發送line訊息失敗')
    return counterline

token = '75SXQN534yudaWLQstdr7Zl3187vZr9H4QidbArkiMi'
counterline = 0
countererror = 0

print('程式開始')
while True:
    realdata = twstock.realtime.get('5340')
    if realdata['success']:
        realprice = realdata['realtime']['latest_trade_price']
        if realprice != '-':
            if float(realprice) >= 70:
                counterline = sendline(1, realprice, counterline, token)
            elif float(realprice) <= 45:
                counterline = sendline(2, realprice, counterline, token)
            if counterline >= 3:
                print('程式結束!')
                break
            for i in range(300):
                time.sleep(1)
    else :
        print('twstock 讀取錯誤，錯誤原因:' + realdata['rtmessage'])
        countereffor = countererror + 1
        if countererror >= 3:
            print('程式結束!')
            break