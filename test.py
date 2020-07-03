# %%
# imports
from report_generators.reg_prof_report_generator import populateRegProfSectionData
from report_generators.ists_gen_section import populateIstsGenSectionData
from report_generators.state_gen_section import populateStateGenSectionData
from report_generators.volt_profile_section import populateVoltProfSectionData
from data_fetchers import inp_ts_data_store
print('imports complete...')

# %%
# initialize timeseries datastore with dummy data
inp_ts_data_store.initDummy()
# x = inp_ts_data_store.tsDataDf
print('data store loading complete...')

# %%
# config paths init
configFilePath = "remc_report_config.xlsx"
outputFilePath = "output/remc_report_output.xlsx"

# %%
# regional profile report generation
regSummConfigSheet = 'regional_profile'
regSummOutputSheet = 'report'
populateRegProfSectionData(
    configFilePath, regSummConfigSheet, outputFilePath, regSummOutputSheet)
print('regional profile report section data dump complete...')

# %%
# ists generation report generation
istsGenConfigSheet = 'ists_gen'
istsGenOutputSheet = 'report'
populateIstsGenSectionData(
    configFilePath, istsGenConfigSheet, outputFilePath, istsGenOutputSheet)
print('ISTS generation report section data dump complete...')

# %%
# state generation report generation
stateGenConfigSheet = 'state_gen'
stateGenOutputSheet = 'report'
populateStateGenSectionData(
    configFilePath, stateGenConfigSheet, outputFilePath, stateGenOutputSheet)
print('State generation report section data dump complete...')

# %%
# voltage profile report generation
voltSummConfigSheet = 'volt_profile'
voltSummOutputSheet = 'report'
populateVoltProfSectionData(
    configFilePath, voltSummConfigSheet, outputFilePath, voltSummOutputSheet)
print('Voltage Profile report section data dump complete...')

# %%
# initialize prev day timeseries datastore with dummy data
inp_ts_data_store.initPrevDummy()
# x = inp_ts_data_store.tsDataDf
print('prev day data store loading complete...')