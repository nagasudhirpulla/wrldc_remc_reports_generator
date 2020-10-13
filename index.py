# %%
# imports
from report_generators.reg_prof_section import populateRegProfSectionData
from report_generators.ists_gen_section import populateIstsGenSectionData
from report_generators.state_gen_section import populateStateGenSectionData
from report_generators.volt_profile_section import populateVoltProfSectionData
from report_generators.scada_graph_data_section import populateScadaGraphDataSectionData
from report_generators.remc_reg_r0_err_section import populateRemcRegionalR0ErrSectionData
from report_generators.remc_reg_r16_err_section import populateRemcRegionalR16ErrSectionData
from report_generators.remc_ists_err_section import populateRemcIstsErrSummSectionData
from report_generators.remc_state_err_section import populateRemcStateErrSummSectionData
from report_generators.remc_ists_err_num_blks_section import populateRemcIstsErrNumBlksSectionData
from report_generators.remc_state_err_num_blks_section import populateRemcStateErrNumBlksSectionData
from report_generators.remc_ists_nrmse_section import populateRemcIstsNrmseSectionData
from report_generators.remc_state_nrmse_section import populateRemcStateNrmseSectionData
from report_generators.remc_reg_da_section import populateRemcRegDaSummSectionData
from report_generators.remc_ists_da_section import populateRemcIstsDaSummSectionData
from report_generators.remc_state_da_section import populateRemcStateDaSummSectionData
from report_generators.remc_graph_data_section import populateRemcGraphDataSectionData
from data_fetchers import inp_ts_data_store
from data_fetchers.remc_data_store import loadRemcDataStore, deleteRemcDataStore
from data_fetchers.remc_data_store import FCA_FORECAST_VS_ACTUAL_STORE_NAME, FCA_DAY_AHEAD_STORE_NAME, FCA_FORECAST_VS_ACTUAL_PREV_STORE_NAME
from data_fetchers.remc_data_store import IFT_FORECAST_VS_ACTUAL_STORE_NAME, IFT_DAY_AHEAD_STORE_NAME
from data_fetchers.remc_data_store import ALEA_FORECAST_VS_ACTUAL_STORE_NAME, ALEA_DAY_AHEAD_STORE_NAME
from data_fetchers.remc_data_store import RES_FORECAST_VS_ACTUAL_STORE_NAME, RES_DAY_AHEAD_STORE_NAME
from data_fetchers.remc_data_store import ENER_FORECAST_VS_ACTUAL_STORE_NAME, ENER_DAY_AHEAD_STORE_NAME
import datetime as dt
import argparse
from utils.printUtils import printWithTs
from report_generators.paste_report_data import pasteDataToTemplateFile
from report_generators.nldc_report_generator import generateNldcReport, transferNldcRepToFtpLocation

printWithTs('imports complete...', clr='green')


# %%
printWithTs('loading SCADA Total ISTS Gen data...', clr='magenta')
# initialize timeseries datastore
inp_ts_data_store.loadGenTsData()
# x = inp_ts_data_store.tsDataDf
printWithTs('done loading SCADA Total ISTS Gen data store...', clr='green')

# %%
printWithTs(
    'started loading REMC FCA Forecast Vs Actual data store...', clr='magenta')
# initialize REMC FCA forecast Vs actual timeseries datastore
loadRemcDataStore(FCA_FORECAST_VS_ACTUAL_STORE_NAME)
# x = inp_ts_data_store.tsDataDf
printWithTs(
    'REMC FCA Forecast Vs Actual data store loading complete...', clr='green')

# %%
# file paths init
configFilePath = "config/remc_report_config.xlsx"
outputFilePath = "output/report_output_data.xlsx"
templateFilePath = 'output/report_template.xlsx'

# %%
printWithTs('started parsing arguments...', clr='magenta')
# parse arguments when invoked directly
parser = argparse.ArgumentParser()
# add argument with flag --name
parser.add_argument(
    '--config', help='filePath of config file', default=configFilePath)
parser.add_argument(
    '--output', help='filePath of config file', default=outputFilePath)
parser.add_argument(
    '--template', help='filePath of template file', default=templateFilePath)
args = parser.parse_args()

# read arguments
configFilePath = args.config
outputFilePath = args.output
templateFilePath = args.template
printWithTs('parsing input arguments done...', clr='green')

