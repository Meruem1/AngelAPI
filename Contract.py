import requests
import pandas as pd
class contact:
    def __init__(self):
        super().__init__()


    def generateContract(self):
        print("generateContract")
        url =''
        d = requests.get(url).json()

        token_df = pd.DataFrame.from_dict(d)
        token_df['expiry'] = pd.to_datetime (token_df ['expiry']).apply(lambda x: x.date())
        token_df = token_df.astype({'strike': float})
      
        return token_df
        # print(token_df['token'],token_df['symbol'])


