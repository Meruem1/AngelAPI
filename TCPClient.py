import socket
import time
import json
import threading
import os
import multiprocessing
import SharedArray as sa


# print(f"{os.getcwd()}\\tcp_data_config.json")



with open("settings.json", "r") as jsonfile:
    # with open(f"{os.getcwd()}\\tcp_data_config.json", "r") as jsonfile:
    SettingStruct = json.load(jsonfile).get('Settings')
queueList = multiprocessing.Queue(SettingStruct['MaxSixeQueue'])




class TCPServer :

    def __init__(self):
        print("call")


        self.__marketDataStruct = dict()
        self.__SettingStruct = dict()

        self._SocketData = dict()
        # Reading tcp_data_config file here
        with open("tcp_data_config.json", "r") as jsonfile:
        # with open(f"{os.getcwd()}\\tcp_data_config.json", "r") as jsonfile:
            self.__marketDataStruct = json.load(jsonfile).get('marketdata')


        with open("settings.json", "r") as jsonfile:
        # with open(f"{os.getcwd()}\\tcp_data_config.json", "r") as jsonfile:
            self.__SettingStruct = json.load(jsonfile).get('Settings')
            print(self.__SettingStruct)

            self.__HOST = SettingStruct['HOST']
            self.__PORT = SettingStruct['PORT']
            self.__BSE_DIR = SettingStruct['BSE_DIR']
            self.__EXCHANGE = SettingStruct['EXCHANGE']


        self.__flag = 1

        threading.Thread(target=self.__startTCPServer).start()
        # threading.Thread(target=self.__saveIntoSharedArray).start()
        # threading.Thread(target=self.__PutTCPQueue).start()
        # threading.Thread(target=self.__GetTCPQueue).start()



    def __startTCPServer(self):
        self.__serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__serversocket.bind((self.__HOST, self.__PORT))
        self.__serversocket.listen(5)
        print("server up and running!!!!")
        while self.__flag>0:
            try :
                # establish a connection
                clientsocket,addr = self.__serversocket.accept()
                print("TCP Client Connected ========= ", clientsocket,addr)
                missing=''
                __data =''
                while self.__flag>0 :
                    try :
                        __sockD = []
                        __data =  str(clientsocket.recv(4096).decode())
                        print(__data)
                        if len(__data)>0 :
                            if len(missing)>0:
                                __data = missing+__data
                                missing=''
                            tempData =  __data.strip().split("\n")
                            for i,value in enumerate(list(map(self.filterData,tempData))) :
                                if value is None  :
                                    missing = tempData[i]
                                else :
                                    __sockD.append(value)

                            if len(__sockD)>0 :
                                # self.__UpdateBidAsk(__sockD)
                                self._SocketData = __sockD

                                print(__sockD)

                    except Exception as e :
                        print("e",e)
                        # try:
                        #     a = sa.create("file://{}/Broadcaster.txt".format(self.__BSE_DIR), 100)
                        # except:
                        #     print("Exception")
                        self._SocketData = []
                        clientsocket.close()
            except Exception as e :
                print(e)



    def __saveIntoSharedArray(self):
        while  self.__flag>0:
            try:
                if len(self._SocketData)>0 :
                    try:
                        # print(self._SocketData)
                        # print(f"file://{self.__EXCHANGE}_{self.__BSE_DIR}/Broadcaster".format(self.__BSE_DIR,self.__EXCHANGE)  )
                        a = sa.create("file://{}/{}_Broadcaster".format(self.__BSE_DIR,self.__EXCHANGE), 100)
                    except Exception as e:
                        print("Exception",e)
                        # a= sa.attach("file://{}/C-{}/{}".format(os.getcwd(),self.username,self.username))
                    # for i in self._SocketData:
                    #     queueList.put(i)
                    #     # print("==========",i)
                    time.sleep(5)
            except Exception as e:
                print("__GetTCPQueue!!",e)

    def __PutTCPQueue(self):
        while  self.__flag>0:
            try:
                if len(self._SocketData)>0 :
                    for i in self._SocketData:
                        queueList.put(i)
                        # print("==========",i)
                    time.sleep(1)
            except Exception as e:
                print("__GetTCPQueue!!",e)


    def __GetTCPQueue(self):
        while  self.__flag>0:
            try:
                item = queueList.get()
                # print(f'Finished {item}')
                # time.sleep(2)
            except Exception as e:
                print("__GetTCPQueue!!",e)


    # def __UpdateBidAsk(self,Data):
    #     for i,value in enumerate(Data) :
    #         if value.get("token") not in self._SocketData.keys() :
    #             self._SocketData[value.get("token")] = value
    #         else :
    #             for i in self.__marketDataStruct.get("packet").keys():
    #                 self._SocketData.get(value.get("token"))[i] = value.get(i)


    def filterData(self,temp):
        Data = temp
        if len(Data)>0  :
            if Data.count('#') == Data.count('$') :
                if str(Data).find('$')>0 and str(Data).find('#')>0 :
                    Data = str(Data).replace('|$|','').replace('|#|','').strip().split('|')
                    r = dict((i, int(Data[self.__marketDataStruct.get("packet")[i]])) \
                            for i in self.__marketDataStruct.get("packet").keys())
                    return r
            # else :
            #     if str(Data).startswith(self.__marketDataStruct.get("start")):
            #         print("one of end packet is missing !")
            #     elif str(Data).startswith(self.__marketDataStruct.get("end")):
            #         print("one of start packet is missing !")

TCPServer()
# queueList.join()
# print("Finished")

