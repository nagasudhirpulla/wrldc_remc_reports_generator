import pandas as pd

def fetchIstsGenDf():
    istsGenDf = pd.read_excel(r'input_data\ists_gen.xlsx', skiprows=9, skipfooter=1)
    return istsGenDf

def fetchPrevIstsGenDf():
    istsGenDf = pd.read_excel(r'input_data\ists_gen_prev.xlsx', skiprows=9, skipfooter=1)
    return istsGenDf