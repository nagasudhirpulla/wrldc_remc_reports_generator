'''
create REMC Regional Day Ahead Forecast summary Section data in the column sequence
name,max,min,avg
'''
import pandas as pd
from data_fetchers.remc_data_store import getRemcPntData, FCA_DAY_AHEAD_STORE_NAME
from utils.remcFormulas import calcNrmsePerc, calcMapePerc
from utils.excel_utils import append_df_to_excel
from utils.printUtils import printWithTs


def populateRemcRegDaSummSectionData(configFilePath, configSheetName, outputFilePath, outputSheetName, truncateSheet=False):
    sectionDataDf = getRemcRegDaSummSectionDataDf(
        configFilePath, configSheetName)
    # dump data to excel
    append_df_to_excel(outputFilePath, sectionDataDf, sheet_name=outputSheetName,
                       startrow=None, truncate_sheet=truncateSheet, index=False, header=False)


def getRemcRegDaSummSectionDataDf(configFilePath, configSheetName):
    # get conf dataframe
    confDf = pd.read_excel(configFilePath, sheet_name=configSheetName)
    # confDf columns should be
    # name,type,forecast_pnt
    for stripCol in 'name,type,forecast_pnt'.split(','):
        confDf[stripCol] = confDf[stripCol].str.strip()

    # initialize results
    resValsList = []

    for rowIter in range(confDf.shape[0]):
        confRow = confDf.iloc[rowIter]
        printWithTs(
            'REMC Regional Day Ahead Forecast summary processing row number {0}'.format(rowIter+2))

        # get the type of row, itcan be dummy / normal / agg_pool / agg_gen_type
        rowType = confRow['type']
        if rowType == 'dummy':
            # since the row is dummy, just insert a None row into result
            resValsList.append({"name": confRow['name'],
                                "max": None, "min": None,
                                "avg": None})
            continue
        forecastPnt = confRow['forecast_pnt']

        forecastSeries = getRemcPntData(FCA_DAY_AHEAD_STORE_NAME, forecastPnt)

        maxForecast = forecastSeries.max()
        minForecast = forecastSeries.min()
        avgForecast = forecastSeries.mean()

        resValsList.append({"name": confRow['name'],
                            "max": maxForecast, "min": minForecast,
                            "avg": avgForecast})
    return pd.DataFrame(resValsList)
