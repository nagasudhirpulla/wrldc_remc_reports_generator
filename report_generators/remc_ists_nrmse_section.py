'''
create REMC Ists NRMSE Section data in the column sequence
name,IFT,ALEASOFT,RES,ENERCAST,FCA
'''
import pandas as pd
from data_fetchers.remc_data_store import getRemcPntData, IFT_FORECAST_VS_ACTUAL_STORE_NAME, ALEA_FORECAST_VS_ACTUAL_STORE_NAME, RES_FORECAST_VS_ACTUAL_STORE_NAME, ENER_FORECAST_VS_ACTUAL_STORE_NAME, FCA_FORECAST_VS_ACTUAL_STORE_NAME
from data_fetchers.inp_ts_data_store import PointIdTypes, getEntityPointIds
from utils.remcFormulas import calcNrmsePerc
from utils.excel_utils import append_df_to_excel
from utils.printUtils import printWithTs
from utils.stringUtils import joinWith


def populateRemcIstsNrmseSectionData(configFilePath, configSheetName, outputFilePath, outputSheetName, truncateSheet=False):
    sectionDataDf = getRemcIstsNrmseSectionDataDf(
        configFilePath, configSheetName)
    # dump data to excel
    append_df_to_excel(outputFilePath, sectionDataDf, sheet_name=outputSheetName,
                       startrow=None, truncate_sheet=truncateSheet, index=False, header=False)


def getRemcIstsNrmseSectionDataDf(configFilePath, configSheetName):
    # get conf dataframe
    confDf = pd.read_excel(configFilePath, sheet_name=configSheetName)
    # confDf columns should be
    # name,r16_pnt,actual_pnt,type,pooling_station
    for stripCol in 'name,type,pooling_station'.split(','):
        confDf[stripCol] = confDf[stripCol].str.strip()

    normalPntsConfDf = confDf[(confDf['type'] == 'normal') | (
        confDf['type'] == '') | (confDf['type'].isnull())]

    # initialize results
    resValsList = []

    for rowIter in range(confDf.shape[0]):
        confRow = confDf.iloc[rowIter]
        printWithTs(
            'REMC ISTS RMSE report processing row number {0}'.format(rowIter+2))

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

        iftRmse = getRmse(
            IFT_FORECAST_VS_ACTUAL_STORE_NAME, r16Pnt, actPnt, avcPnt)
        resRmse = getRmse(
            RES_FORECAST_VS_ACTUAL_STORE_NAME, r16Pnt, actPnt, avcPnt)
        enerRmse = getRmse(
            ENER_FORECAST_VS_ACTUAL_STORE_NAME, r16Pnt, actPnt, avcPnt)
        fcaRmse = getRmse(
            FCA_FORECAST_VS_ACTUAL_STORE_NAME, r16Pnt, actPnt, avcPnt)

        resValsList.append({"name": confRow['name'], "ift": iftRmse,
                            "res": resRmse, "enercast": enerRmse,
                            "fca": fcaRmse})
    return pd.DataFrame(resValsList)


def getRmse(storename, forecastPnt, actPnt, avcPnt):
    forecastVals = getRemcPntData(
        storename, forecastPnt).tolist()
    actVals = getRemcPntData(
        storename, actPnt).tolist()
    avcVals = getRemcPntData(
        storename, avcPnt).tolist()
    rmsePerc = calcNrmsePerc(actVals, forecastVals, avcVals)
    return rmsePerc
