# https://stackoverflow.com/questions/13034496/using-global-variables-between-files
# https://www.programiz.com/python-programming/global-keyword
from data_fetchers.inp_ts_data_df_fetch import fetchDummyTsInpData
from operator import add
import re

def initDummy():
    global tsDataDf
    tsDataDf = fetchDummyTsInpData()


def getPntData(pnt):
    # returns a series of point data
    global tsDataDf
    return tsDataDf[pnt]


def getPntsData(pnts):
    # returns a sum of points data
    # https://stackoverflow.com/questions/18713321/element-wise-addition-of-2-lists
    if len(pnts) == 0:
        return None
    resVals = getPntData(pnts[0])
    for pnt in pnts[1:]:
        resVals = list(map(add, resVals, getPntData(pnt)))
    return resVals

def getEqPntData(pntEq):
    # returns data for points equation like {a}+{b}-{x}
    # https://stackoverflow.com/a/4894134/2746323
    pnts = re.findall('{.*?}',pntEq)
    pnts = [pnt[1:-1] for pnt in pnts]
    numericEq = pntEq.replace('{', '').replace('}', '')
    ## todo complete this