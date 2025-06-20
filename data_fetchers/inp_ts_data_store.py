# https://stackoverflow.com/questions/13034496/using-global-variables-between-files
# https://www.programiz.com/python-programming/global-keyword
import enum
from data_fetchers.inp_ts_data_df_fetch import fetchTsInpData, fetchPrevTsInpData
from data_fetchers.point_ids_df_fetch import fetchPointIdsDf
from data_fetchers.volt_df_fetch import fetchVoltDf
from operator import add
import re
import pandas as pd

def loadPointIdsData(configFilePath, pointsSheet):
    global pointIdsDf
    pointIdsDf = fetchPointIdsDf(configFilePath, pointsSheet)


@enum.unique
class PointIdTypes(str, enum.Enum):
    installed_capacity = 'installed_capacity',
    actual_point = 'actual_point',
    sch_point = 'sch_point',
    pooling_station = 'pooling_station',
    gen_type1 = 'gen_type1',
    entity_type = 'entity_type',
    r0_pnt = 'r0_pnt',
    r16_pnt = 'r16_pnt',
    actual_pnt_sch = 'actual_pnt_sch',
    cuf_pnt = 'cuf_pnt',
    avc_point = 'avc_point',
    forecast_point = 'forecast_point'
    wbes_acr = 'wbes_acr'

def loadGenTsData():
    global tsDataDf
    tsDataDf = fetchTsInpData()

def loadVoltTsData():
    global tsDataDf
    tsDataDf = fetchVoltDf()

def deleteTsData():
    global tsDataDf
    tsDataDf = pd.DataFrame()

def initPrevData():
    global tsPrevDataDf
    tsPrevDataDf = fetchPrevTsInpData()

def getEntityPointIds(entityName):
    pointIdsDict = pointIdsDf.loc[entityName].to_dict()
    return pointIdsDict

def getPntData(pnt, isPrev=False):
    # returns a pandas series of point data
    global tsDataDf
    global tsPrevDataDf
    if (pd.isnull(pnt) or (pnt == '')):
        return None
    if "," in pnt:
        return getPntsData(pnt.split(','), isPrev)
    if "{" in pnt:
        return getEqPntData(pnt, isPrev)
    else:
        if isPrev == True:
            return tsPrevDataDf[pnt]
        return tsDataDf[pnt]


def getSinglePntData(pnt, isPrev=False):
    # returns a pandas series of point data
    global tsDataDf
    global tsPrevDataDf
    if isPrev == True:
        return tsPrevDataDf[pnt.replace(' ', '')]
    return tsDataDf[pnt.replace(' ', '')]


def getPntsData(pnts, isPrev=False):
    # returns a sum of points data
    # https://stackoverflow.com/questions/18713321/element-wise-addition-of-2-lists
    if len(pnts) == 0:
        return None
    resVals = getPntData(pnts[0], isPrev)
    for pnt in pnts[1:]:
        if (pd.isnull(pnt) or (pnt == '')):
            continue
        resVals = list(map(add, resVals, getPntData(pnt, isPrev)))
    return pd.Series(resVals)


def getEqPntData(pntEq, isPrev=False):
    global tsDataDf
    global tsPrevDataDf
    # returns data for points equation like {a}+{b}-{x}
    # https://stackoverflow.com/a/4894134/2746323
    pnts = re.findall('{.*?}', pntEq.replace(' ', ''))
    pnts = [pnt[1:-1] for pnt in pnts]
    numericEq = pntEq.replace('{', '').replace('}', '')
    resVals = []
    # iterate through each timestamp of the datastore
    if isPrev == True:
        numStoreRows = tsPrevDataDf.shape[0]
    else:
        numStoreRows = tsDataDf.shape[0]
    for samplItr in range(numStoreRows):
        samplEq = numericEq
        for pnt in pnts:
            if isPrev == True:
                samplEq = samplEq.replace(
                    pnt, str(tsPrevDataDf[pnt].iloc[samplItr]))
            else:
                samplEq = samplEq.replace(
                    pnt, str(tsDataDf[pnt].iloc[samplItr]))
        sampleVal = eval(samplEq)
        resVals.append(sampleVal)
    return pd.Series(resVals)
