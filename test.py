# https://pythoncircle.com/post/668/uploading-a-file-to-ftp-server-using-python/
# https://stackoverflow.com/questions/12613797/python-script-uploading-files-via-ftp
import datetime as dt
from data_fetchers.wbes_data_store import loadWbesAcronymsSch, getWbesAcrSch, WbesSchTypeEnum
import pandas as pd
import json
from report_generators.trasEm_report_generator import generateTrasEmReport

appConfigFilePath = 'config/config.json'
configFilePath = "config/remc_report_config.xlsx"

appConfig = {}
with open(appConfigFilePath) as f:
    appConfig = json.load(f)

wbesAcrCol = 'wbes_acr'
utilAcrs = pd.read_excel(configFilePath, sheet_name='points', usecols=[wbesAcrCol])[wbesAcrCol].dropna().to_list() 
loadWbesAcronymsSch(utilAcrs, appConfig, dt.datetime.now())
print(getWbesAcrSch('SIPAT1', WbesSchTypeEnum.TRAS_EMERGENCY))
print(getWbesAcrSch('SIPAT1,SOLAPUR', WbesSchTypeEnum.NET_MU))
generateTrasEmReport("output/trasData.csv")