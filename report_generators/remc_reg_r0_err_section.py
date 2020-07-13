'''
create REMC Regional R0 Error summary Section data in the column sequence
Solar, Wind, Combined (Solar+wind)
'''
import pandas as pd
from data_fetchers.remc_data_store import getRemcPntData, FCA_FORECAST_VS_ACTUAL_STORE_NAME
from utils.remcFormulas import calcNrmsePerc, calcMapePerc
from utils.excel_utils import append_df_to_excel
from utils.printUtils import printWithTs


def populateRemcRegionalR0ErrSectionData(configFilePath, configSheetName, outputFilePath, outputSheetName, truncateSheet=False):
    sectionDataDf = getRemcRegionalR0ErrSectionDataDf(
        configFilePath, configSheetName)
    # dump data to excel
    append_df_to_excel(outputFilePath, sectionDataDf, sheet_name=outputSheetName,
                       startrow=None, truncate_sheet=truncateSheet, index=False, header=False)


def getRemcRegionalR0ErrSectionDataDf(configFilePath, configSheetName):
    # get conf dataframe
    confDf = pd.read_excel(configFilePath, sheet_name=configSheetName)
    # confDf columns should be
    # name,r0_pnt,actual_pnt,cuf_pnt,avc_pnt,type
    for stripCol in 'name,r0_pnt,actual_pnt,avc_pnt,type'.split(','):
        confDf[stripCol] = confDf[stripCol].str.strip()

    # initialize results
    resValsList = []

    # find the row index of first non dummy row
    for rowIter in range(len(confDf)):
        confRow = confDf.iloc[rowIter]
        rowType = confRow['type']
        if rowType == 'dummy':
            resValsList.append({"name": confRow['name'],
                                "solar": None, "wind": None,
                                "combined": None})

    # get regional solar row
    solarConf = confDf[confDf['name'] == 'solar'].squeeze()
    windConf = confDf[confDf['name'] == 'wind'].squeeze()
    combinedConf = confDf[confDf['name'] == 'combined'].squeeze()

    # get data values
    regSolActVals = getRemcPntData(
        FCA_FORECAST_VS_ACTUAL_STORE_NAME, solarConf['actual_pnt'])
    regSolR0Vals = getRemcPntData(
        FCA_FORECAST_VS_ACTUAL_STORE_NAME, solarConf['r0_pnt'])
    regSolAvcVals = getRemcPntData(
        FCA_FORECAST_VS_ACTUAL_STORE_NAME, solarConf['avc_pnt'])

    regWindActVals = getRemcPntData(
        FCA_FORECAST_VS_ACTUAL_STORE_NAME, windConf['actual_pnt'])
    regWindR0Vals = getRemcPntData(
        FCA_FORECAST_VS_ACTUAL_STORE_NAME, windConf['r0_pnt'])
    regWindAvcVals = getRemcPntData(
        FCA_FORECAST_VS_ACTUAL_STORE_NAME, windConf['avc_pnt'])

    regCombActVals = getRemcPntData(
        FCA_FORECAST_VS_ACTUAL_STORE_NAME, combinedConf['actual_pnt'])
    regCombR0Vals = getRemcPntData(
        FCA_FORECAST_VS_ACTUAL_STORE_NAME, combinedConf['r0_pnt'])
    regCombAvcVals = getRemcPntData(
        FCA_FORECAST_VS_ACTUAL_STORE_NAME, combinedConf['avc_pnt'])

    # calculate the output rows
    # calculate regional solar mape for r0
    regSolR0MapePerc = calcMapePerc(regSolActVals, regSolR0Vals, regSolAvcVals)
    # calculate regional solar nrmse for r0
    regSolR0NrmsePerc = calcNrmsePerc(
        regSolActVals, regSolR0Vals, regSolAvcVals)
    # calculate regional wind mape for r0
    regWindR0MapePerc = calcMapePerc(
        regWindActVals, regWindR0Vals, regWindAvcVals)
    # calculate regional wind nrmse for r0
    regWindR0NrmsePerc = calcNrmsePerc(
        regWindActVals, regWindR0Vals, regWindAvcVals)
    # calculate regional combined mape for r0
    regCombR0MapePerc = calcMapePerc(
        regCombActVals, regCombR0Vals, regCombAvcVals)
    # calculate regional combined nrmse for r0
    regCombR0NrmsePerc = calcNrmsePerc(
        regCombActVals, regCombR0Vals, regCombAvcVals)

    printWithTs('Processing REMC Regional R0 Error summary Section at row {0}'.format(
        len(resValsList)+1))

    # create result dataframe rows
    resValsList.extend([
        {"name": "MAPE", "solar": regSolR0MapePerc,
            "wind": regWindR0MapePerc, "combined": regCombR0MapePerc},
        {"name": "NRMSE", "solar": regSolR0NrmsePerc,
            "wind": regWindR0NrmsePerc, "combined": regCombR0NrmsePerc}
    ])

    return pd.DataFrame(resValsList)
