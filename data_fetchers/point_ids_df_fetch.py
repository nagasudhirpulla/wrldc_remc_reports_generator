import pandas as pd

def fetchPointIdsDf(configFilePath, pointsSheet):
    confDf = pd.read_excel(configFilePath, sheet_name=pointsSheet, index_col=0)
    confDf.index = confDf.index.str.strip()
    return confDf