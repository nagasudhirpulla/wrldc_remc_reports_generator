import pandas as pd
import datetime as dt
import os

def fetchTotGenDf():
    fPath = r'input_data\tot_gen\tot_gen.xlsx'
    if not(os.path.exists(fPath)):
        yestDate = dt.datetime.now() - dt.timedelta(days=1)
        yestDateStr = dt.datetime.strftime(yestDate, '%Y%-m%-d')
        fPath = r'input_data\tot_gen\{0}.xlsx'.format(yestDateStr)
    totGenDf = pd.read_excel(fPath, skiprows=9, skipfooter=1)
    return totGenDf

def fetchPrevTotGenDf():
    fPath = r'input_data\tot_gen\tot_gen_prev.xlsx'
    if not(os.path.exists(fPath)):
        yestDate = dt.datetime.now() - dt.timedelta(days=2)
        yestDateStr = dt.datetime.strftime(yestDate, '%Y%-m%-d')
        fPath = r'input_data\tot_gen\{0}.xlsx'.format(yestDateStr)
    totGenDf = pd.read_excel(fPath, skiprows=9, skipfooter=1)
    return totGenDf