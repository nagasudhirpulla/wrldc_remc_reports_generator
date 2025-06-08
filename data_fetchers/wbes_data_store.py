import requests
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


def getWbesAcrSch(utilAcr: str, schType: WbesSchTypeEnum):
    global wbesDataStore
    utilAcronyms = getFromJoined(utilAcr)
    return sum([wbesDataStore[wbesAcr][schType] for wbesAcr in utilAcronyms])


def loadWbesAcronymsSch(utilAcrs: list, appConfig: dict, reqDt: dt.datetime):
    global wbesDataStore
    wbesApiBase = appConfig['wbesApiBase']
    wbesapiKey = appConfig['wbesapiKey']
    wbesUname = appConfig['wbesUname']
    wbesPwd = appConfig['wbesPwd']
    response = requests.post(url=wbesApiBase, params={"apiKey": wbesapiKey},
                             json={"Date": dt.datetime.strftime(reqDt, "%d-%m-%Y"),
                                   "SchdRevNo": -1,
                                   "UserName": wbesUname,
                                   "UtilAcronymList": utilAcrs,
                                   "UtilRegionIdList": [2]  # 2 is for WR
                                   },
                             auth=HTTPBasicAuth(wbesUname, wbesPwd))
    if not response.status_code == 200:
        printWithTs(f"Error: {response.status_code}", clr='magenta')
        return None
    json_data = response.json()
    # with open("data.json", "w") as file:
    #     json.dump(json_data, file, indent=4)
    acronymsData = json_data['ResponseBody']['GroupWiseDataList']
    schData = {}
    for acrData in acronymsData:
        acrName = acrData['Acronym']

        netSchVals = acrData['NetScheduleSummary']['TotalNetSchdAmount']
        netMuVal = max(0, -0.024*statistics.mean(netSchVals))

        allSchData: list[object] = acrData['NetScheduleSummary']['NetSchdDataList']
        # find a list item where EnergyScheduleTypeName=AS and ASTypeName=EMERGENCY
        trasEmSchVals = [x for x in allSchData if x["EnergyScheduleTypeName"]
                         == "AS" and x["ASTypeName"] == "EMERGENCY"][0]['NetSchdAmount']
        trasEmMuVal = statistics.mean(trasEmSchVals)*0.024
        schData[acrName] = {
            WbesSchTypeEnum.NET_MU: netMuVal,
            WbesSchTypeEnum.TRAS_EMERGENCY: trasEmMuVal
        }
    # add missing acronyms with 0.0 values
    for u in utilAcrs:
        if u not in schData:
            schData[u] = {
                WbesSchTypeEnum.NET_MU: 0.0,
                WbesSchTypeEnum.TRAS_EMERGENCY: 0.0
            }
    wbesDataStore = schData
