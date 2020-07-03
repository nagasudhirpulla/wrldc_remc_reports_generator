# %%
# imports
from report_generators.reg_prof_report_generator import populateRegProfSectionData
from report_generators.ists_gen_section import populateIstsGenSectionData
from report_generators.state_gen_section import populateStateGenSectionData
from report_generators.volt_profile_section import populateVoltProfSectionData
from report_generators.graph_data_section import populateGraphDataSectionData
from data_fetchers import inp_ts_data_store
import datetime as dt


def printWithTs(printStr):
    print('{0}: {1}'.format(dt.datetime.strftime(
        dt.datetime.now(), '%Y-%b-%d %H:%M:%S'), printStr))


printWithTs('imports complete...')

# %%
# initialize timeseries datastore with dummy data
inp_ts_data_store.initDummy()
# x = inp_ts_data_store.tsDataDf
printWithTs('data store loading complete...')

# %%
# config paths init
configFilePath = "remc_report_config.xlsx"
outputFilePath = "output/remc_report_output.xlsx"

# %%
# regional profile report generation
regSummConfigSheet = 'regional_profile'
regSummOutputSheet = 'Daily REMC Report_Part1'
populateRegProfSectionData(
    configFilePath, regSummConfigSheet, outputFilePath, regSummOutputSheet, truncateSheet=True)
printWithTs('regional profile report section data dump complete...')

# %%
# ists generation report generation
istsGenConfigSheet = 'ists_gen'
istsGenOutputSheet = 'Daily REMC Report_Part1'
populateIstsGenSectionData(
    configFilePath, istsGenConfigSheet, outputFilePath, istsGenOutputSheet)
printWithTs('ISTS generation report section data dump complete...')

# %%
# state generation report generation
stateGenConfigSheet = 'state_gen'
stateGenOutputSheet = 'Daily REMC Report_Part1'
populateStateGenSectionData(
    configFilePath, stateGenConfigSheet, outputFilePath, stateGenOutputSheet)
printWithTs('State generation report section data dump complete...')

# %%
# voltage profile report generation
voltSummConfigSheet = 'volt_profile'
voltSummOutputSheet = 'Daily REMC Report_Part2'
populateVoltProfSectionData(
    configFilePath, voltSummConfigSheet, outputFilePath, voltSummOutputSheet, truncateSheet=True)
printWithTs('Voltage Profile report section data dump complete...')

# %%
# initialize prev day timeseries datastore with dummy data
inp_ts_data_store.initPrevDummy()
# x = inp_ts_data_store.tsDataDf
printWithTs('prev day data store loading complete...')

# %%
# graph data report generation
graphDataConfigSheet = 'graph_data'
graphDataOutputSheet = 'graph_data'
populateGraphDataSectionData(
    configFilePath, graphDataConfigSheet, outputFilePath, graphDataOutputSheet)
printWithTs('Graph data report section data dump complete...')
