import sys
import numpy as np
import numpy.matlib
from enum import Enum
''' Main Doc

DESIGN NOTES:
- Dictionary with multi-dimensional keys like below cannot be used because it is not possible to search for values and 
retrieve keys efficiently.
ee['btc']
Out[37]: {'abc': 1, 'def': 2, 'eth': 8, 'zcg': 9}
ee.values()
Out[38]: [{}, {}, {'abc': 1, 'def': 2, 'eth': 8, 'zcg': 9}]

    BTC-BTC
    BTC-ETH  =
    BTC-LTC

    ETH-BTC
    ETH-ETH
    ETH-LTC

    LTC-BTC
    LTC-ETH
    LTC-LTC

Run:
1. Running in PyCharm's Terminal:
C:\Users\chee\Anaconda2\python.exe arbitrage.py


'''
class Exch(object):
    def __init__(self):
        try:
            rateMatrix, lstrCoin = self.getCoinRates()
            self.rateMatrix = rateMatrix
            self.lstrCoin = lstrCoin
        except:
            print "Unexpected error in Exch.init():", sys.exc_info()[0]
            raise

        return

    # TO DO: get real exch
    def getCoinRates(self):
        try:
            rateMatrix = np.array([ (1, 0.2, 0.3), (0.4, 1, 0.6), (0.7, 0.8, 1) ])   #FAKE
            lstrCoin = ["BTC", "ETH", "LTC"]  # FAKE
        except:
            print "Unexpected error in Exch.getCoinRates():", sys.exc_info()[0]
            raise

        return rateMatrix, lstrCoin
# End of Class

def createUniqueCoin(lCoin):
    try:
        nn = len(lCoin)
        dCoin = dict()
        for ii in range(nn):
            #print ii
            dCoin[lCoin[ii]] = ii
    except:
        print "Unexpected error in createUniqueCoin():", sys.exc_info()[0]
        raise

    return dCoin

def calc1D(aExch):
    try:
        nCoin = 3

        #rateMatrix, lStrCoin = getCoinRates()                # ORDERED List of Strings of Coin names
        rateMatrix = aExch.rateMatrix
        lStrCoin = aExch.lstrCoin
        if nCoin != len(lStrCoin):
            sys.exit(3)
        dctiCoinCode = createUniqueCoin(lStrCoin)     # UNORDERED Dictionary of Coin names to Integer code
        #print(dEx)
        #intCoin1D = np.zeros([len(lStrCoin)])
        intCoin1D = np.array([dctiCoinCode[key] for key in lStrCoin])   # Coin ID integer valued
        intCoin1D = np.reshape(intCoin1D, [len(lStrCoin),1])
        print(intCoin1D.shape)
        print("##### HOLD #####")
        dRateResult1D = np.ones(nCoin)  # Coin Rate is ALL 1.0, since no exchange yet.
    except:
        print "Unexpected error in calc1D():", sys.exc_info()[0]
        raise

    return rateMatrix, intCoin1D, dRateResult1D, dctiCoinCode

def calc2D(intCoin1D, dRateResult1D, rateMatrix):
    '''
    OBSOLETE - the same result can be achived by using calcND
    :return:
    '''
    try:
        nrow = intCoin1D.size
        ncol = rateMatrix.shape[1]    # the second dimension
        intCoin2D = np.zeros([nrow*ncol, 2], order='C', dtype=np.int)      # This is 2 column, ie due to two coins, ie rate between a pair of coins.
        dRateResult2D = np.zeros(nrow * ncol)     # 2D here is NOT the dimension, but rates between 2 coins.

        print(intCoin2D.shape)      # eg (9L, 2L)
        print(type(intCoin1D[0]))   # eg <type 'numpy.int32'>
        print(rateMatrix)
        #eg [[ 1.   0.2  0.3]
        # [ 0.4  1.   0.6]
        # [ 0.7  0.8  1. ]]

        print(dRateResult1D)   # eg [ 1.  1.  1.]
        # Build Indices
        aOffset = 0
        for ii in intCoin1D:
            print(ii)
            #print(type(ii))
            ltmp = range(aOffset, ncol+aOffset)
            print("ltmp " + str(ltmp))
            intCoin2D[ltmp, 0] = ii
            #print((intCoin2D[ltmp, 1]).shape)
            #print((intCoin1D).shape)
            intCoin2D[ltmp, 1] = intCoin1D[:, 0]
            print(rateMatrix[ii,:])
            dRateResult2D[ltmp] = np.multiply(rateMatrix[ii,:], dRateResult1D)
            print(dRateResult2D[ltmp])
            aOffset = aOffset + ncol        #print(aOffset)
    except:
        print "Unexpected error in calc2D():", sys.exc_info()[0]
        raise

    return intCoin2D, dRateResult2D

