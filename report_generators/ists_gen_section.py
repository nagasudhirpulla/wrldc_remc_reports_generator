'''
create Ists Generation Section data in the column sequence
name,installed_capacity,max_avc,day_max_actual,day_max_actual_time,day_min_actual,day_min_actual_time,sch_mu,act_mu,dev_mu,cuf
'''
import pandas as pd
import datetime as dt
from data_fetchers.inp_ts_data_store import getPntData, PointIdTypes, getEntityPointIds
from data_fetchers.remc_data_store import getRemcPntData, FCA_FORECAST_VS_ACTUAL_STORE_NAME
from utils.excel_utils import append_df_to_excel
from utils.printUtils import printWithTs
from utils.stringUtils import joinWith
from data_fetchers.wbes_data_store import WbesSchTypeEnum, getWbesAcrSch


def populateIstsGenSectionData(configFilePath, configSheetName, outputFilePath, outputSheetName, reqDt: dt.datetime, truncateSheet=False):
    sectionDataDf = getIstsGenSectionDataDf(
        configFilePath, configSheetName, reqDt)
    # dump data to excel
    append_df_to_excel(outputFilePath, sectionDataDf, sheet_name=outputSheetName,
                       startrow=None, truncate_sheet=truncateSheet, index=False, header=False)


def getIstsGenSectionDataDf(configFilePath, configSheetName, reqDt: dt.datetime):
    # get conf dataframe
    confDf = pd.read_excel(configFilePath, sheet_name=configSheetName)
    # confDf columns should be
    # name,installed_capacity,avc_id,act_id,sch_id,type,pooling_station,gen_type
    confDf['name'] = confDf['name'].str.strip()
    confDf['type'] = confDf['type'].str.strip()
    confDf['pooling_station'] = confDf['pooling_station'].str.strip()
    confDf['gen_type'] = confDf['gen_type'].str.strip()
    normalPntsConfDf = confDf[(confDf['type'] == 'normal') | (
        confDf['type'] == '') | (confDf['type'].isnull())]

    # initialize results
    resValsList = []

    for rowIter in range(confDf.shape[0]):
        confRow = confDf.iloc[rowIter]
        printWithTs('ists gen processing row number {0}'.format(rowIter+2))

        timeValSeries = getPntData('HRS')

        # get the type of row, itcan be dummy / normal / agg_pool / agg_gen_type
        rowType = confRow['type']
        if rowType == 'dummy':
            # since the row is dummy, just insert a None row into result
            resValsList.append({"name": confRow['name'],
                                "installed_capacity": None,
                                "max_avc": None, "day_max_actual": None,
                                "day_max_actual_time": None, "day_min_actual": None,
                                "day_min_actual_time": None, "sch_mu": None,
                                "act_mu": None, "dev_mu": None, "cuf": None})
            continue
        elif not (pd.isnull(rowType)) and rowType.startswith('agg_'):
            aggColName = rowType[len('agg_'):]
            aggIdentifier = confRow[aggColName]
            confDfForAgg = normalPntsConfDf[normalPntsConfDf[aggColName]
                                            == aggIdentifier]
            avcPnt = joinWith([getEntityPointIds(entName)[PointIdTypes.avc_point.value]
                              for entName in confDfForAgg['name'].dropna().tolist()])
            actPnt = joinWith([getEntityPointIds(entName)[PointIdTypes.actual_point.value]
                              for entName in confDfForAgg['name'].tolist()])
            # schPnt = joinWith([getEntityPointIds(entName)[PointIdTypes.sch_point.value]
            #                   for entName in confDfForAgg['name'].tolist()])
            wbesAcr = joinWith([getEntityPointIds(entName)[PointIdTypes.wbes_acr.value]
                                for entName in confDfForAgg['name'].tolist()])
            installedCapacity = sum([getEntityPointIds(entName)[PointIdTypes.installed_capacity.value]
                                     for entName in confDfForAgg['name'].tolist()])
        else:
            entName = confRow['name']
            entityIds = getEntityPointIds(entName)
            actPnt = entityIds[PointIdTypes.actual_point.value]
            avcPnt = entityIds[PointIdTypes.avc_point.value]
            # schPnt = entityIds[PointIdTypes.sch_point.value]
            wbesAcr = entityIds[PointIdTypes.wbes_acr.value]
            installedCapacity = entityIds[PointIdTypes.installed_capacity.value]

        if ((avcPnt == '') or pd.isnull(avcPnt)):
            maxAvc = None
        else:
            # maxAvc = getRemcPntData(
            #     FCA_FORECAST_VS_ACTUAL_STORE_NAME, avcPnt).max()
            avcVals = pd.Series()
            for avcPntId in avcPnt.split(","):
                if (avcPntId.startswith("WREMC")):
                    pntAvcVals = getPntData(avcPntId)
                else:
                    pntAvcVals = getRemcPntData(
                        FCA_FORECAST_VS_ACTUAL_STORE_NAME, avcPntId)
                avcVals = avcVals.add(pntAvcVals, fill_value=0)
            maxAvc = min(installedCapacity, avcVals.max())

        dayMaxActual = getPntData(actPnt).max()
        dayMaxActualTime = timeValSeries.iloc[getPntData(actPnt).idxmax()]

        dayMinActual = getPntData(actPnt).min()
        dayMinActualTime = timeValSeries.iloc[getPntData(actPnt).idxmin()]

        # schMu = getPntData(schPnt).mean()*0.024
        schMu = getWbesAcrSch(wbesAcr, schType=WbesSchTypeEnum.NET_MU)
        actMu = getPntData(actPnt).mean()*0.024
        devMu = actMu - schMu
        # installedCapacity = confRow['installed_capacity']
        cufPerc = (actMu*100000)/(24*installedCapacity)

        resValsList.append({"name": confRow['name'],
                            "installed_capacity": installedCapacity,
                            "max_avc": maxAvc, "day_max_actual": dayMaxActual,
                            "day_max_actual_time": dayMaxActualTime, "day_min_actual": dayMinActual,
                            "day_min_actual_time": dayMinActualTime, "sch_mu": schMu,
                            "act_mu": actMu, "dev_mu": devMu, "cuf": cufPerc})
    return pd.DataFrame(resValsList)
