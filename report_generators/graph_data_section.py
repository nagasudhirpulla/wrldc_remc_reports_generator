'''
create Graph Data Section data in the column sequence
name1,name2,name3,...
'''
import pandas as pd
from data_fetchers.inp_ts_data_store import getPntData
from utils.excel_utils import append_df_to_excel
from utils.printUtils import printWithTs


def populateGraphDataSectionData(configFilePath, configSheetName, outputFilePath, outputSheetName):
    sectionDataDf = getGraphDataSectionDataDf(configFilePath, configSheetName)
    # dump data to excel
    append_df_to_excel(outputFilePath, sectionDataDf, sheet_name=outputSheetName,
                       startrow=0, truncate_sheet=True, index=False)


def getGraphDataSectionDataDf(configFilePath, configSheetName):
    # get conf dataframe
    confDf = pd.read_excel(configFilePath, sheet_name=configSheetName)

    # initialize results
    resValsObj = {}

    # confDf columns should be
    # name, pnt, day_offset
    for rowIter in range(confDf.shape[0]):
        confRow = confDf.iloc[rowIter]
        printWithTs('graph data processing row number {0}'.format(rowIter+2))

        name = confRow['name']
        pnt = confRow['pnt']
        dayOffset = confRow['day_offset']
        isPrev = False
        if dayOffset == -2:
            isPrev = True

        pntData = getPntData(pnt, isPrev=isPrev)
        resValsObj[name] = pntData.values

    return pd.DataFrame(resValsObj)
