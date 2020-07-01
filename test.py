# %%
# initialize timeseries datastore with dummy data
from report_generators.reg_prof_report_generator import populateRegProfSectionData
from data_fetchers import inp_ts_data_store
inp_ts_data_store.initDummy()
x = inp_ts_data_store.tsDataDf

# %%
# config paths init
configFilePath = "remc_report_config.xlsx"
regSummConfigSheet = "section_1"
outputFilePath = "output/remc_report_output.xlsx"
regSummOutputSheet = "section_1"

# %%
# test regional profile report generation
populateRegProfSectionData(
    configFilePath, regSummConfigSheet, outputFilePath, regSummOutputSheet)


# %%