# %%
printWithTs('started regional profile report generation...', clr='magenta')
# regional profile report generation
regSummConfigSheet = 'regional_profile'
regSummOutputSheet = 'Daily REMC Report_Part1'
populateRegProfSectionData(
    configFilePath, regSummConfigSheet, outputFilePath, regSummOutputSheet, truncateSheet=True)
printWithTs('regional profile report section data dump complete...', clr='green')

# %%
printWithTs('started ists generation report generation...', clr='magenta')
# ists generation report generation
istsGenConfigSheet = 'ists_gen'
istsGenOutputSheet = 'Daily REMC Report_Part1'
populateIstsGenSectionData(
    configFilePath, istsGenConfigSheet, outputFilePath, istsGenOutputSheet)
printWithTs('ISTS generation report section data dump complete...', clr='green')

# %%
printWithTs('started state generation report generation...', clr='magenta')
# state generation report generation
stateGenConfigSheet = 'state_gen'
stateGenOutputSheet = 'Daily REMC Report_Part1'
populateStateGenSectionData(
    configFilePath, stateGenConfigSheet, outputFilePath, stateGenOutputSheet)
printWithTs('State generation report section data dump complete...', clr='green')

# %%
# deleting SCADA Total ISTS Gen data from global dataframe
printWithTs('deleting SCADA Total ISTS Gen data...', clr='magenta')
inp_ts_data_store.deleteTsData()
printWithTs('done deleting SCADA Total ISTS Gen data...', clr='green')

# %%
# loading SCADA voltage data to global dataframe
printWithTs('loading SCADA voltage data...', clr='magenta')
inp_ts_data_store.loadVoltTsData()
printWithTs('done loading SCADA voltage data...', clr='green')

# %%
printWithTs('started voltage profile report generation...', clr='magenta')
# voltage profile report generation
voltSummConfigSheet = 'volt_profile'
voltSummOutputSheet = 'Daily REMC Report_Part2'
populateVoltProfSectionData(
    configFilePath, voltSummConfigSheet, outputFilePath, voltSummOutputSheet, truncateSheet=True)
printWithTs('Voltage Profile report section data dump complete...', clr='green')

# %%
printWithTs('started REMC regional R0 error summary generation...', clr='magenta')
# REMC regional R0 error report generation
regR0ErrSummConfigSheet = 'remc_regional_r0_error'
regR0ErrSummOutputSheet = 'Daily REMC Report_Part3'
populateRemcRegionalR0ErrSectionData(
    configFilePath, regR0ErrSummConfigSheet, outputFilePath, regR0ErrSummOutputSheet, truncateSheet=True)
printWithTs('REMC regional R0 error summary data dump complete...', clr='green')

# %%
printWithTs(
    'started REMC regional R16 error summary generation...', clr='magenta')
# REMC regional R16 error report generation
regR16ErrSummConfigSheet = 'remc_regional_r16_error'
regR16ErrSummOutputSheet = 'Daily REMC Report_Part3'
populateRemcRegionalR16ErrSectionData(
    configFilePath, regR16ErrSummConfigSheet, outputFilePath, regR16ErrSummOutputSheet, truncateSheet=False)
printWithTs('REMC regional R16 error summary data dump complete...', clr='green')

# %%
printWithTs('started REMC ISTS error summary generation...', clr='magenta')
# REMC ISTS error report generation
istsErrSummConfigSheet = 'remc_ists_error'
istsErrSummOutputSheet = 'Daily REMC Report_Part3'
populateRemcIstsErrSummSectionData(
    configFilePath, istsErrSummConfigSheet, outputFilePath, istsErrSummOutputSheet, truncateSheet=False)
printWithTs('REMC ISTS error summary data dump complete...', clr='green')

# %%
printWithTs('started REMC state error summary generation...', clr='magenta')
# REMC State error report generation
stateErrSummConfigSheet = 'remc_state_error'
stateErrSummOutputSheet = 'Daily REMC Report_Part3'
populateRemcStateErrSummSectionData(
    configFilePath, stateErrSummConfigSheet, outputFilePath, stateErrSummOutputSheet, truncateSheet=False)
printWithTs('REMC state error summary data dump complete...', clr='green')

# %%
printWithTs(
    'started loading REMC IFT Forecast Vs Actual data store...', clr='magenta')
loadRemcDataStore(IFT_FORECAST_VS_ACTUAL_STORE_NAME)
printWithTs(
    'done loading REMC IFT Forecast Vs Actual data store...', clr='green')

printWithTs(
    'started loading REMC ALEASOFT Forecast Vs Actual data store...', clr='magenta')
