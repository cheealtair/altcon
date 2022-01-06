'''

HISTORY
06Jan2022     Migrated from Python 2 to 3, changing print() syntax. Debugged and working now with threading.
'''

import hashlib
import hmac
import json

import requests
import changelly
#import thread
import threading
import time
import sys
#from multiprocessing.dummy import Pool as ThreadPool

# Initialize for Changelly exchange
exChangelly = changelly.Changelly()

getCurr = exChangelly.getCurrenciesJson()
print (getCurr)
print(getCurr['result'])

getAmount = exChangelly.getExchangeAmountJson('xmr', 'eth')
print (getAmount)


lCurrencies = getCurr['result']
dctMain = {}

yyy = exChangelly.getRate('xmr','eth')
print(yyy)


class myThread(threading.Thread):
    def __init__(self, threadID, name, sfromExch):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.sfromExch = sfromExch
        
    def run(self):
        isRan = False
        print("Starting " + self.name)
        dctMain[self.sfromExch] = getExchangeTo(self.sfromExch, lCurrencies[:5])
        print("Exiting " + self.name)


def getExchangeTo(sfrom, sExchList):
    """
    :param sfrom:
    :param sExchList:
    :return:
    """
    dctEx={}
    print ('Xchange from {0}'.format(sfrom))
    for sto in [key for key in sExchList if key != sfrom]:
        yyy = exChangelly.getExchangeAmountJson( sfrom, sto)
        if 'error' in yyy:
            smessage = yyy['error']
            print(smessage['message'])
        else:
            dctEx[sto] = yyy['result']
    print(dctEx)
    return dctEx


lthreads=[]
icount = 1
for ii in lCurrencies[:5]:
    print(ii)
    lthreads.append( myThread(icount, ii, ii) )
    icount = icount + 1

for ithread in lthreads:
    ithread.start()
    time.sleep(0.5)
    ithread.join()


print ("Thread completed")

