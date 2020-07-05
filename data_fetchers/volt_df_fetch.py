import pandas as pd

def fetchVoltDf():
    voltDf = pd.read_excel(r'input_data\voltages.xlsx', skiprows=9)
    return voltDf

def fetchPrevVoltDf():
    voltDf = pd.read_excel(r'input_data\voltages_prev.xlsx', skiprows=9)
    return voltDf