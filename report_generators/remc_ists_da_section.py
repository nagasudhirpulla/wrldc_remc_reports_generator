'''
create REMC Ists Day Ahead Forecast summary Section data in the column sequence
name,max,min,avg
'''
import pandas as pd
from data_fetchers.remc_data_store import getRemcPntData, FCA_DAY_AHEAD_STORE_NAME
from data_fetchers.inp_ts_data_store import PointIdTypes, getEntityPointIds
from utils.remcFormulas import calcNrmsePerc, calcMapePerc
from utils.excel_utils import append_df_to_excel
from utils.printUtils import printWithTs
from utils.stringUtils import joinWith


def populateRemcIstsDaSummSectionData(configFilePath, configSheetName, outputFilePath, outputSheetName, truncateSheet=False):
    sectionDataDf = getRemcIstsDaSummSectionDataDf(
        configFilePath, configSheetName)
    # dump data to excel
    append_df_to_excel(outputFilePath, sectionDataDf, sheet_name=outputSheetName,
                       startrow=None, truncate_sheet=truncateSheet, index=False, header=False)


def getRemcIstsDaSummSectionDataDf(configFilePath, configSheetName):
    # get conf dataframe
    confDf = pd.read_excel(configFilePath, sheet_name=configSheetName)
    # confDf columns should be
    # name,type,forecast_pnt
    for stripCol in 'name,type,pooling_station'.split(','):
        confDf[stripCol] = confDf[stripCol].str.strip()

    normalPntsConfDf = confDf[(confDf['type'] == 'normal') | (
        confDf['type'] == '') | (confDf['type'].isnull())]

    # initialize results
    resValsList = []

    for rowIter in range(confDf.shape[0]):
        confRow = confDf.iloc[rowIter]
        printWithTs(
            'REMC ISTS Day Ahead Forecast summary processing row number {0}'.format(rowIter+2))

        # get the type of row, itcan be dummy / normal / agg_pool / agg_gen_type
        rowType = confRow['type']
        if rowType == 'dummy':
            # since the row is dummy, just insert a None row into result
            resValsList.append({"name": confRow['name'],
                                "max": None, "min": None,
                                "avg": None})
            continue
        elif not(pd.isnull(rowType)) and rowType.startswith('agg_'):
            aggColName = rowType[len('agg_'):]
            aggIdentifier = confRow[aggColName]
            confDfForAgg = normalPntsConfDf[normalPntsConfDf[aggColName]
                                            == aggIdentifier]
            forecastPnt = joinWith([getEntityPointIds(entName)[PointIdTypes.forecast_point.value]
                              for entName in confDfForAgg['name'].tolist()])
        else:
            entName = confRow['name']
            entityIds = getEntityPointIds(entName)
            forecastPnt = entityIds[PointIdTypes.forecast_point.value]

        forecastSeries = getRemcPntData(FCA_DAY_AHEAD_STORE_NAME, forecastPnt)

        maxForecast = forecastSeries.max()
        minForecast = forecastSeries.min()
        avgForecast = forecastSeries.mean()

        resValsList.append({"name": confRow['name'],
                            "max": maxForecast, "min": minForecast,
                            "avg": avgForecast})
    return pd.DataFrame(resValsList)
