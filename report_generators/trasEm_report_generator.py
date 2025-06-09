import csv
from data_fetchers.wbes_data_store import getWbesDataStore, WbesSchTypeEnum


def generateTrasEmReport(outputCsvPath: str):
    wbesData = getWbesDataStore()
    with open(outputCsvPath, 'w', newline="") as f:
        c = csv.writer(f)
        c.writerow(["Name", "TRAS Emergency Schedule"])
        for util in wbesData:
            c.writerow([util, wbesData[util][WbesSchTypeEnum.TRAS_EMERGENCY]])
