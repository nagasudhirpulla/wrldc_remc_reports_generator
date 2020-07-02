import pandas as pd

def fetchDummyTotGenDf():
    totGenDf = pd.read_excel(r'dummy_data\totgen.xlsx', skiprows=9, skipfooter=1)
    return totGenDf

def fetchDummyPrevTotGenDf():
    totGenDf = pd.read_excel(r'dummy_data\totgen_prev.xlsx', skiprows=9, skipfooter=1)
    return totGenDf