loadRemcDataStore(ALEA_FORECAST_VS_ACTUAL_STORE_NAME)
printWithTs(
    'done loading REMC ALEASOFT Forecast Vs Actual data store...', clr='green')

printWithTs(
    'started loading REMC RES Forecast Vs Actual data store...', clr='magenta')
loadRemcDataStore(RES_FORECAST_VS_ACTUAL_STORE_NAME)
printWithTs(
    'done loading REMC RES Forecast Vs Actual data store...', clr='green')

printWithTs(
    'started loading REMC ENERCAST Forecast Vs Actual data store...', clr='magenta')
loadRemcDataStore(ENER_FORECAST_VS_ACTUAL_STORE_NAME)
printWithTs(
    'done loading REMC ENERCAST Forecast Vs Actual data store...', clr='green')

# %%
printWithTs(
    'started REMC ISTS error number of blks report generation...', clr='magenta')
# REMC ISTS error number of blks
istsFspNumBlksConfigSheet = 'ists_fsp_err_num_blks'
istsFspNumBlksOutputSheet = 'Daily REMC Report_Part3'
populateRemcIstsErrNumBlksSectionData(
    configFilePath, istsFspNumBlksConfigSheet, outputFilePath, istsFspNumBlksOutputSheet, truncateSheet=False)
printWithTs('REMC ISTS error number of blks data dump complete...', clr='green')

# %%
printWithTs(
    'started REMC State error number of blks report generation...', clr='magenta')
# REMC REMC State error number of blks
stateFspNumBlksConfigSheet = 'state_fsp_err_num_blks'
stateFspNumBlksOutputSheet = 'Daily REMC Report_Part3'
populateRemcStateErrNumBlksSectionData(
    configFilePath, stateFspNumBlksConfigSheet, outputFilePath, stateFspNumBlksOutputSheet, truncateSheet=False)
printWithTs('REMC State error number of blks data dump complete...', clr='green')

# %%
printWithTs(
    'started REMC ISTS RMSE report generation...', clr='magenta')
# REMC ISTS RMSE
istsFspRmseConfigSheet = 'ists_fsp_rmse'
istsFspRmseOutputSheet = 'Daily REMC Report_Part3'
populateRemcIstsNrmseSectionData(
    configFilePath, istsFspRmseConfigSheet, outputFilePath, istsFspRmseOutputSheet, truncateSheet=False)
printWithTs('REMC ISTS RMSE data dump complete...', clr='green')

# %%
printWithTs(
    'started REMC State RMSE report generation...', clr='magenta')
# REMC State RMSE
stateFspRmseConfigSheet = 'state_fsp_rmse'
stateFspRmseOutputSheet = 'Daily REMC Report_Part3'
populateRemcStateNrmseSectionData(
    configFilePath, stateFspRmseConfigSheet, outputFilePath, stateFspRmseOutputSheet, truncateSheet=False)
printWithTs('REMC State RMSE data dump complete...', clr='green')

# %%
printWithTs(
    'started deleting REMC IFT Forecast Vs Actual data store...', clr='magenta')
deleteRemcDataStore(IFT_FORECAST_VS_ACTUAL_STORE_NAME)
printWithTs(
    'done deleting REMC IFT Forecast Vs Actual data store...', clr='green')

printWithTs(
    'started deleting REMC ALEASOFT Forecast Vs Actual data store...', clr='magenta')
deleteRemcDataStore(ALEA_FORECAST_VS_ACTUAL_STORE_NAME)
printWithTs(
    'done deleting REMC ALEASOFT Forecast Vs Actual data store...', clr='green')

printWithTs(
    'started deleting REMC RES Forecast Vs Actual data store...', clr='magenta')
deleteRemcDataStore(RES_FORECAST_VS_ACTUAL_STORE_NAME)
printWithTs(
    'done deleting REMC RES Forecast Vs Actual data store...', clr='green')

printWithTs(
    'started deleting REMC ENERCAST Forecast Vs Actual data store...', clr='magenta')
deleteRemcDataStore(ENER_FORECAST_VS_ACTUAL_STORE_NAME)
printWithTs(
    'done deleting REMC ENERCAST Forecast Vs Actual data store...', clr='green')

# %%
printWithTs(
    'started loading REMC FCA Day Ahead data store...', clr='magenta')
loadRemcDataStore(FCA_DAY_AHEAD_STORE_NAME)
printWithTs(
    'done loading REMC FCA Day Ahead data store...', clr='green')

