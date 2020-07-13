'''
create REMC Regional R0 Error summary Section data in the column sequence
Regional Solar, Regional Wind, Regional Combined (Solar+wind), ISTS Solar, ISTS Wind, ISTS Combined (Solar+wind)
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

    # get regional rows
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

    # get ISTS rows
    solarConf = confDf[confDf['name'] == 'ists_solar'].squeeze()
    windConf = confDf[confDf['name'] == 'ists_wind'].squeeze()
    combinedConf = confDf[confDf['name'] == 'ists_combined'].squeeze()

    # get data values
    istsSolActVals = getRemcPntData(
        FCA_FORECAST_VS_ACTUAL_STORE_NAME, solarConf['actual_pnt'])
    istsSolR0Vals = getRemcPntData(
        FCA_FORECAST_VS_ACTUAL_STORE_NAME, solarConf['r0_pnt'])
    istsSolAvcVals = getRemcPntData(
        FCA_FORECAST_VS_ACTUAL_STORE_NAME, solarConf['avc_pnt'])

    istsWindActVals = getRemcPntData(
        FCA_FORECAST_VS_ACTUAL_STORE_NAME, windConf['actual_pnt'])
    istsWindR0Vals = getRemcPntData(
        FCA_FORECAST_VS_ACTUAL_STORE_NAME, windConf['r0_pnt'])
    istsWindAvcVals = getRemcPntData(
        FCA_FORECAST_VS_ACTUAL_STORE_NAME, windConf['avc_pnt'])

    istsCombActVals = getRemcPntData(
        FCA_FORECAST_VS_ACTUAL_STORE_NAME, combinedConf['actual_pnt'])
    istsCombR0Vals = getRemcPntData(
        FCA_FORECAST_VS_ACTUAL_STORE_NAME, combinedConf['r0_pnt'])
    istsCombAvcVals = getRemcPntData(
        FCA_FORECAST_VS_ACTUAL_STORE_NAME, combinedConf['avc_pnt'])

    # calculate the output rows for region
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

    # calculate the output rows for ists
    # calculate ists solar mape for r0
    istsSolR0MapePerc = calcMapePerc(
        istsSolActVals, istsSolR0Vals, istsSolAvcVals)
    # calculate ists solar nrmse for r0
    istsSolR0NrmsePerc = calcNrmsePerc(
        istsSolActVals, istsSolR0Vals, istsSolAvcVals)
    # calculate ists wind mape for r0
    istsWindR0MapePerc = calcMapePerc(
        istsWindActVals, istsWindR0Vals, istsWindAvcVals)
    # calculate ists wind nrmse for r0
    istsWindR0NrmsePerc = calcNrmsePerc(
        istsWindActVals, istsWindR0Vals, istsWindAvcVals)
    # calculate ists combined mape for r0
    istsCombR0MapePerc = calcMapePerc(
        istsCombActVals, istsCombR0Vals, istsCombAvcVals)
    # calculate ists combined nrmse for r0
    istsCombR0NrmsePerc = calcNrmsePerc(
        istsCombActVals, istsCombR0Vals, istsCombAvcVals)

    printWithTs('Processing REMC Regional R0 Error summary Section at row {0}'.format(
        len(resValsList)+1))

    # create result dataframe rows
    resValsList.extend([
        {"name": "MAPE",
         "solar": regSolR0MapePerc, "wind": regWindR0MapePerc, "combined": regCombR0MapePerc,
         "istsSolar": istsSolR0MapePerc, "istsWind": istsWindR0MapePerc, "istsCombined": istsCombR0MapePerc
         },
        {"name": "NRMSE",
         "solar": regSolR0NrmsePerc, "wind": regWindR0NrmsePerc, "combined": regCombR0NrmsePerc,
         "istsSolar": istsSolR0NrmsePerc, "istsWind": istsWindR0NrmsePerc, "istsCombined": istsCombR0NrmsePerc
         }
    ])

    return pd.DataFrame(resValsList)
