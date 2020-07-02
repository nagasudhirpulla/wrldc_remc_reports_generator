'''
create Regional Profile Section data in the column sequence
name, installed_capacity, max_avc, day_max_actual, day_max_actual_time, day_min_actual, day_min_actual_time, sch_mu, act_mu, dev_mu, cuf
'''
import pandas as pd
from data_fetchers.inp_ts_data_store import getPntData
from utils.excel_utils import saveDfToExcelSheet


def populateRegProfSectionData(configFilePath, configSheetName, outputFilePath, outputSheetName):
    sectionDataDf = getRegProfSectionDataDf(configFilePath, configSheetName)
    # dump data to excel
    saveDfToExcelSheet(outputFilePath, outputSheetName, sectionDataDf)


def getRegProfSectionDataDf(configFilePath, configSheetName):
    # get conf dataframe
    confDf = pd.read_excel(configFilePath, sheet_name=configSheetName)

    # initialize results
    resValsList = []

    # confDf columns should be
    # name, capacity, avc_point, actual_point, sch_point, type
    for rowIter in range(confDf.shape[0]):
        confRow = confDf.iloc[rowIter]
        timeValSeries = getPntData('HRS')

        maxAvc = getPntData(confRow['avc_point']).max()
        dayMaxActual = getPntData(confRow['actual_point']).max()
        dayMaxActualTime = timeValSeries.iloc[getPntData(
            confRow['actual_point']).idxmax()]

        dayMinActual = getPntData(confRow['actual_point']).min()
        dayMinActualTime = timeValSeries.iloc[getPntData(
            confRow['actual_point']).idxmin()]

        schMu = getPntData(confRow['sch_point']).mean()*0.024
        actMu = getPntData(confRow['actual_point']).mean()*0.024
        devMu = actMu - schMu

        resValsList.append({"name": confRow['name'],
                            "installed_capacity": confRow['capacity'],
                            "max_avc": maxAvc, "day_max_actual": dayMaxActual,
                            "day_max_actual_time": dayMaxActualTime, "day_min_actual": dayMinActual,
                            "day_min_actual_time": dayMinActualTime, "sch_mu": schMu,
                            "act_mu": actMu, "dev_mu": devMu, "cuf": 0})
    return pd.DataFrame(resValsList)
