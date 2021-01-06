'''
create Ists Generation Section data in the column sequence
name,installed_capacity,max_avc,day_max_actual,day_max_actual_time,day_min_actual,day_min_actual_time,sch_mu,act_mu,dev_mu,cuf
'''
import pandas as pd
from data_fetchers.inp_ts_data_store import getPntData
from data_fetchers.remc_data_store import getRemcPntData, FCA_FORECAST_VS_ACTUAL_STORE_NAME
from utils.excel_utils import append_df_to_excel
from utils.printUtils import printWithTs


def populateMaxGenInfoSectionData(configFilePath, configSheetName, outputFilePath, outputSheetName, truncateSheet=False):
    sectionDataDf = getMaxGenInfoSectionDataDf(configFilePath, configSheetName)
    # dump data to excel
    append_df_to_excel(outputFilePath, sectionDataDf, sheet_name=outputSheetName,
                       startrow=None, truncate_sheet=truncateSheet, index=False, header=False)


def getMaxGenInfoSectionDataDf(configFilePath, configSheetName):
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
        printWithTs('max gen info processing row number {0}'.format(rowIter+2))

        timeValSeries = getPntData('HRS')

        # get the type of row, itcan be dummy / normal / agg_pool / agg_gen_type
        rowType = confRow['type']
        if rowType == 'dummy':
            # since the row is dummy, just insert a None row into result
            resValsList.append({"name": confRow['name'],
                                "installed_capacity": None,
                                "max1": None, "max1_perc": None,
                                "max2": None, "max2_perc": None,
                                "max3": None, "max3_perc": None})
            continue
        elif not(pd.isnull(rowType)) and rowType.startswith('agg_'):
            aggColName = rowType[len('agg_'):]
            aggIdentifier = confRow[aggColName]
            confDfForAgg = normalPntsConfDf[normalPntsConfDf[aggColName]
                                            == aggIdentifier]
            actPnt = ','.join(confDfForAgg['act_id'].tolist())
        else:
            actPnt = confRow['act_id']

        installedCapacity = confRow['installed_capacity']
        max1 = getPntData(actPnt)[5*60:10*60].max()
        max1Perc = max1*100/installedCapacity

        max2 = getPntData(actPnt)[10*60:17*60].max()
        max2Perc = max2*100/installedCapacity

        max3 = getPntData(actPnt)[17*60:24*60].max()
        max3Perc = max3*100/installedCapacity

        resValsList.append({"name": confRow['name'],
                            "installed_capacity": installedCapacity,
                            "max1": max1, "max1_perc": max1Perc,
                            "max2": max2, "max2_perc": max2Perc,
                            "max3": max3, "max3_perc": max3Perc})
    return pd.DataFrame(resValsList)
