'''
create REMC State RMSE Section data in the column sequence
name,IFT,ALEASOFT,RES,ENERCAST,FCA
'''
import pandas as pd
from data_fetchers.remc_data_store import getRemcPntData, IFT_FORECAST_VS_ACTUAL_STORE_NAME, ALEA_FORECAST_VS_ACTUAL_STORE_NAME, RES_FORECAST_VS_ACTUAL_STORE_NAME, ENER_FORECAST_VS_ACTUAL_STORE_NAME, FCA_FORECAST_VS_ACTUAL_STORE_NAME
from utils.remcFormulas import calcRmsePerc
from utils.excel_utils import append_df_to_excel
from utils.printUtils import printWithTs


def populateRemcStateRmseSectionData(configFilePath, configSheetName, outputFilePath, outputSheetName, truncateSheet=False):
    sectionDataDf = getRemcStateRmseSectionDataDf(
        configFilePath, configSheetName)
    # dump data to excel
    append_df_to_excel(outputFilePath, sectionDataDf, sheet_name=outputSheetName,
                       startrow=None, truncate_sheet=truncateSheet, index=False, header=False)


def getRemcStateRmseSectionDataDf(configFilePath, configSheetName):
    # get conf dataframe
    confDf = pd.read_excel(configFilePath, sheet_name=configSheetName)
    # confDf columns should be
    # name,r16_pnt,actual_pnt,type,state
    for stripCol in 'name,r16_pnt,actual_pnt,type,state'.split(','):
        confDf[stripCol] = confDf[stripCol].str.strip()

    normalPntsConfDf = confDf[(confDf['type'] == 'normal') | (
        confDf['type'] == '') | (confDf['type'].isnull())]

    # initialize results
    resValsList = []

    for rowIter in range(confDf.shape[0]):
        confRow = confDf.iloc[rowIter]
        printWithTs(
            'REMC State RMSE report processing row number {0}'.format(rowIter+2))

        # get the type of row, itcan be dummy / normal / agg_pool / agg_gen_type
        rowType = confRow['type']
        if rowType == 'dummy':
            # since the row is dummy, just insert a None row into result
            resValsList.append({"name": confRow['name'], "ift": None,
                                "aleasoft": None, "res": None,
                                "enercast": None, "fca": None})
            continue
        elif not(pd.isnull(rowType)) and rowType.startswith('agg_'):
            aggColName = rowType[len('agg_'):]
            aggIdentifier = confRow[aggColName]
            confDfForAgg = normalPntsConfDf[normalPntsConfDf[aggColName]
                                            == aggIdentifier]
            actPnt = ','.join(confDfForAgg['actual_pnt'].tolist())
            r16Pnt = ','.join(confDfForAgg['r16_pnt'].tolist())
        else:
            actPnt = confRow['actual_pnt']
            r16Pnt = confRow['r16_pnt']

        iftRmse = getRmse(
            IFT_FORECAST_VS_ACTUAL_STORE_NAME, r16Pnt, actPnt)
        aleaRmse = getRmse(
            ALEA_FORECAST_VS_ACTUAL_STORE_NAME, r16Pnt, actPnt)
        resRmse = getRmse(
            RES_FORECAST_VS_ACTUAL_STORE_NAME, r16Pnt, actPnt)
        enerRmse = getRmse(
            ENER_FORECAST_VS_ACTUAL_STORE_NAME, r16Pnt, actPnt)
        fcaRmse = getRmse(
            FCA_FORECAST_VS_ACTUAL_STORE_NAME, r16Pnt, actPnt)
        
        resValsList.append({"name": confRow['name'], "ift": iftRmse,
                                "aleasoft": aleaRmse, "res": resRmse,
                                "enercast": enerRmse, "fca": fcaRmse})
    return pd.DataFrame(resValsList)


def getRmse(storename, forecastPnt, actPnt):
    forecastVals = getRemcPntData(
        storename, forecastPnt).tolist()
    actVals = getRemcPntData(
        storename, actPnt).tolist()
    rmsePerc = calcRmsePerc(actVals, forecastVals)
    return rmsePerc
