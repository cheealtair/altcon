import hashlib
import hmac
import json
import requests
from broker import broker

# DECORATOR
def getResponse(bb):
   #print (bb)
   def wrap(func):
      def func_wrapper(self, *args):
         #print ('in func_wrapper')
         serialized_data = json.dumps(func(*args))
         #print (serialized_data)
         sign = hmac.new(self.API_SECRET.encode('utf-8'), serialized_data.encode('utf-8'), hashlib.sha512).hexdigest()
         headers = {'api-key': self.API_KEY, 'sign': sign, 'Content-type': 'application/json'}
         response = requests.post(self.API_URL, headers=headers, data=serialized_data)
         return response.json()
      return func_wrapper
   return wrap


class Changelly(broker):

   def __init__(self):
      self.API_URL = 'https://api.changelly.com'
      self.API_KEY = 'a078d292d5cc4fc2ad11511651edafe2'  # ''place_your_api_key_here'
      self.API_SECRET = 'e1ec6f1ad52df07800d18bed63333268889e2a3c470b3df3afc42a7cfafd66a3'  # ''place_your_api_secret_here'

   def __call__(self):
      pass

   @getResponse('dsd')
   def getCurrenciesJson():
      message = {
         'jsonrpc': '2.0',
         'id': 1,
         'method': 'getCurrencies',
         'params': []
      }
      return message

   @getResponse('d')
   def getExchangeAmountJson(self, sfrom, sto):
      message = {
         'jsonrpc': '2.0',
         'id': 2,
         'method': 'getExchangeAmount',
         'params': {
            'from': sfrom, # 'eth',
            'to': sto, # 'btc',
            'amount': '1'
         }
      }
      return message


   def getRate(self, sFrom, sTo):
       '''
       Interface from broker
       :param sFrom:
       :param sTo:
       :return:
       '''
       sMessage = self.getExchangeAmountJson(self, sFrom, sTo)
       # {u'jsonrpc': u'2.0', u'id': 2, u'result': u'0.32835'}
       rate = sMessage['result']
       return rate



   '''
   def getCurrencies(self):
      message = {
         'jsonrpc': '2.0',
         'id': 1,
         'method': 'getCurrencies',
         'params': []
      }
      serialized_data = json.dumps(message)
      sign = hmac.new(self.API_SECRET.encode('utf-8'), serialized_data.encode('utf-8'), hashlib.sha512).hexdigest()
      headers = {'api-key': self.API_KEY, 'sign': sign, 'Content-type': 'application/json'}
      response = requests.post(self.API_URL, headers=headers, data=serialized_data)
      #print(response.json())
      return response.json()

   def getExchangeAmount(self, sfrom, sto):
      message = {
         'jsonrpc': '2.0',
         'id': 2,
         'method': 'getExchangeAmount',
         'params': {
             'from': sfrom,  # 'eth',
             'to' : sto,     #'btc',
             'amount' : '1'
         }
      }
      serialized_data = json.dumps(message)
      sign = hmac.new(self.API_SECRET.encode('utf-8'), serialized_data.encode('utf-8'), hashlib.sha512).hexdigest()
      headers = {'api-key': self.API_KEY, 'sign': sign, 'Content-type': 'application/json'}
      response = requests.post(self.API_URL, headers=headers, data=serialized_data)
      # print(response.json())
      return response.json()
   '''

