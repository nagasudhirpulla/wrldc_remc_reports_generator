# https://stackoverflow.com/questions/13034496/using-global-variables-between-files
# https://www.programiz.com/python-programming/global-keyword
from data_fetchers.inp_ts_data_df_fetch import fetchDummyTsInpData, fetchPrevDummyTsInpData
from operator import add
import re
import pandas as pd


def initDummy():
    global tsDataDf
    tsDataDf = fetchDummyTsInpData()

def initPrevDummy():
    global tsPrevDataDf
    tsPrevDataDf = fetchPrevDummyTsInpData()

def getPntData(pnt):
    # returns a series of point data
    global tsDataDf
    if pnt == None:
        return None
    elif "," in pnt:
        return getPntsData(pnt.split(','))
    if "{" in pnt:
        return getEqPntData(pnt)
    else:
        return tsDataDf[pnt]


def getSinglePntData(pnt):
    # returns a series of point data
    global tsDataDf
    return tsDataDf[pnt.replace(' ', '')]


def getPntsData(pnts):
    # returns a sum of points data
    # https://stackoverflow.com/questions/18713321/element-wise-addition-of-2-lists
    if len(pnts) == 0:
        return None
    resVals = getPntData(pnts[0])
    for pnt in pnts[1:]:
        resVals = list(map(add, resVals, getPntData(pnt)))
    return pd.Series(resVals)


def getEqPntData(pntEq):
    global tsDataDf
    # returns data for points equation like {a}+{b}-{x}
    # https://stackoverflow.com/a/4894134/2746323
    pnts = re.findall('{.*?}', pntEq.replace(' ', ''))
    pnts = [pnt[1:-1] for pnt in pnts]
    numericEq = pntEq.replace('{', '').replace('}', '')
    resVals = []
    # iterate through each timestamp of the datastore
    for samplItr in (tsDataDf.shape[0]):
        samplEq = numericEq
        for pnt in pnts:
            samplEq = samplEq.replace(pnt, str(tsDataDf[pnt].iloc[samplItr]))
        sampleVal = eval(samplEq)
        resVals.append(sampleVal)
    return pd.Series(resVals)