# %%
printWithTs(
    'started REMC Regional Day Ahead report generation...', clr='magenta')
# REMC Regional Regional Day Ahead report
regDaConfigSheet = 'regional_da_forecast'
regDaOutputSheet = 'Daily REMC Report_Part3'
populateRemcRegDaSummSectionData(
    configFilePath, regDaConfigSheet, outputFilePath, regDaOutputSheet, truncateSheet=False)
printWithTs('REMC Regional Day Ahead data dump complete...', clr='green')

# %%
printWithTs(
    'started REMC Ists Day Ahead report generation...', clr='magenta')
# REMC Ists Day Ahead report
istsDaConfigSheet = 'ists_da_forecast'
istsDaOutputSheet = 'Daily REMC Report_Part3'
populateRemcIstsDaSummSectionData(
    configFilePath, istsDaConfigSheet, outputFilePath, istsDaOutputSheet, truncateSheet=False)
printWithTs('REMC Ists Day Ahead data dump complete...', clr='green')

# %%
printWithTs(
    'started REMC State Day Ahead report generation...', clr='magenta')
# REMC Ists Day Ahead report
stateDaConfigSheet = 'state_da_forecast'
stateDaOutputSheet = 'Daily REMC Report_Part3'
populateRemcStateDaSummSectionData(
    configFilePath, stateDaConfigSheet, outputFilePath, stateDaOutputSheet, truncateSheet=False)
printWithTs('REMC State Day Ahead data dump complete...', clr='green')


# %%
'''
printWithTs('started loading SCADA prev day data store...', clr='magenta')
# initialize prev day timeseries datastore
inp_ts_data_store.initPrevData()
# x = inp_ts_data_store.tsDataDf
printWithTs('prev day data store loading complete...', clr='green')
'''

# %%
printWithTs('started SCADA graph data report generation...', clr='magenta')
# graph data report generation
scadaGraphDataConfigSheet = 'scada_graph_data'
scadaGraphDataOutputSheet = 'scada_graph_data'
populateScadaGraphDataSectionData(
    configFilePath, scadaGraphDataConfigSheet, templateFilePath, scadaGraphDataOutputSheet)
printWithTs('SCADA Graph data report section data dump complete...', clr='green')

# %%
# deleting SCADA Voltage data from global dataframe
printWithTs('deleting SCADA Voltage data...', clr='magenta')
inp_ts_data_store.deleteTsData()
printWithTs('done deleting SCADA Voltage data...', clr='green')

# %%
printWithTs(
    'started loading REMC FCA Forecast Vs Actual Prev data store...', clr='magenta')
# initialize REMC FCA forecast Vs actual Prev timeseries datastore
loadRemcDataStore(FCA_FORECAST_VS_ACTUAL_PREV_STORE_NAME)
printWithTs(
    'REMC FCA Forecast Vs Actual Prev data store loading complete...', clr='green')

# %%
printWithTs('started REMC graph data report generation...', clr='magenta')
# graph data report generation
graphDataConfigSheet = 'remc_graph_data'
graphDataOutputSheet = 'remc_graph_data'
populateRemcGraphDataSectionData(
    configFilePath, graphDataConfigSheet, templateFilePath, graphDataOutputSheet)
printWithTs('REMC Graph data report section data dump complete...', clr='green')

# %%
# pasting data from date file to template file
pasteDataToTemplateFile(outputFilePath, templateFilePath)
printWithTs('Data pasting done from data file to template file...', clr='green')
printWithTs('Report preparation done !', clr='green')

# %%
srcReportPath = 'output/report_template.xlsx'
srcShNames = ["Daily REMC Report_Part1",
              "Daily REMC Report_Part2", "Daily REMC Report_Part3"]

yestDateStr = dt.datetime.strftime(
    dt.datetime.now() - dt.timedelta(days=1), '%Y_%m_%d')
outputCsvPath = 'output/nldc/nldc_remc_data_{0}.csv'.format(yestDateStr)
generateNldcReport(srcReportPath, srcShNames, outputCsvPath)
printWithTs('NLDC Report preparation done !', clr='green')

# %%
appConfigSheet = 'app_config'
isNldcFtpSuccess = transferNldcRepToFtpLocation(
    configFilePath, appConfigSheet, outputCsvPath)
if isNldcFtpSuccess:
    printWithTs('NLDC CSV Ftp transfer done !', clr='green')
else:
    printWithTs('NLDC CSV FTP transfer not done...', clr='green')
