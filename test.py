# %%
# imports
# initialize timeseries datastore with dummy data
from report_generators.reg_prof_report_generator import populateRegProfSectionData
from report_generators.ists_gen_section import populateIstsGenSectionData
from data_fetchers import inp_ts_data_store
# %%
# initialize timeseries datastore with dummy data
inp_ts_data_store.initDummy()
x = inp_ts_data_store.tsDataDf

# %%
# config paths init
configFilePath = "remc_report_config.xlsx"
outputFilePath = "output/remc_report_output.xlsx"
regSummConfigSheet = "section_1"
regSummOutputSheet = "section_1"
istsGenConfigSheet = "section_2"
istsGenOutputSheet = "section_2"

# %%
# test regional profile report generation
populateRegProfSectionData(
    configFilePath, regSummConfigSheet, outputFilePath, regSummOutputSheet)


# %%
# test ists generation report generation
populateIstsGenSectionData(
    configFilePath, istsGenConfigSheet, outputFilePath, istsGenOutputSheet)