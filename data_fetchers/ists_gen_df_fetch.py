import pandas as pd

def fetchDummyIstsGenDf():
    istsGenDf = pd.read_excel(r'dummy_data\202071_ists_gen.xlsx', skiprows=9, skip_footer=1)
    return istsGenDf