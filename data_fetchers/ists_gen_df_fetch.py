import pandas as pd

def fetchDummyIstsGenDf():
    istsGenDf = pd.read_excel(r'dummy_data\ists_gen.xlsx', skiprows=9, skipfooter=1)
    return istsGenDf