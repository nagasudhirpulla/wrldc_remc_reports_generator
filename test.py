# %%
# imports
from report_generators.reg_prof_section import populateRegProfSectionData
from report_generators.ists_gen_section import populateIstsGenSectionData
from report_generators.state_gen_section import populateStateGenSectionData
from report_generators.volt_profile_section import populateVoltProfSectionData
from report_generators.graph_data_section import populateGraphDataSectionData
from data_fetchers import inp_ts_data_store
import datetime as dt
import argparse
from utils.printUtils import printWithTs

printWithTs('imports complete...', clr='green')


# %%
# initialize timeseries datastore with dummy data
inp_ts_data_store.initDummy()
# x = inp_ts_data_store.tsDataDf
printWithTs('data store loading complete...', clr='green')

# %%
# config paths init
configFilePath = "config/remc_report_config.xlsx"
outputFilePath = "output/report_output_data.xlsx"

# %%
# parse arguments when invoked directly
parser = argparse.ArgumentParser()
# add argument with flag --name
parser.add_argument(
    '--config', help='filePath of config file', default=configFilePath)
parser.add_argument(
    '--output', help='filePath of config file', default=outputFilePath)
args = parser.parse_args()

# read arguments
configFilePath = args.config
outputFilePath = args.output
printWithTs('parsing input arguments done...', clr='green')

# %%
# regional profile report generation
regSummConfigSheet = 'regional_profile'
regSummOutputSheet = 'Daily REMC Report_Part1'
populateRegProfSectionData(
    configFilePath, regSummConfigSheet, outputFilePath, regSummOutputSheet, truncateSheet=True)
printWithTs('regional profile report section data dump complete...', clr='green')

# %%
# ists generation report generation
istsGenConfigSheet = 'ists_gen'
istsGenOutputSheet = 'Daily REMC Report_Part1'
populateIstsGenSectionData(
    configFilePath, istsGenConfigSheet, outputFilePath, istsGenOutputSheet)
printWithTs('ISTS generation report section data dump complete...', clr='green')

# %%
# state generation report generation
stateGenConfigSheet = 'state_gen'
stateGenOutputSheet = 'Daily REMC Report_Part1'
populateStateGenSectionData(
    configFilePath, stateGenConfigSheet, outputFilePath, stateGenOutputSheet)
printWithTs('State generation report section data dump complete...', clr='green')

# %%
# voltage profile report generation
voltSummConfigSheet = 'volt_profile'
voltSummOutputSheet = 'Daily REMC Report_Part2'
populateVoltProfSectionData(
    configFilePath, voltSummConfigSheet, outputFilePath, voltSummOutputSheet, truncateSheet=True)
printWithTs('Voltage Profile report section data dump complete...', clr='green')

# %%
# initialize prev day timeseries datastore with dummy data
inp_ts_data_store.initPrevDummy()
# x = inp_ts_data_store.tsDataDf
printWithTs('prev day data store loading complete...', clr='green')

# %%
# graph data report generation
graphDataConfigSheet = 'graph_data'
graphDataOutputSheet = 'graph_data'
populateGraphDataSectionData(
    configFilePath, graphDataConfigSheet, outputFilePath, graphDataOutputSheet)
printWithTs('Graph data report section data dump complete...', clr='green')
