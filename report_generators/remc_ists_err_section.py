'''
create REMC Ists Error summary Section data in the column sequence
name,r0_mape,r0_nrmse,r16_mape,r16_nrmse
'''
import pandas as pd
from data_fetchers.remc_data_store import getRemcPntData, FCA_FORECAST_VS_ACTUAL_STORE_NAME
from data_fetchers.inp_ts_data_store import PointIdTypes, getEntityPointIds
from utils.remcFormulas import calcNrmsePerc, calcMapePerc
from utils.excel_utils import append_df_to_excel
from utils.printUtils import printWithTs
from utils.stringUtils import joinWith

def populateRemcIstsErrSummSectionData(configFilePath, configSheetName, outputFilePath, outputSheetName, truncateSheet=False):
    sectionDataDf = getRemcIstsErrSummSectionDataDf(
        configFilePath, configSheetName)
    # dump data to excel
    append_df_to_excel(outputFilePath, sectionDataDf, sheet_name=outputSheetName,
                       startrow=None, truncate_sheet=truncateSheet, index=False, header=False)


def getRemcIstsErrSummSectionDataDf(configFilePath, configSheetName):
    # get conf dataframe
    confDf = pd.read_excel(configFilePath, sheet_name=configSheetName)
    # confDf columns should be
    # name,r0_pnt,r16_pnt,actual_pnt,cuf_pnt,avc_pnt,type,pooling_station
    for stripCol in 'name,type,pooling_station'.split(','):
        confDf[stripCol] = confDf[stripCol].str.strip()

    normalPntsConfDf = confDf[(confDf['type'] == 'normal') | (
        confDf['type'] == '') | (confDf['type'].isnull())]

    # initialize results
    resValsList = []

    for rowIter in range(confDf.shape[0]):
        confRow = confDf.iloc[rowIter]
        printWithTs(
            'REMC ISTS error summary processing row number {0}'.format(rowIter+2))

        # get the type of row, itcan be dummy / normal / agg_pool / agg_gen_type
        rowType = confRow['type']
        if rowType == 'dummy':
            # since the row is dummy, just insert a None row into result
            resValsList.append({"name": confRow['name'],
                                "r0_mape": None, "r0_nrmse": None,
                                "r16_mape": None, "r16_nrmse": None})
            continue
        elif not(pd.isnull(rowType)) and rowType.startswith('agg_'):
            aggColName = rowType[len('agg_'):]
            aggIdentifier = confRow[aggColName]
            confDfForAgg = normalPntsConfDf[normalPntsConfDf[aggColName]
                                            == aggIdentifier]
            avcPnt = joinWith([getEntityPointIds(entName)[PointIdTypes.avc_point.value]
                              for entName in confDfForAgg['name'].dropna().tolist()])
            actPnt = joinWith([getEntityPointIds(entName)[PointIdTypes.actual_pnt_sch.value]
                              for entName in confDfForAgg['name'].tolist()])
            r0Pnt = joinWith([getEntityPointIds(entName)[PointIdTypes.r0_pnt.value]
                              for entName in confDfForAgg['name'].tolist()])
            r16Pnt = joinWith([getEntityPointIds(entName)[PointIdTypes.r16_pnt.value]
                              for entName in confDfForAgg['name'].tolist()])
        else:
            entName = confRow['name']
            entityIds = getEntityPointIds(entName)
            avcPnt = entityIds[PointIdTypes.avc_point.value]
            actPnt = entityIds[PointIdTypes.actual_pnt_sch.value]
            r0Pnt = entityIds[PointIdTypes.r0_pnt.value]
            r16Pnt = entityIds[PointIdTypes.r16_pnt.value]

        avcVals = getRemcPntData(FCA_FORECAST_VS_ACTUAL_STORE_NAME, avcPnt).tolist()
        r0Vals = getRemcPntData(FCA_FORECAST_VS_ACTUAL_STORE_NAME, r0Pnt).tolist()
        r16Vals = getRemcPntData(FCA_FORECAST_VS_ACTUAL_STORE_NAME, r16Pnt).tolist()
        actVals = getRemcPntData(FCA_FORECAST_VS_ACTUAL_STORE_NAME, actPnt).tolist()

        r0MapePerc = calcMapePerc(actVals, r0Vals, avcVals)
        r0NrmsePerc = calcNrmsePerc(actVals, r0Vals, avcVals)
        r16MapePerc = calcMapePerc(actVals, r16Vals, avcVals)
        r16NrmsePerc = calcNrmsePerc(actVals, r16Vals, avcVals)

        resValsList.append({"name": confRow['name'],
                            "r0_mape": r0MapePerc, "r0_nrmse": r0NrmsePerc,
                            "r16_mape": r16MapePerc, "r16_nrmse": r16NrmsePerc})
    return pd.DataFrame(resValsList)
