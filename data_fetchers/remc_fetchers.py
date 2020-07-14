import pandas as pd


def fetchFcaDayAheadDf():
    fcaDayAheadDf = pd.read_csv(r'input_data\fca\DAY_AHED.csv')
    fcaDayAheadDf.columns = [x.strip()
                             for x in list(fcaDayAheadDf.columns.values)]
    return fcaDayAheadDf


def fetchFcaForeVsActDf():
    fcaForeVsActDf = pd.read_csv(r'input_data\fca\FC_VS_AC.csv')
    return fcaForeVsActDf

def fetchFcaForeVsActPrevDf():
    fcaForeVsActPrevDf = pd.read_csv(r'input_data\fca\FC_VS_AC_PREV.csv')
    return fcaForeVsActPrevDf

def fetchIftDayAheadDf():
    iftDayAheadDf = pd.read_csv(r'input_data\ift\DAY_AHED.csv')
    iftDayAheadDf.columns = [x.strip()
                             for x in list(iftDayAheadDf.columns.values)]
    return iftDayAheadDf


def fetchIftForeVsActDf():
    iftForeVsActDf = pd.read_csv(r'input_data\ift\FC_VS_AC.csv')
    return iftForeVsActDf


def fetchResDayAheadDf():
    resDayAheadDf = pd.read_csv(r'input_data\res\DAY_AHED.csv')
    resDayAheadDf.columns = [x.strip()
                             for x in list(resDayAheadDf.columns.values)]
    return resDayAheadDf


def fetchResForeVsActDf():
    resForeVsActDf = pd.read_csv(r'input_data\res\FC_VS_AC.csv')
    return resForeVsActDf


def fetchAleaDayAheadDf():
    aleaDayAheadDf = pd.read_csv(r'input_data\aleasoft\DAY_AHED.csv')
    aleaDayAheadDf.columns = [x.strip()
                             for x in list(aleaDayAheadDf.columns.values)]
    return aleaDayAheadDf


def fetchAleaForeVsActDf():
    aleaForeVsActDf = pd.read_csv(r'input_data\aleasoft\FC_VS_AC.csv')
    return aleaForeVsActDf


def fetchEnerDayAheadDf():
    enerDayAheadDf = pd.read_csv(r'input_data\enercast\DAY_AHED.csv')
    enerDayAheadDf.columns = [x.strip()
                             for x in list(enerDayAheadDf.columns.values)]
    return enerDayAheadDf


def fetchEnerForeVsActDf():
    enerForeVsActDf = pd.read_csv(r'input_data\enercast\FC_VS_AC.csv')
    return enerForeVsActDf
