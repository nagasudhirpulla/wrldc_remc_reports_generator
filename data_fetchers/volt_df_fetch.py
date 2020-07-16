import pandas as pd
import datetime as dt
import os

def fetchVoltDf():
    fPath = r'input_data\volt\volt.xlsx'
    if not(os.path.exists(fPath)):
        yestDate = dt.datetime.now() - dt.timedelta(days=1)
        yestDateStr = '{0}{1}{2}'.format(yestDate.year, yestDate.month, yestDate.day)
        fPath = r'input_data\volt\{0}.xlsx'.format(yestDateStr)
    voltDf = pd.read_excel(fPath, skiprows=9)
    return voltDf

def fetchPrevVoltDf():
    fPath = r'input_data\volt\volt_prev.xlsx'
    if not(os.path.exists(fPath)):
        yestDate = dt.datetime.now() - dt.timedelta(days=2)
        yestDateStr = dt.datetime.strftime(yestDate, '%Y%-m%-d')
        fPath = r'input_data\volt\{0}.xlsx'.format(yestDateStr)
    voltDf = pd.read_excel(fPath, skiprows=9)
    return voltDf