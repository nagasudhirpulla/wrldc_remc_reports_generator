'''
create REMC Regional R16 Error summary Section data in the column sequence
Solar, Wind, Combined (Solar+wind)
'''
import pandas as pd
from data_fetchers.remc_data_store import getRemcPntData, FCA_FORECAST_VS_ACTUAL_STORE_NAME
from utils.remcFormulas import calcNrmsePerc, calcMapePerc
from utils.excel_utils import append_df_to_excel
from utils.printUtils import printWithTs


def populateRemcRegionalR16ErrSectionData(configFilePath, configSheetName, outputFilePath, outputSheetName, truncateSheet=False):
    sectionDataDf = getRemcRegionalR16ErrSectionDataDf(
        configFilePath, configSheetName)
    # dump data to excel
    append_df_to_excel(outputFilePath, sectionDataDf, sheet_name=outputSheetName,
                       startrow=None, truncate_sheet=truncateSheet, index=False, header=False)


def getRemcRegionalR16ErrSectionDataDf(configFilePath, configSheetName):
    # get conf dataframe
    confDf = pd.read_excel(configFilePath, sheet_name=configSheetName)
    # confDf columns should be
    # name,r16_pnt,actual_pnt,cuf_pnt,avc_pnt,type
    for stripCol in 'name,r16_pnt,actual_pnt,avc_pnt,type'.split(','):
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
    regSolR16Vals = getRemcPntData(
        FCA_FORECAST_VS_ACTUAL_STORE_NAME, solarConf['r16_pnt'])
    regSolAvcVals = getRemcPntData(
        FCA_FORECAST_VS_ACTUAL_STORE_NAME, solarConf['avc_pnt'])

    regWindActVals = getRemcPntData(
        FCA_FORECAST_VS_ACTUAL_STORE_NAME, windConf['actual_pnt'])
    regWindR16Vals = getRemcPntData(
        FCA_FORECAST_VS_ACTUAL_STORE_NAME, windConf['r16_pnt'])
    regWindAvcVals = getRemcPntData(
        FCA_FORECAST_VS_ACTUAL_STORE_NAME, windConf['avc_pnt'])

    regCombActVals = getRemcPntData(
        FCA_FORECAST_VS_ACTUAL_STORE_NAME, combinedConf['actual_pnt'])
    regCombR16Vals = getRemcPntData(
        FCA_FORECAST_VS_ACTUAL_STORE_NAME, combinedConf['r16_pnt'])
    regCombAvcVals = getRemcPntData(
        FCA_FORECAST_VS_ACTUAL_STORE_NAME, combinedConf['avc_pnt'])

    # calculate the output rows
    # calculate regional solar mape for r16
    regSolR16MapePerc = calcMapePerc(regSolActVals, regSolR16Vals, regSolAvcVals)
    # calculate regional solar nrmse for r16
    regSolR16NrmsePerc = calcNrmsePerc(
        regSolActVals, regSolR16Vals, regSolAvcVals)
    # calculate regional wind mape for r16
    regWindR16MapePerc = calcMapePerc(
        regWindActVals, regWindR16Vals, regWindAvcVals)
    # calculate regional wind nrmse for r16
    regWindR16NrmsePerc = calcNrmsePerc(
        regWindActVals, regWindR16Vals, regWindAvcVals)
    # calculate regional combined mape for r16
    regCombR16MapePerc = calcMapePerc(
        regCombActVals, regCombR16Vals, regCombAvcVals)
    # calculate regional combined nrmse for r16
    regCombR16NrmsePerc = calcNrmsePerc(
        regCombActVals, regCombR16Vals, regCombAvcVals)

    printWithTs('Processing REMC Regional R16 Error summary Section at row {0}'.format(
        len(resValsList)+1))

    # create result dataframe rows
    resValsList.extend([
        {"name": "MAPE", "solar": regSolR16MapePerc,
            "wind": regWindR16MapePerc, "combined": regCombR16MapePerc},
        {"name": "NRMSE", "solar": regSolR16NrmsePerc,
            "wind": regWindR16NrmsePerc, "combined": regCombR16NrmsePerc}
    ])

    return pd.DataFrame(resValsList)
