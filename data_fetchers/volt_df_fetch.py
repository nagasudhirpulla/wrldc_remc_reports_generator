import pandas as pd

def fetchDummyVoltDf():
    voltDf = pd.read_excel(r'dummy_data\202071_voltages.xlsx', skiprows=9)
    return voltDf