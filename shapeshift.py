import json
import requests
from broker import broker



class Shapeshift(broker):
    ''' Coomnon for multiple _init__ function

    '''
    def myinit(self):
        self.API_URL = 'https://shapeshift.io'
        #self.API_URL = 'https://shapeshift.io'
        #self.API_KEY = 'a078d292d5cc4fc2ad11511651edafe2'  # ''place_your_api_key_here'
        #self.API_SECRET = 'e1ec6f1ad52df07800d18bed63333268889e2a3c470b3df3afc42a7cfafd66a3'  # ''place_your_api_secret_here'

    def getCoinName(self):
        response = requests.get(self.API_URL + '/getcoins/')
        #print(response.text)
        '''
        {   
            "BTC": {"name": "Bitcoin", "symbol": "BTC", "image": "https://shapeshift.io/images/coins/bitcoin.png",
                 "imageSmall": "https://shapeshift.io/images/coins-sm/bitcoin.png", "status": "available",
                 "minerFee": 0.00125}, 
            "1ST": {"name": "FirstBlood", "symbol": "1ST", "image": "htt....
        }
        '''
        dctCoins = json.loads(response.text)
        return dctCoins

    def __init__(self):
        self.myinit()

    def __init__(self, bGetList):
        self.myinit()
        self.dctCoins = self.getCoinName()

    def getRate(self, sFrom, sTo):
        '''
        Interface from broker
        :param sFrom:
        :param sTo:
        :return:
        '''
        sPair = sFrom + '_' + sTo
        response = requests.get(self.API_URL + '/rate/' + sPair)
        aaa = response.json()
        print(response.json())
        print (response)
        return aaa['rate']

    def get_all(self):
        response = requests.get(self.API_URL + '/rate' )
        return response

if __name__ == "__main__":
    print ("running Main shapeshift.py")
    myss = Shapeshift('true')
    aRate = myss.getRate('CLAM','DOGE')
    print (aRate)
#    serialized_data = json.dumps(message)
#    headers = {'Content-type': 'application/json'}
#    response = requests.post(myss.API_URL, headers=headers, data=serialized_data)

    #type(response.json())
    #rrr = requests.get(myss.API_URL+'/rate')
    for key in myss.dctCoins:
        print(key)
    #rrr = myss.get_all()
    #print("a")
    #print rrr.headers
    #print("b")
    #print rrr.json()
    #print("c")
    #return response.json()
