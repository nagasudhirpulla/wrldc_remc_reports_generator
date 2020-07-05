import pandas as pd

def fetchTotGenDf():
    totGenDf = pd.read_excel(r'input_data\totgen.xlsx', skiprows=9, skipfooter=1)
    return totGenDf

def fetchPrevTotGenDf():
    totGenDf = pd.read_excel(r'input_data\totgen_prev.xlsx', skiprows=9, skipfooter=1)
    return totGenDf