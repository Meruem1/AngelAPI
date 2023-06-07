from Contract import contact
from smartapi import SmartConnect #or from smartapi.smartConnect import SmartConnect
import pyotp


# #create object of call
# smartapiObj=SmartConnect(self.api_key=self.api_key)
#                 # ,
#                 #optional
#                 #access_token = "your access token",
#                 #refresh_token = "your refresh_token")

# #login api call


class initalization(contact):
    def __init__(self):
        super().__init__()
        self.client_id = ""
        # self.password = "meruem@6467"
        self.password = ""
        self.api_key = ""
        self.qrOtp = ""

        self.token_df = []
        self.feedToken = None
        self.refreshToken = None
        self.auth_token = None

        self.smartapiObj = object()
        self.token_df = self.generateContract()
        self.getLoginCreds()


    def getLoginCreds(self):

        totp = pyotp.TOTP(self.qrOtp)
        totp = totp.now()
        print("totp =========",totp)
        self.smartapiObj = SmartConnect(self.api_key)

        data = self.smartapiObj.generateSession(self.client_id,self.password,totp)
        print("data =====",data)
        print("self.smartapiObj =====",self.smartapiObj)
        if(data['status']):
            self.refreshToken= data['data']['refreshToken']
            self.auth_token= data['data']['jwtToken']


            #fetch the feedtoken
            self.feedToken=self.smartapiObj.getfeedToken()

            print("refreshToken",self.refreshToken)
            print("self.auth_token",self.auth_token)
            print("init self.feedToken",self.feedToken)
            # print("feedToken",feedToken)

            # #fetch User Profile
            userProfile= self.smartapiObj.getProfile(self.refreshToken)
            print("userProfile",userProfile)
        else:
            print("login error",data)


initalization()