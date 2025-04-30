'''
create REMC Regional R16 Error summary Section data in the column sequence
Regional Solar, Regional Wind, Regional Combined (Solar+wind), ISTS Solar, ISTS Wind, ISTS Combined (Solar+wind)
'''
import pandas as pd
from data_fetchers.remc_data_store import getRemcPntData, FCA_FORECAST_VS_ACTUAL_STORE_NAME
from data_fetchers.inp_ts_data_store import PointIdTypes, getEntityPointIds
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
    for stripCol in 'name,type'.split(','):
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
    # solarConf = confDf[confDf['name'] == 'solar'].squeeze()
    # windConf = confDf[confDf['name'] == 'wind'].squeeze()
    # combinedConf = confDf[confDf['name'] == 'combined'].squeeze()

    # get data values
    regSolActVals = getRemcPntData(
        FCA_FORECAST_VS_ACTUAL_STORE_NAME, getEntityPointIds('SOLAR')[PointIdTypes.actual_pnt_sch.value])
    regSolR16Vals = getRemcPntData(
        FCA_FORECAST_VS_ACTUAL_STORE_NAME, getEntityPointIds('SOLAR')[PointIdTypes.r16_pnt.value])
    regSolAvcVals = getRemcPntData(
        FCA_FORECAST_VS_ACTUAL_STORE_NAME, getEntityPointIds('SOLAR')[PointIdTypes.avc_point.value])

    regWindActVals = getRemcPntData(
        FCA_FORECAST_VS_ACTUAL_STORE_NAME, getEntityPointIds('WIND')[PointIdTypes.actual_pnt_sch.value])
    regWindR16Vals = getRemcPntData(
        FCA_FORECAST_VS_ACTUAL_STORE_NAME, getEntityPointIds('WIND')[PointIdTypes.r16_pnt.value])
    regWindAvcVals = getRemcPntData(
        FCA_FORECAST_VS_ACTUAL_STORE_NAME, getEntityPointIds('WIND')[PointIdTypes.avc_point.value])

    regCombActVals = getRemcPntData(
        FCA_FORECAST_VS_ACTUAL_STORE_NAME, getEntityPointIds('Total Wind & Solar')[PointIdTypes.actual_pnt_sch.value])
    regCombR16Vals = getRemcPntData(
        FCA_FORECAST_VS_ACTUAL_STORE_NAME, getEntityPointIds('Total Wind & Solar')[PointIdTypes.r16_pnt.value])
    regCombAvcVals = getRemcPntData(
        FCA_FORECAST_VS_ACTUAL_STORE_NAME, getEntityPointIds('Total Wind & Solar')[PointIdTypes.avc_point.value])

    # get ISTS rows
    # solarConf = confDf[confDf['name'] == 'Total ISTS Solar'].squeeze()
    # windConf = confDf[confDf['name'] == 'Total ISTS Wind'].squeeze()
    # combinedConf = confDf[confDf['name'] == 'Total ISTS RE'].squeeze()

    # get data values
    istsSolActVals = getRemcPntData(
        FCA_FORECAST_VS_ACTUAL_STORE_NAME, getEntityPointIds('Total ISTS Solar')[PointIdTypes.actual_pnt_sch.value])
    istsSolR16Vals = getRemcPntData(
        FCA_FORECAST_VS_ACTUAL_STORE_NAME, getEntityPointIds('Total ISTS Solar')[PointIdTypes.r16_pnt.value])
    istsSolAvcVals = getRemcPntData(
        FCA_FORECAST_VS_ACTUAL_STORE_NAME, getEntityPointIds('Total ISTS Solar')[PointIdTypes.avc_point.value])

    istsWindActVals = getRemcPntData(
        FCA_FORECAST_VS_ACTUAL_STORE_NAME, getEntityPointIds('Total ISTS Wind')[PointIdTypes.actual_pnt_sch.value])
    istsWindR16Vals = getRemcPntData(
        FCA_FORECAST_VS_ACTUAL_STORE_NAME, getEntityPointIds('Total ISTS Wind')[PointIdTypes.r16_pnt.value])
    istsWindAvcVals = getRemcPntData(
        FCA_FORECAST_VS_ACTUAL_STORE_NAME, getEntityPointIds('Total ISTS Wind')[PointIdTypes.avc_point.value])

    istsCombActVals = getRemcPntData(
        FCA_FORECAST_VS_ACTUAL_STORE_NAME, getEntityPointIds('Total ISTS RE')[PointIdTypes.actual_pnt_sch.value])
    istsCombR16Vals = getRemcPntData(
        FCA_FORECAST_VS_ACTUAL_STORE_NAME, getEntityPointIds('Total ISTS RE')[PointIdTypes.r16_pnt.value])
    istsCombAvcVals = getRemcPntData(
        FCA_FORECAST_VS_ACTUAL_STORE_NAME, getEntityPointIds('Total ISTS RE')[PointIdTypes.avc_point.value])

    # calculate the output rows for region
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

    # calculate the output rows for ists
    # calculate ists solar mape for r16
    istsSolR16MapePerc = calcMapePerc(
        istsSolActVals, istsSolR16Vals, istsSolAvcVals)
    # calculate ists solar nrmse for r16
    istsSolR16NrmsePerc = calcNrmsePerc(
        istsSolActVals, istsSolR16Vals, istsSolAvcVals)
    # calculate ists wind mape for r16
    istsWindR16MapePerc = calcMapePerc(
        istsWindActVals, istsWindR16Vals, istsWindAvcVals)
    # calculate ists wind nrmse for r16
    istsWindR16NrmsePerc = calcNrmsePerc(
        istsWindActVals, istsWindR16Vals, istsWindAvcVals)
    # calculate ists combined mape for r16
    istsCombR16MapePerc = calcMapePerc(
        istsCombActVals, istsCombR16Vals, istsCombAvcVals)
    # calculate ists combined nrmse for r16
    istsCombR16NrmsePerc = calcNrmsePerc(
        istsCombActVals, istsCombR16Vals, istsCombAvcVals)

    printWithTs('Processing REMC Regional R16 Error summary Section at row {0}'.format(
        len(resValsList)+1))

    # create result dataframe rows
    resValsList.extend([
        {"name": "MAPE",
         "solar": regSolR16MapePerc, "wind": regWindR16MapePerc, "combined": regCombR16MapePerc,
         "istsSolar": istsSolR16MapePerc, "istsWind": istsWindR16MapePerc, "istsCombined": istsCombR16MapePerc
         },
        {"name": "NRMSE",
         "solar": regSolR16NrmsePerc, "wind": regWindR16NrmsePerc, "combined": regCombR16NrmsePerc,
         "istsSolar": istsSolR16NrmsePerc, "istsWind": istsWindR16NrmsePerc, "istsCombined": istsCombR16NrmsePerc
         }
    ])

    return pd.DataFrame(resValsList)
