'''
create Regional Profile Section data in the column sequence
name, installed_capacity, max_avc, day_max_actual, day_max_actual_time, day_min_actual, day_min_actual_time, sch_mu, act_mu, dev_mu, cuf
'''
import pandas as pd
from data_fetchers.inp_ts_data_store import getPntData, PointIdTypes, getEntityPointIds
from data_fetchers.remc_data_store import getRemcPntData, FCA_FORECAST_VS_ACTUAL_STORE_NAME
from utils.excel_utils import append_df_to_excel
from utils.printUtils import printWithTs


def populateRegProfSectionData(configFilePath, configSheetName, outputFilePath, outputSheetName, truncateSheet=False):
    sectionDataDf = getRegProfSectionDataDf(configFilePath, configSheetName)
    # dump data to excel
    append_df_to_excel(outputFilePath, sectionDataDf, sheet_name=outputSheetName,
                       startrow=0, truncate_sheet=truncateSheet, index=False, header=False)


def getRegProfSectionDataDf(configFilePath, configSheetName):
    # get conf dataframe
    confDf = pd.read_excel(configFilePath, sheet_name=configSheetName)

    # confDf columns should be
    # name, capacity, avc_point, actual_point, sch_point, type
    confDf['name'] = confDf['name'].str.strip()
    confDf['type'] = confDf['type'].str.strip()

    # initialize results
    resValsList = []

    for rowIter in range(confDf.shape[0]):
        printWithTs(
            'regional profile processing row number {0}'.format(rowIter+2))
        confRow = confDf.iloc[rowIter]

        # get the type of row, itcan be dummy / normal
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

        timeValSeries = getPntData('HRS')
        entName = confRow['name']
        entityIds = getEntityPointIds(entName)
        installedCapacity = entityIds[PointIdTypes.installed_capacity.value]
        actPnt =  entityIds[PointIdTypes.actual_point.value]
        avcPnt = entityIds[PointIdTypes.avc_point.value]
        if ((avcPnt == '') or pd.isnull(avcPnt)):
            maxAvc = None
        else:
            maxAvc = min(installedCapacity, getRemcPntData(
                FCA_FORECAST_VS_ACTUAL_STORE_NAME, avcPnt).max())

        dayMaxActual = getPntData(actPnt).max()
        dayMaxActualTime = timeValSeries.iloc[getPntData(actPnt).idxmax()]

        dayMinActual = getPntData(actPnt).min()
        dayMinActualTime = timeValSeries.iloc[getPntData(actPnt).idxmin()]

        schMu = getPntData(entityIds[PointIdTypes.sch_point.value]).mean()*0.024
        actMu = getPntData(actPnt).mean()*0.024
        devMu = actMu - schMu
        cufPerc = (actMu*100000)/(24*installedCapacity)

        resValsList.append({"name": entName,
                            "installed_capacity": installedCapacity,
                            "max_avc": maxAvc, "day_max_actual": dayMaxActual,
                            "day_max_actual_time": dayMaxActualTime, "day_min_actual": dayMinActual,
                            "day_min_actual_time": dayMinActualTime, "sch_mu": schMu,
                            "act_mu": actMu, "dev_mu": devMu, "cuf": cufPerc})
    return pd.DataFrame(resValsList)
