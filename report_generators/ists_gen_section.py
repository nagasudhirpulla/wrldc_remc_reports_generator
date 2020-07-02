'''
create Ists Generation Section data in the column sequence
name,installed_capacity,max_avc,day_max_actual,day_max_actual_time,day_min_actual,day_min_actual_time,sch_mu,act_mu,dev_mu,cuf
'''
import pandas as pd
from data_fetchers.inp_ts_data_store import getPntData
from utils.excel_utils import saveDfToExcelSheet


def populateIstsGenSectionData(configFilePath, configSheetName, outputFilePath, outputSheetName):
    sectionDataDf = getIstsGenSectionDataDf(configFilePath, configSheetName)
    # dump data to excel
    saveDfToExcelSheet(outputFilePath, outputSheetName, sectionDataDf)


def getIstsGenSectionDataDf(configFilePath, configSheetName):
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
                                "act_mu": None, "dev_mu": None, "CUF": None})
            continue
        elif rowType == 'agg_pool':
            poolStation = confRow['pooling_station']
            # get all normal points that have the same pooling station
            poolStationConfDf = normalPntsConfDf[normalPntsConfDf['pooling_station'] == poolStation]
            avcPnt = ','.join(poolStationConfDf['avc_id'].tolist())
            actPnt = ','.join(poolStationConfDf['act_id'].tolist())
            schPnt = ','.join(poolStationConfDf['sch_id'].tolist())
        elif rowType == 'agg_gen_type':
            genType = confRow['gen_type']
            # get all normal points that have the same pooling station
            genTypeConfDf = normalPntsConfDf[normalPntsConfDf['gen_type'] == genType]
            avcPnt = ','.join(genTypeConfDf['avc_id'].tolist())
            actPnt = ','.join(genTypeConfDf['act_id'].tolist())
            schPnt = ','.join(genTypeConfDf['sch_id'].tolist())
        else:
            avcPnt = confRow['avc_id']
            actPnt = confRow['act_id']
            schPnt = confRow['sch_id']

        maxAvc = getPntData(avcPnt).max()
        dayMaxActual = getPntData(actPnt).max()
        dayMaxActualTime = timeValSeries.iloc[getPntData(actPnt).idxmax()]

        dayMinActual = getPntData(actPnt).min()
        dayMinActualTime = timeValSeries.iloc[getPntData(actPnt).idxmin()]

        schMu = getPntData(schPnt).mean()*0.024
        actMu = getPntData(actPnt).mean()*0.024
        devMu = actMu - schMu

        resValsList.append({"name": confRow['name'],
                            "installed_capacity": confRow['installed_capacity'],
                            "max_avc": maxAvc, "day_max_actual": dayMaxActual,
                            "day_max_actual_time": dayMaxActualTime, "day_min_actual": dayMinActual,
                            "day_min_actual_time": dayMinActualTime, "sch_mu": schMu,
                            "act_mu": actMu, "dev_mu": devMu, "CUF": 0})
    return pd.DataFrame(resValsList)
