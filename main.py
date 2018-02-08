import hashlib
import hmac
import json

import requests
import changelly
import thread
import threading
import time
import sys
#from multiprocessing.dummy import Pool as ThreadPool

# Initialize for Changelly exchange
exChangelly = changelly.Changelly()

'''
getCurr = exChangelly.getCurrencies()
print (getCurr)

getAmount = exChangelly.getExchangeAmount('xmr', 'eth')
print (getAmount)
'''

print("decorators")
xxx = exChangelly.getCurrenciesJson();
print(xxx)

lCurrencies = xxx['result']
# Restrict list for testing
#lCurrencies = lCurrencies[1:24]
print (lCurrencies)
dctMain = {}

class myThread(threading.Thread):

   def __init__(self, threadID, name, sfromExch):
       threading.Thread.__init__(self)
       self.threadID = threadID
       self.name = name
       self.sfromExch = sfromExch

   def run(self):
      while True:
         try:
            print "Starting " + self.name
            dctMain[self.sfromExch] = getExchangeTo(self.sfromExch, lCurrencies)
            print "Exiting " + self.name
            return
         except:
            pass

def getExchangeTo(sfrom, sExchList):
   """

   :param sfrom:
   :param sExchList:
   :return:
   """
   dctEx={}
   print ('Xchange from {0}'.format(sfrom))
   for sto in [key for key in sExchList if key != sfrom]:
      #print ('{0}, {1}'.format(ii, jj))
      yyy = exChangelly.getExchangeAmountJson(exChangelly, sfrom, sto)
      #print (yyy)
      #print ('{0}, {1}, {2}'.format(sfrom, sto, yyy['result']))
      dctEx[sto] = yyy['result']
   return dctEx

# Create new threads
#thread1 = myThread(1, "t1", 'btc')
#thread2 = myThread(2, "t2", 'eth')

#tt=list[len(lCurrencies)]
lthreads=[]
icount = 1
for ii in lCurrencies:
   print ii
   lthreads.append( myThread(icount, ii, ii) )
   icount = icount + 1

for ithread in lthreads:
   ithread.start()
   time.sleep(0.5)

# Start new threads
#thread1.start()
#thread2.start()

print ("Thread completed")
sys.exit(1)

dExch={}


'''    
for ii in lCurrencies:
   dExch[ii]={}
      for jj in [key for key in lCurrencies if key != ii]:
         print ('{0}, {1}'.format(ii, jj))
         yyy = exChangelly.getExchangeAmountJson(exChangelly, ii, jj)
         print (yyy)
         print ('{0}, {1}, {2}'.format(ii, jj, yyy['result']))
   )
   '''
print (dExch)
#print("exchange")
#yyy = exChangelly.getExchangeAmountJson(exChangelly, 'xmr','eth');
#print(yyy)