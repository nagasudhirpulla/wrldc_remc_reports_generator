from data_fetchers.ists_gen_df_fetch import fetchIstsGenDf, fetchPrevIstsGenDf
from data_fetchers.tot_gen_df_fetch import fetchTotGenDf, fetchPrevTotGenDf
from data_fetchers.volt_df_fetch import fetchVoltDf, fetchPrevVoltDf


def fetchTsInpData():
    istsGenDf = fetchIstsGenDf()
    totGenDf = fetchTotGenDf()
    voltDf = fetchVoltDf()
    inpTsDataDf = istsGenDf.merge(totGenDf, on='HRS').merge(voltDf, on='HRS')
    return inpTsDataDf


def fetchPrevTsInpData():
    istsGenDf = fetchPrevIstsGenDf()
    totGenDf = fetchPrevTotGenDf()
    voltDf = fetchPrevVoltDf()
    inpTsDataDf = istsGenDf.merge(totGenDf, on='HRS').merge(voltDf, on='HRS')
    return inpTsDataDf
