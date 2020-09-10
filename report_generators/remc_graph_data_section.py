'''
create REMC Graph Data Section data in the column sequence
name1,name2,name3,...
'''
import pandas as pd
from data_fetchers.remc_data_store import getRemcPntData
from utils.excel_utils import append_df_to_excel
from utils.printUtils import printWithTs


def populateRemcGraphDataSectionData(configFilePath, configSheetName, outputFilePath, outputSheetName):
    sectionDataDf = getRemcGraphDataSectionDataDf(
        configFilePath, configSheetName)
    # dump data to excel
    append_df_to_excel(outputFilePath, sectionDataDf, sheet_name=outputSheetName,
                       startrow=0, truncate_sheet=True, index=False)


def getRemcGraphDataSectionDataDf(configFilePath, configSheetName):
    # get conf dataframe
    confDf = pd.read_excel(configFilePath, sheet_name=configSheetName)
    for stripCol in 'name,pnt,store'.split(','):
        confDf[stripCol] = confDf[stripCol].str.strip()

    # initialize results
    resValsObj = {}

    # confDf columns should be
    # name, pnt, store
    for rowIter in range(confDf.shape[0]):
        confRow = confDf.iloc[rowIter]
        printWithTs('graph data processing row number {0}'.format(rowIter+2))

        name = confRow['name']
        pnt = confRow['pnt']
        store = confRow['store']

        pntData = getRemcPntData(store, pnt)

        # replace with zeros if we do not have data in the store
        if pntData.size == 0:
            pntData = pd.Series([0 for x in range(96)])

        resValsObj[name] = pntData.values

    return pd.DataFrame(resValsObj)
