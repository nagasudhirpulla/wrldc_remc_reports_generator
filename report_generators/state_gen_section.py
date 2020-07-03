'''
create Ists Generation Section data in the column sequence
name,installed_capacity,max_avc,day_max_actual,day_max_actual_time,day_min_actual,day_min_actual_time,sch_mu,act_mu,dev_mu,cuf
'''
import pandas as pd
from data_fetchers.inp_ts_data_store import getPntData
from utils.excel_utils import saveDfToExcelSheet, append_df_to_excel


def populateStateGenSectionData(configFilePath, configSheetName, outputFilePath, outputSheetName):
    sectionDataDf = getStateGenSectionDataDf(configFilePath, configSheetName)
    # dump data to excel
    # saveDfToExcelSheet(outputFilePath, outputSheetName, sectionDataDf)
    append_df_to_excel(outputFilePath, sectionDataDf, sheet_name=outputSheetName, startrow=None, truncate_sheet=False, index=False, header=False)

def getStateGenSectionDataDf(configFilePath, configSheetName):
    # get conf dataframe
    confDf = pd.read_excel(configFilePath, sheet_name=configSheetName)
    # confDf columns should be
    # name,installed_capacity,avc_id,act_id,sch_id,type,state
    confDf['name'] = confDf['name'].str.strip()
    confDf['type'] = confDf['type'].str.strip()
    confDf['state'] = confDf['state'].str.strip()
    normalPntsConfDf = confDf[(confDf['type'] == 'normal') | (
        confDf['type'] == '') | (confDf['type'].isnull())]

    # initialize results
    resValsList = []

    for rowIter in range(confDf.shape[0]):
        confRow = confDf.iloc[rowIter]
        timeValSeries = getPntData('HRS')

        # get the type of row, itcan be dummy / normal / agg_state
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
        elif rowType == 'agg_state':
            state = confRow['state']
            # get all normal points that have the same state
            stateConfDf = normalPntsConfDf[normalPntsConfDf['state'] == state]
            avcPnt = ','.join(stateConfDf['avc_id'].tolist())
            actPnt = ','.join(stateConfDf['act_id'].tolist())
            schPnt = ','.join(stateConfDf['sch_id'].tolist())
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
        installedCapacity = confRow['installed_capacity']
        cufPerc = (actMu*2.4)/installedCapacity

        resValsList.append({"name": confRow['name'],
                            "installed_capacity": installedCapacity,
                            "max_avc": maxAvc, "day_max_actual": dayMaxActual,
                            "day_max_actual_time": dayMaxActualTime, "day_min_actual": dayMinActual,
                            "day_min_actual_time": dayMinActualTime, "sch_mu": schMu,
                            "act_mu": actMu, "dev_mu": devMu, "cuf": cufPerc})
    return pd.DataFrame(resValsList)
