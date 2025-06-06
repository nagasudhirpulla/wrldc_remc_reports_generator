import requests
import json
import datetime as dt
import statistics
from requests.auth import HTTPBasicAuth
from utils.printUtils import printWithTs
import enum
from utils.stringUtils import getFromJoined


@enum.unique
class WbesSchTypeEnum(enum.Enum):
    NET_MU = 1
    TRAS_EMERGENCY = 2


def getWbesSch(configFilePath: str, utilAcr: str, reqDt: dt.datetime, schType: WbesSchTypeEnum):
    utilAcronyms = getFromJoined(utilAcr)
    return sum([getWbesSinglePntSch(configFilePath, wbesAcr, reqDt, schType) for wbesAcr in utilAcronyms])


def getWbesSinglePntSch(configFilePath: str, utilAcr: str, reqDt: dt.datetime, schType: WbesSchTypeEnum):
    # get config from json
    configDict = {}
    with open(configFilePath) as f:
        configDict = json.load(f)
    wbesApiBase = configDict['wbesApiBase']
    wbesapiKey = configDict['wbesapiKey']
    wbesUname = configDict['wbesUname']
    wbesPwd = configDict['wbesPwd']
    response = requests.post(url=wbesApiBase, params={"apiKey": wbesapiKey},
                             json={"Date": dt.datetime.strftime(reqDt, "%d-%m-%Y"),
                                   "SchdRevNo": -1,
                                   "UserName": wbesUname,
                                   "UtilAcronymList": [utilAcr],
                                   "UtilRegionIdList": [2]  # 2 is for WR
                                   },
                             auth=HTTPBasicAuth(wbesUname, wbesPwd))
    if not response.status_code == 200:
        printWithTs(f"Error: {response.status_code}", clr='magenta')
        return None
    json_data = response.json()
    # print(json_data)
    if schType == WbesSchTypeEnum.NET_MU:
        netSchVals = json_data['ResponseBody']['GroupWiseDataList'][0]['NetScheduleSummary']['TotalNetSchdAmount']
        netMuVal = statistics.mean(netSchVals)*0.024
        return netMuVal
    elif schType == WbesSchTypeEnum.TRAS_EMERGENCY:
        allSchData: list[object] = json_data['ResponseBody']['GroupWiseDataList'][0]['NetScheduleSummary']['NetSchdDataList']
        # find a list item where EnergyScheduleTypeName=AS and ASTypeName=EMERGENCY
        trasEmSchVals = [x for x in allSchData if x["EnergyScheduleTypeName"]
                         == "AS" and x["ASTypeName"] == "EMERGENCY"][0]['NetSchdAmount']
        trasEmSchMuVal = statistics.mean(trasEmSchVals)*0.024
        return trasEmSchMuVal
    else:
        printWithTs("Unknown sch type given", clr='magenta')
    return None
