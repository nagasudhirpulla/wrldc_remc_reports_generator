'''
create REMC Ists Error summary Section data in the column sequence
name,IFT,ALEASOFT,RES,ENERCAST,FCA
'''
import pandas as pd
from data_fetchers.remc_data_store import getRemcPntData, IFT_FORECAST_VS_ACTUAL_STORE_NAME, ALEA_FORECAST_VS_ACTUAL_STORE_NAME, RES_FORECAST_VS_ACTUAL_STORE_NAME, ENER_FORECAST_VS_ACTUAL_STORE_NAME, FCA_FORECAST_VS_ACTUAL_STORE_NAME
from utils.remcFormulas import calcErrPercWithRespectToAvc
from utils.excel_utils import append_df_to_excel
from utils.printUtils import printWithTs


def populateRemcIstsErrNumBlksSectionData(configFilePath, configSheetName, outputFilePath, outputSheetName, truncateSheet=False):
    sectionDataDf = getRemcIstsErrNumBlksSectionDataDf(
        configFilePath, configSheetName)
    # dump data to excel
    append_df_to_excel(outputFilePath, sectionDataDf, sheet_name=outputSheetName,
                       startrow=None, truncate_sheet=truncateSheet, index=False, header=False)


def getRemcIstsErrNumBlksSectionDataDf(configFilePath, configSheetName):
    # get conf dataframe
    confDf = pd.read_excel(configFilePath, sheet_name=configSheetName)
    # confDf columns should be
    # name,r16_pnt,avc_pnt,actual_pnt,type,pooling_station
    for stripCol in 'name,r16_pnt,avc_pnt,actual_pnt,type,pooling_station'.split(','):
        confDf[stripCol] = confDf[stripCol].str.strip()

    normalPntsConfDf = confDf[(confDf['type'] == 'normal') | (
        confDf['type'] == '') | (confDf['type'].isnull())]

    # initialize results
    resValsList = []

    for rowIter in range(confDf.shape[0]):
        confRow = confDf.iloc[rowIter]
        printWithTs(
            'REMC ISTS error number of blocks report processing row number {0}'.format(rowIter+2))

        # get the type of row, itcan be dummy / normal / agg_pool / agg_gen_type
        rowType = confRow['type']
        if rowType == 'dummy':
            # since the row is dummy, just insert a None row into result
            resValsList.append({"name": confRow['name'], "ift": None,
                                "res": None, "enercast": None, "fca": None})
            continue
        elif not (pd.isnull(rowType)) and rowType.startswith('agg_'):
            aggColName = rowType[len('agg_'):]
            aggIdentifier = confRow[aggColName]
            confDfForAgg = normalPntsConfDf[normalPntsConfDf[aggColName]
                                            == aggIdentifier]
            avcPnt = ','.join(confDfForAgg['avc_pnt'].tolist())
            actPnt = ','.join(confDfForAgg['actual_pnt'].tolist())
            r16Pnt = ','.join(confDfForAgg['r16_pnt'].tolist())
        else:
            avcPnt = confRow['avc_pnt']
            actPnt = confRow['actual_pnt']
            r16Pnt = confRow['r16_pnt']

        iftNumBlksLessThan15 = getNumBlksWithErrLessThan15(
            IFT_FORECAST_VS_ACTUAL_STORE_NAME, avcPnt, r16Pnt, actPnt)
        resNumBlksLessThan15 = getNumBlksWithErrLessThan15(
            RES_FORECAST_VS_ACTUAL_STORE_NAME, avcPnt, r16Pnt, actPnt)
        enerNumBlksLessThan15 = getNumBlksWithErrLessThan15(
            ENER_FORECAST_VS_ACTUAL_STORE_NAME, avcPnt, r16Pnt, actPnt)
        fcaNumBlksLessThan15 = getNumBlksWithErrLessThan15(
            FCA_FORECAST_VS_ACTUAL_STORE_NAME, avcPnt, r16Pnt, actPnt)

        resValsList.append({"name": confRow['name'], "ift": iftNumBlksLessThan15,
                            "res": resNumBlksLessThan15, "enercast": enerNumBlksLessThan15,
                            "fca": fcaNumBlksLessThan15})
    return pd.DataFrame(resValsList)


def getNumBlksWithErrLessThan15(storename, avcPnt, forecastPnt, actPnt):
    avcVals = getRemcPntData(
        storename, avcPnt).tolist()
    forecastVals = getRemcPntData(
        storename, forecastPnt).tolist()
    actVals = getRemcPntData(
        storename, actPnt).tolist()
    errPercVals = calcErrPercWithRespectToAvc(actVals, forecastVals, avcVals)
    numBlks15 = len([x for x in errPercVals if abs(x) <= 15])
    return numBlks15
