from data_fetchers.remc_fetchers import fetchFcaDayAheadDf, fetchFcaForeVsActDf, fetchIftDayAheadDf, fetchIftForeVsActDf, fetchAleaDayAheadDf, fetchAleaForeVsActDf, fetchEnerDayAheadDf, fetchEnerForeVsActDf, fetchResDayAheadDf, fetchResForeVsActDf
import pandas as pd
from operator import add

# constants for data store names
FCA_DAY_AHEAD_STORE_NAME = 'fcaDayAheadStore'
FCA_FORECAST_VS_ACTUAL_STORE_NAME = 'fcaForecastVsActualStore'
IFT_DAY_AHEAD_STORE_NAME = 'iftDayAheadStore'
IFT_FORECAST_VS_ACTUAL_STORE_NAME = 'iftForecastVsActualStore'
ALEA_DAY_AHEAD_STORE_NAME = 'aleaDayAheadStore'
ALEA_FORECAST_VS_ACTUAL_STORE_NAME = 'aleaForecastVsActualStore'
ENER_DAY_AHEAD_STORE_NAME = 'enerDayAheadStore'
ENER_FORECAST_VS_ACTUAL_STORE_NAME = 'enerForecastVsActualStore'
RES_DAY_AHEAD_STORE_NAME = 'resDayAheadStore'
RES_FORECAST_VS_ACTUAL_STORE_NAME = 'resForecastVsActualStore'


def loadRemcDataStore(storeName):
    global g_fcaDayAheadDf
    global g_fcaForecastVsActual
    global g_iftDayAheadDf
    global g_iftForecastVsActual
    global g_aleaDayAheadDf
    global g_aleaForecastVsActual
    global g_enerDayAheadDf
    global g_enerForecastVsActual
    global g_resDayAheadDf
    global g_resForecastVsActual

    if storeName == FCA_DAY_AHEAD_STORE_NAME:
        g_fcaDayAheadDf = fetchFcaDayAheadDf()
    elif storeName == FCA_FORECAST_VS_ACTUAL_STORE_NAME:
        g_fcaForecastVsActual = fetchFcaForeVsActDf()
    elif storeName == IFT_DAY_AHEAD_STORE_NAME:
        g_iftDayAheadDf = fetchIftDayAheadDf()
    elif storeName == IFT_FORECAST_VS_ACTUAL_STORE_NAME:
        g_iftForecastVsActual = fetchIftForeVsActDf()
    elif storeName == ALEA_DAY_AHEAD_STORE_NAME:
        g_aleaDayAheadDf = fetchAleaDayAheadDf()
    elif storeName == ALEA_FORECAST_VS_ACTUAL_STORE_NAME:
        g_aleaForecastVsActual = fetchAleaForeVsActDf()
    elif storeName == ENER_DAY_AHEAD_STORE_NAME:
        g_enerDayAheadDf = fetchEnerDayAheadDf()
    elif storeName == ENER_FORECAST_VS_ACTUAL_STORE_NAME:
        g_enerForecastVsActual = fetchEnerForeVsActDf()
    elif storeName == RES_DAY_AHEAD_STORE_NAME:
        g_resDayAheadDf = fetchResDayAheadDf()
    elif storeName == RES_FORECAST_VS_ACTUAL_STORE_NAME:
        g_resForecastVsActual = fetchResForeVsActDf()


def deleteRemcDataStore(storeName):
    global g_fcaDayAheadDf
    global g_fcaForecastVsActual
    global g_iftDayAheadDf
    global g_iftForecastVsActual
    global g_aleaDayAheadDf
    global g_aleaForecastVsActual
    global g_enerDayAheadDf
    global g_enerForecastVsActual
    global g_resDayAheadDf
    global g_resForecastVsActual

    if storeName == FCA_DAY_AHEAD_STORE_NAME:
        g_fcaDayAheadDf = pd.DataFrame()
    elif storeName == FCA_FORECAST_VS_ACTUAL_STORE_NAME:
        g_fcaForecastVsActual = pd.DataFrame()
    elif storeName == IFT_DAY_AHEAD_STORE_NAME:
        g_iftDayAheadDf = pd.DataFrame()
    elif storeName == IFT_FORECAST_VS_ACTUAL_STORE_NAME:
        g_iftForecastVsActual = pd.DataFrame()
    elif storeName == ALEA_DAY_AHEAD_STORE_NAME:
        g_aleaDayAheadDf = pd.DataFrame()
    elif storeName == ALEA_FORECAST_VS_ACTUAL_STORE_NAME:
        g_aleaForecastVsActual = pd.DataFrame()
    elif storeName == ENER_DAY_AHEAD_STORE_NAME:
        g_enerDayAheadDf = pd.DataFrame()
    elif storeName == ENER_FORECAST_VS_ACTUAL_STORE_NAME:
        g_enerForecastVsActual = pd.DataFrame()
    elif storeName == RES_DAY_AHEAD_STORE_NAME:
        g_resDayAheadDf = pd.DataFrame()
    elif storeName == RES_FORECAST_VS_ACTUAL_STORE_NAME:
        g_resForecastVsActual = pd.DataFrame()


def getRemcPntData(storeName, pnt):
    # returns a pandas series of remc point data
    global g_fcaDayAheadDf
    global g_fcaForecastVsActual
    global g_iftDayAheadDf
    global g_iftForecastVsActual
    global g_aleaDayAheadDf
    global g_aleaForecastVsActual
    global g_enerDayAheadDf
    global g_enerForecastVsActual
    global g_resDayAheadDf
    global g_resForecastVsActual

    if storeName == FCA_DAY_AHEAD_STORE_NAME:
        tsDf = g_fcaDayAheadDf
    elif storeName == FCA_FORECAST_VS_ACTUAL_STORE_NAME:
        tsDf = g_fcaForecastVsActual
    elif storeName == IFT_DAY_AHEAD_STORE_NAME:
        tsDf = g_iftDayAheadDf
    elif storeName == IFT_FORECAST_VS_ACTUAL_STORE_NAME:
        tsDf = g_iftForecastVsActual
    elif storeName == ALEA_DAY_AHEAD_STORE_NAME:
        tsDf = g_aleaDayAheadDf
    elif storeName == ALEA_FORECAST_VS_ACTUAL_STORE_NAME:
        tsDf = g_aleaForecastVsActual
    elif storeName == ENER_DAY_AHEAD_STORE_NAME:
        tsDf = g_enerDayAheadDf
    elif storeName == ENER_FORECAST_VS_ACTUAL_STORE_NAME:
        tsDf = g_enerForecastVsActual
    elif storeName == RES_DAY_AHEAD_STORE_NAME:
        tsDf = g_resDayAheadDf
    elif storeName == RES_FORECAST_VS_ACTUAL_STORE_NAME:
        tsDf = g_resForecastVsActual
    else:
        return None

    if (pd.isnull(pnt) or (pnt == '')):
        return None
    if "," in pnt:
        pnts = pnt.split(',')
        if len(pnts) == 0:
            return None
        resVals = tsDf[pnts[0]]
        for pnt in pnts[1:]:
            if (pd.isnull(pnt) or (pnt == '')):
                continue
            resVals = list(map(add, resVals, tsDf[pnt]))
        return pd.Series(resVals)
    else:
        return tsDf[pnt]