def calcND(iND, intCoinN_1D, dRateResultN_1D, rateMatrix, lstrCoin, dctCoin):
    '''
    :return: intCoinN_D with No. of columns corresponding to how many times the rates are changed
    '''
    try:
        nrow = intCoinN_1D.shape[0]
        ncol = rateMatrix.shape[1]    # the second dimension
        intCoinND = np.zeros([nrow*ncol, iND], order='C', dtype=np.int)      # This is 3 or N column, ie due to N coins, ie rate between N of coins.
        dRateResultND = np.zeros(nrow * ncol)     # ND here is NOT the dimension, but rates between N coins.
        dRateResultND_wrtOrig = np.zeros(nrow * ncol)     # Results vector converted back to original coin.

        #print(intCoinND.shape)      # eg (9L, 2L)
        #print(type(intCoinN_1D[0]))   # eg <type 'numpy.int32'>
        #print(rateMatrix)
        #eg [[ 1.   0.2  0.3]
        # [ 0.4  1.   0.6]
        # [ 0.7  0.8  1. ]]

        #print(dRateResultN_1D)   # eg [ 1.  1.  1.]
        # Build Indices
        aOffset = 0
        intCoin1D = np.array([dctCoin[key] for key in lstrCoin])
        #print("Entering For Loop")
        for ii in range(nrow):         # nrow = rows of existing matrix, not expanded one
            #print(ii)
            #print(type(ii))

            # Getting the chunk of index to expand on
            ltmp = range(aOffset, ncol+aOffset)            #print("ltmp " + str(ltmp))
            #print("range iND " + str(range(iND-1)))
            #print("intCoinND")
            #print(intCoinND.shape)
            #print(intCoinND[ltmp, 0:iND-1])
            #print(intCoinN_1D[ii, :].shape)
            # eg iND=3, need 2nd dim to be 0,1, ie leave out 3rd col [:,2]. The index 0,1 is 0:2 = 0:iND-1

            # Calculate the index matrix
            intCoinND[ltmp, 0:iND-1] = intCoinN_1D[ii, :]  # each row of intCoinN_1D, eg BTC-BTC, expanded to ltmp rows
            intCoinND[ltmp, iND-1] = intCoin1D                    # new column iND for new matrix
            #print(intCoinN_1D[ii, iND-2])

            # Calculate the new vector of result
            iFrCoin = intCoinN_1D[ii, iND - 2]                               # coinCode for coin to change from
            lvec = ldGetVector(iFrCoin, rateMatrix, lstrCoin, lstrCoin, dctCoin, dctCoin)            #print(lvec)
            #print(dRateResultN_1D[ii])
            dRateResultND[ltmp] = np.multiply(lvec, dRateResultN_1D[ii])
            #print(dRateResultND[ltmp])

            # Convert the result (dRateResultND) back to the original value.
            intCoinOrig = intCoinN_1D[ii, 0]   # the initial coin that was translated from
            sCoinCode =  lstrCoin[intCoinOrig]
            lvec2 = ldGetRateFromManyToOne(intCoin1D, intCoinOrig, rateMatrix)  # , lstrCoin, lstrCoin, dctCoin, dctCoin)
            dRateResultND_wrtOrig[ltmp] = np.multiply(lvec2, dRateResultND[ltmp])



            aOffset = aOffset + ncol        #print(aOffset)
    except:
        print "Unexpected error in calcND():", sys.exc_info()[0]
        raise

    return intCoinND, dRateResultND, dRateResultND_wrtOrig

def ldGetRateFromManyToOne(lCoinFrom, iToCoin, rateMatrixTo):   #, lstrCoinFrom, lstrCoinTo, dctCoinFrom, dctCoinTo):
    '''
          XXX   ETH  XXX
    BTC [        X       ]    convert BTC to ETH
    ETH [        X       ]    convert ETH to ETH
    LTC [        X       ]    convert LTC to ETH
    :param lCoinFrom: list of coins to convert from
    :param iToCoin:    the coin to convert to
    :param rateMatrixTo:
    :param lstrCoinFrom:
    :param lstrCoinTo:
    :param dctCoinFrom:
    :param dctCoinTo:
    :return:
    '''

    #iToCoin  is the column indicator.
    # find all rows
    try:
        lvec = np.zeros(len(lCoinFrom))
        for ii in  range(len(lCoinFrom)):
            lvec[ii] = rateMatrix[lCoinFrom[ii], iToCoin]
    except:
        print "Unexpected error in ldGetRateFromManyToOne():", sys.exc_info()[0]
        raise

    return lvec



