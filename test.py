from smartapi import SmartWebSocket
import csv

from smartapi import SmartConnect
from smartapi import webSocket
from smartapi.smartWebSocketV2 import SmartWebSocketV2
import threading

FEED_TOKEN = ''
CLIENT_CODE= ''
API_KEY = ""
AUTH_TOKEN =''

correlation_id = "test1"
action = 1    #1 sub 0 unsub
mode = 3      #1 (LTP)  2 (Quote) 3 (Snap Quote)

token_list = [{"exchangeType": 2, "tokens": ["46285"]}]

sws = SmartWebSocketV2(AUTH_TOKEN, API_KEY, CLIENT_CODE, FEED_TOKEN)


def on_data(wsapp, message):
    try:
        # print("Ticks: {}".format(message))
        # print('last_traded_price',message['last_traded_price']/100)
        data = {"token":message['token'],"bid" : message['best_5_sell_data'][4]['price']/100 ,"ask":message['best_5_buy_data'][0]['price']/100
                ,"ltp":message['last_traded_price']/100}
        
        print(data)
        # write_csv(data)
        # print('best_5_buy_data',message['best_5_buy_data']/100)

        # print("ltp : ",message['last_traded_price']/100,"ask : ",message['best_5_buy_data'][0]['price']/100,"ask : ",message['best_5_sell_data'][4]['price']/100)
    except Exception as e:
        print(e)


def on_open(wsapp):
    print("on open")
    sws.subscribe(correlation_id, mode, token_list)
    # unsubscribe()


def unsubscribe():
    sws.unsubscribe(correlation_id, mode, token_list)



def on_error(wsapp, error):
    print(error)


def on_close(wsapp):
    print("Close")


def write_csv(data):
    with open('marketData.csv', 'w') as csv_file:  
        writer = csv.writer(csv_file)
        for key, value in data.items():
            writer.writerow([key, value])


# Assign the callbacks.
sws.on_open = on_open
sws.on_data = on_data
sws.on_error = on_error
sws.on_close = on_close


threading.Thread(target=sws.connect()).start()

# sws.close_connection()

print("helloo----")
