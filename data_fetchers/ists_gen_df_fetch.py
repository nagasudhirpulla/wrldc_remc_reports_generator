import pandas as pd
import os
import datetime as dt


def fetchIstsGenDf():
    fPath = r'input_data\ists_gen\ists_gen.xlsx'
    # if input_data\ists_gen\ists_gen.xlsx not exists
    if not(os.path.exists(fPath)):
        yestDate = dt.datetime.now()
        yestDateStr = '{0}{1}{2}'.format(yestDate.year, yestDate.month, yestDate.day)
        fPath = r'input_data\ists_gen\{0}.xlsx'.format(yestDateStr)
    istsGenDf = pd.read_excel(fPath, skiprows=9, skipfooter=1)
    return istsGenDf


def fetchPrevIstsGenDf():
    fPath = r'input_data\ists_gen\ists_gen_prev.xlsx'
    # if input_data\ists_gen\ists_gen_prev.xlsx not exists
    if not(os.path.exists(fPath)):
        yestDate = dt.datetime.now() - dt.timedelta(days=1)
        yestDateStr = dt.datetime.strftime(yestDate, '%Y%-m%-d')
        fPath = r'input_data\ists_gen\{0}.xlsx'.format(yestDateStr)
    istsGenDf = pd.read_excel(fPath, skiprows=9, skipfooter=1)
    return istsGenDf
