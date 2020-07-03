'''
create Voltage Profile Section data in the column sequence
name,400_max,400_min,400_avg,220_max,220_min,220_avg
'''
import pandas as pd
from data_fetchers.inp_ts_data_store import getPntData
from utils.excel_utils import saveDfToExcelSheet, append_df_to_excel


def populateVoltProfSectionData(configFilePath, configSheetName, outputFilePath, outputSheetName):
    sectionDataDf = getVoltProfSectionDataDf(configFilePath, configSheetName)
    # dump data to excel
    # saveDfToExcelSheet(outputFilePath, outputSheetName, sectionDataDf)
    append_df_to_excel(outputFilePath, sectionDataDf, sheet_name=outputSheetName, startrow=None, truncate_sheet=False, index=False, header=False)

def getVoltProfSectionDataDf(configFilePath, configSheetName):
    # get conf dataframe
    confDf = pd.read_excel(configFilePath, sheet_name=configSheetName)

    # initialize results
    resValsList = []

    # confDf columns should be
    # name,400_kv_pnt,220_kv_pnt,type
    for rowIter in range(confDf.shape[0]):
        confRow = confDf.iloc[rowIter]

        rowType = confRow['type']
        if rowType == 'dummy':
            resValsList.append({"name": confRow['name'],
                                "400_max": None, "400_min": None, "400_avg": None,
                                "220_max": None, "220_min": None, "220_avg": None})
            continue

        pnt400 = confRow['400_kv_pnt']
        max400 = None
        min400 = None
        avg400 = None

        pnt220 = confRow['220_kv_pnt']
        max220 = None
        min220 = None
        avg220 = None

        # handle none point id in this section config
        # get 400 kV values
        if not(pd.isnull(pnt400)):
            max400 = getPntData(pnt400).max()
            min400 = getPntData(pnt400).min()
            avg400 = getPntData(pnt400).mean()

        # handle none point id in this section config
        # get 220 kV values
        if not(pd.isnull(pnt220)):
            max220 = getPntData(pnt220).max()
            min220 = getPntData(pnt220).min()
            avg220 = getPntData(pnt220).mean()

        resValsList.append({"name": confRow['name'],
                            "400_max": max400, "400_min": min400, "400_avg": avg400,
                            "220_max": max220, "220_min": min220, "220_avg": avg220})
    return pd.DataFrame(resValsList)
