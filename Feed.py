# package import statement
from initalization import initalization
from smartapi import SmartWebSocket
import csv

from smartapi import SmartConnect
from smartapi import webSocket
from smartapi.smartWebSocketV2 import SmartWebSocketV2
import threading



class feed(initalization):
    def __init__(self):
        super().__init__()
        self.MarketFeeed = dict()

        self.correlation_id = "test1"
        self.subAction = 1          #1 sub 0 unsub
        self.unsubAction = 0
        self.snapQuoteMode = 3      #1 (LTP)  2 (Quote) 3 (Snap Quote)

        self.socketObj = SmartWebSocket(self.feedToken, self.client_id)
        self.sws = SmartWebSocketV2(self.auth_token, self.api_key, self.client_id, self.feedToken)
        # WS = webSocket(self.feedToken, self.client_id)
        self.token_list = [{"exchangeType": 2, "tokens": ["46285"]}]

        # print("ws==========",WS)
        print("self.socketObj =========",self.socketObj)
        threading.Thread(target=self.getMarketFeed).start()

    def getMarketFeed(self):

        def on_data(wsapp, message):
            try:
                print(message)
                # # print("Ticks: {}".format(message))
                # # print('last_traded_price',message['last_traded_price']/100)
                # data = {"token":message['token'],"bid" : message['best_5_sell_data'][4]['price']/100 ,"ask":message['best_5_buy_data'][0]['price']/100
                #         ,"ltp":message['last_traded_price']/100}
                
                # print(data)
                # # write_csv(data)
                # # print('best_5_buy_data',message['best_5_buy_data']/100)

                # # print("ltp : ",message['last_traded_price']/100,"ask : ",message['best_5_buy_data'][0]['price']/100,"ask : ",message['best_5_sell_data'][4]['price']/100)
            except Exception as e:
                print(e)


        def on_open(wsapp):
            print("on open")
            self.sws.subscribe(self.correlation_id,self.snapQuoteMode, self.token_list)


        def unsubscribe():
            self.sws.unsubscribe(self.correlation_id,self.snapQuoteMode, self.token_list)


        def on_error(wsapp, error):
            print(error)


        def on_close(wsapp):
            print("Close")


        # Assign the callbacks.
        self.sws.on_open = on_open
        self.sws.on_data = on_data
        self.sws.on_error = on_error
        self.sws.on_close = on_close


    def write_csv(self,data):
        with open('marketData.csv', 'w') as csv_file:  
            writer = csv.writer(csv_file)
            for key, value in data.items():
                writer.writerow([key, value])


feedObj = feed()







#logout
# try:
#     logout=smartapiObj.terminateSession('V438849')
#     print("Logout Successfull")
# except Exception as e:
#     print("Logout failed: {}".format(e.message))

