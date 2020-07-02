from data_fetchers.ists_gen_df_fetch import fetchDummyIstsGenDf, fetchDummyPrevIstsGenDf
from data_fetchers.tot_gen_df_fetch import fetchDummyTotGenDf, fetchDummyPrevTotGenDf
from data_fetchers.volt_df_fetch import fetchDummyVoltDf, fetchDummyPrevVoltDf


def fetchDummyTsInpData():
    istsGenDf = fetchDummyIstsGenDf()
    totGenDf = fetchDummyTotGenDf()
    voltDf = fetchDummyVoltDf()
    inpTsDataDf = istsGenDf.merge(totGenDf, on='HRS').merge(voltDf, on='HRS')
    return inpTsDataDf


def fetchPrevDummyTsInpData():
    istsGenDf = fetchDummyPrevIstsGenDf()
    totGenDf = fetchDummyPrevTotGenDf()
    voltDf = fetchDummyPrevVoltDf()
    inpTsDataDf = istsGenDf.merge(totGenDf, on='HRS').merge(voltDf, on='HRS')
    return inpTsDataDf