def ldGetVector(iFromCoin, rateMatrixTo, lstrCoinFrom, lstrCoinTo, dctCoinFrom, dctCoinTo):
    '''
    Obtain a list of exchange rates from coin iFromCoin, to all other coins for a given exchange,
    where rateMatrixTo holds the rates of coins of the To Exchange.
    In the general form, the From is the current Exchange, whereas the To can be going to a different Exchange.
    The integer iFromCoin, is used to get the string from lstrCoinFrom. This string code for the coin (sCoinCode)
    is checked against the To list lstrCoinTo, to obtain the index, iToCoin.
    The iToCoin is the row index of the rateMatrix to get the rates for all other coins, ie across all columns
    :param iFromCoin:
    :param rateMatrixTo:
    :param lstrCoinFrom:
    :param lstrCoinTo:
    :param dctCoinFrom:
    :param dctCoinTo:
    :return:
    '''
    try:
        sCoinCode = lstrCoinFrom[iFromCoin]    # This back and forth is needed in case it is a different Exchange
        iToCoin = lstrCoinTo.index(sCoinCode)
        lvec = rateMatrix[iToCoin, :]
    except:
        print "Unexpected error in ldGetVector():", sys.exc_info()[0]
        raise
    return lvec


def printResult(nDim, dctCoinCode, intCoinArray, dRateResult, lStrCoin):
    try:
        if (nDim != intCoinArray.shape[1]):
            print("printResult: nDim not same as number of Columns of intCoinArrray")
        if (dRateResult.size != intCoinArray.shape[0]):
            print("printResult: Size of Result not same as number of Rows of intCoinArrray")
        for ii in range(dRateResult.size):
            sCodeChain = ''    # Build this into eg BTC-ETC-LTC...
            for jj in range(intCoinArray.shape[1]):  # eg jj in
                iCoinCode = intCoinArray[ii, jj]
                if sCodeChain == '':
                    sCodeChain = lStrCoin[iCoinCode]
                else:
                    sCodeChain = sCodeChain + '-' + lStrCoin[iCoinCode]
            print(sCodeChain + " $" + str(dRateResult[ii]))
    except:
        print "Unexpected error in printResult():", sys.exc_info()[0]
        raise

    return



if __name__ == '__main__':
    try:
        print("Start Arbitrage")

        aExch = Exch()
        rateMatrix, intCoin1D, dRateResult1D, dctCoinCode = calc1D(aExch)

        print(intCoin1D)
        print(dRateResult1D)
        print(rateMatrix)
        print(dctCoinCode)


        #intCoin2D, dRateResult2D = calc2D(intCoin1D, dRateResult1D, rateMatrix)  #Same as below
        intCoin2D, dRateResult2D, dRateResult2DwrtOrig = calcND(2, intCoin1D, dRateResult1D, rateMatrix, aExch.lstrCoin, dctCoinCode)
        print("###############")
        print(intCoin2D)
        print(dRateResult2D)
        print(dRateResult2DwrtOrig)

        #printResult(2, dctCoinCode, intCoin2D, dRateResult2D, aExch.lstrCoin)

        intCoin3D, dRateResult3D, dRateResult3DwrtOrig = calcND(3, intCoin2D, dRateResult2D, rateMatrix, aExch.lstrCoin, dctCoinCode)
        print("###############")
        print(intCoin3D)
        print(dRateResult3D)
        print(dRateResult3DwrtOrig)

        intCoin4D, dRateResult4D, dRateResult4DwrtOrig = calcND(4, intCoin3D, dRateResult3D, rateMatrix, aExch.lstrCoin, dctCoinCode)
        print("###############")
        print(intCoin4D)
        print(dRateResult4D)
        print(dRateResult4DwrtOrig)
        sys.exit(33)



        a2D = np.array([ (1, 0.2, 0.3), (0.4, 1, 0.6), (0.7, 0.8, 1) ])
        print("2D - dim = " + str(a2D.ndim))
        print("shape = " + str(a2D.shape))
        print(a2D)

        nrow = 3
        nrow1 = nrow -1
        rates = dict()
        rates[(2,3)] = 0.3
        rates[(5, 1)] = 0.5
        #print(rates[1])

        rate_prod1d = [1,1,1]
        test1d = [2,1,3]
        for ii in range(0,nrow) :
            print(ii)
            aRow = a2D[ii,:]
            print(aRow)

        c1d = rate_prod1d * aRow
        print(c1d)


    except:
        print "Unexpected error in main:", sys.exc_info()[0]
        raise
