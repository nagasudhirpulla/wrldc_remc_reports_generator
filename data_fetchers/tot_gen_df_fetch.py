import pandas as pd

def fetchDummyTotGenDf():
    totGenDf = pd.read_excel(r'dummy_data\202071_totgen.xlsx', skiprows=9, skipfooter=1)
    return totGenDf