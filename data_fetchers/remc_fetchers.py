import pandas as pd
import datetime as dt
import os

def getDateStr(numDays):
    reqDate = dt.datetime.now() + dt.timedelta(days=numDays)
    return dt.datetime.strftime(reqDate, '%Y-%m-%d')
        
def fetchFcaDayAheadDf():
    fPath = r'input_data\fca\DAY_AHED.csv'
    if not(os.path.exists(fPath)):
        fPath = r'input_data\fca\DAY_AHED_{0}.xlsx'.format(getDateStr(0))
    fcaDayAheadDf = pd.read_csv(fPath)
    fcaDayAheadDf.columns = [x.strip()
                             for x in list(fcaDayAheadDf.columns.values)]
    return fcaDayAheadDf


def fetchFcaForeVsActDf():
    fPath = r'input_data\fca\FC_VS_AC.csv'
    if not(os.path.exists(fPath)):
        fPath = r'input_data\fca\FC_VS_AC_{0}.xlsx'.format(getDateStr(0))
    fcaForeVsActDf = pd.read_csv(fPath)
    return fcaForeVsActDf

def fetchFcaForeVsActPrevDf():
    fPath = r'input_data\fca\FC_VS_AC_PREV.csv'
    if not(os.path.exists(fPath)):
        fPath = r'input_data\fca\FC_VS_AC_{0}.xlsx'.format(getDateStr(-1))
    fcaForeVsActPrevDf = pd.read_csv(fPath)
    return fcaForeVsActPrevDf

def fetchIftDayAheadDf():
    fPath = r'input_data\ift\DAY_AHED.csv'
    if not(os.path.exists(fPath)):
        fPath = r'input_data\ift\DAY_AHED_{0}.xlsx'.format(getDateStr(0))
    iftDayAheadDf = pd.read_csv(fPath)
    iftDayAheadDf.columns = [x.strip()
                             for x in list(iftDayAheadDf.columns.values)]
    return iftDayAheadDf


def fetchIftForeVsActDf():
    fPath = r'input_data\ift\FC_VS_AC.csv'
    if not(os.path.exists(fPath)):
        fPath = r'input_data\ift\FC_VS_AC_{0}.xlsx'.format(getDateStr(0))
    iftForeVsActDf = pd.read_csv(r'input_data\ift\FC_VS_AC.csv')
    return iftForeVsActDf


def fetchResDayAheadDf():
    fPath = r'input_data\res\DAY_AHED.csv'
    if not(os.path.exists(fPath)):
        fPath = r'input_data\res\DAY_AHED_{0}.xlsx'.format(getDateStr(0))
    resDayAheadDf = pd.read_csv(fPath)
    resDayAheadDf.columns = [x.strip()
                             for x in list(resDayAheadDf.columns.values)]
    return resDayAheadDf


def fetchResForeVsActDf():
    fPath = r'input_data\res\FC_VS_AC.csv'
    if not(os.path.exists(fPath)):
        fPath = r'input_data\res\FC_VS_AC_{0}.xlsx'.format(getDateStr(0))
    resForeVsActDf = pd.read_csv(r'input_data\res\FC_VS_AC.csv')
    return resForeVsActDf


def fetchAleaDayAheadDf():
    fPath = r'input_data\aleasoft\DAY_AHED.csv'
    if not(os.path.exists(fPath)):
        fPath = r'input_data\aleasoft\DAY_AHED_{0}.xlsx'.format(getDateStr(0))
    aleaDayAheadDf = pd.read_csv(fPath)
    aleaDayAheadDf.columns = [x.strip()
                             for x in list(aleaDayAheadDf.columns.values)]
    return aleaDayAheadDf


def fetchAleaForeVsActDf():
    fPath = r'input_data\aleasoft\FC_VS_AC.csv'
    if not(os.path.exists(fPath)):
        fPath = r'input_data\aleasoft\FC_VS_AC_{0}.xlsx'.format(getDateStr(0))
    aleaForeVsActDf = pd.read_csv(fPath)
    return aleaForeVsActDf


def fetchEnerDayAheadDf():
    fPath = r'input_data\enercast\DAY_AHED.csv'
    if not(os.path.exists(fPath)):
        fPath = r'input_data\enercast\DAY_AHED_{0}.xlsx'.format(getDateStr(0))
    enerDayAheadDf = pd.read_csv(fPath)
    enerDayAheadDf.columns = [x.strip()
                             for x in list(enerDayAheadDf.columns.values)]
    return enerDayAheadDf


def fetchEnerForeVsActDf():
    fPath = r'input_data\enercast\FC_VS_AC.csv'
    if not(os.path.exists(fPath)):
        fPath = r'input_data\enercast\FC_VS_AC_{0}.xlsx'.format(getDateStr(0))
    enerForeVsActDf = pd.read_csv(fPath)
    return enerForeVsActDf
