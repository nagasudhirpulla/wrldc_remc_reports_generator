'''
create REMC State Error summary Section data in the column sequence
name,IFT,ALEASOFT,RES,ENERCAST,FCA
'''
import pandas as pd
from data_fetchers.remc_data_store import getRemcPntData, IFT_FORECAST_VS_ACTUAL_STORE_NAME, ALEA_FORECAST_VS_ACTUAL_STORE_NAME, RES_FORECAST_VS_ACTUAL_STORE_NAME, ENER_FORECAST_VS_ACTUAL_STORE_NAME, FCA_FORECAST_VS_ACTUAL_STORE_NAME
from data_fetchers.inp_ts_data_store import PointIdTypes, getEntityPointIds
from utils.remcFormulas import calcErrPercWithRespectToAvc
from utils.excel_utils import append_df_to_excel
from utils.printUtils import printWithTs
from utils.stringUtils import joinWith


def populateRemcStateErrNumBlksSectionData(configFilePath, configSheetName, outputFilePath, outputSheetName, truncateSheet=False):
    sectionDataDf = getRemcStateErrNumBlksSectionDataDf(
        configFilePath, configSheetName)
    # dump data to excel
    append_df_to_excel(outputFilePath, sectionDataDf, sheet_name=outputSheetName,
                       startrow=None, truncate_sheet=truncateSheet, index=False, header=False)


def getRemcStateErrNumBlksSectionDataDf(configFilePath, configSheetName):
    # get conf dataframe
    confDf = pd.read_excel(configFilePath, sheet_name=configSheetName)
    # confDf columns should be
    # name,r16_pnt,avc_pnt,actual_pnt,type,state
    for stripCol in 'name,type,state'.split(','):
        confDf[stripCol] = confDf[stripCol].str.strip()

    normalPntsConfDf = confDf[(confDf['type'] == 'normal') | (
        confDf['type'] == '') | (confDf['type'].isnull())]

    # initialize results
    resValsList = []

    for rowIter in range(confDf.shape[0]):
        confRow = confDf.iloc[rowIter]
        printWithTs(
            'REMC State error number of blocks report processing row number {0}'.format(rowIter+2))

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
            avcPnt = joinWith([getEntityPointIds(entName)[PointIdTypes.avc_point.value]
                              for entName in confDfForAgg['name'].dropna().tolist()])
            actPnt = joinWith([getEntityPointIds(entName)[PointIdTypes.actual_pnt_sch.value]
                              for entName in confDfForAgg['name'].tolist()])
            r16Pnt = joinWith([getEntityPointIds(entName)[PointIdTypes.r16_pnt.value]
                              for entName in confDfForAgg['name'].tolist()])
        else:
            entName = confRow['name']
            entityIds = getEntityPointIds(entName)
            avcPnt = entityIds[PointIdTypes.avc_point.value]
            actPnt = entityIds[PointIdTypes.actual_pnt_sch.value]
            r16Pnt = entityIds[PointIdTypes.r16_pnt.value]

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
