from data_fetchers.ists_gen_df_fetch import fetchDummyIstsGenDf
from data_fetchers.tot_gen_df_fetch import fetchDummyTotGenDf
from data_fetchers.volt_df_fetch import fetchDummyVoltDf


def fetchDummyTsInpData():
    istsGenDf = fetchDummyIstsGenDf()
    totGenDf = fetchDummyTotGenDf()
    voltDf = fetchDummyVoltDf()
    inpTsDataDf = istsGenDf.merge(totGenDf, on='HRS').merge(voltDf, on='HRS')
    return inpTsDataDf