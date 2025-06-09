import datetime as dt
from utils.stringUtils import isDate, isNumber
from utils.printUtils import printWithTs


def setReportForDate(reqDtStr: str):
    global reportDt_
    dateFmt = "%Y-%m-%d"
    if isNumber(reqDtStr):
        dateOffset = float(reqDtStr)
        reportDt_ = dt.datetime.now()-dt.timedelta(days=dateOffset)
    elif isDate(reqDtStr, dateFmt):
        reportDt_ = dt.datetime.strptime(reqDtStr, dateFmt)
    else:
        printWithTs(
            f"report date {reqDtStr} is neither number offset nor a date in yyyy-mm-dd format", clr='magenta')


def getReportForDate() -> dt.datetime:
    global reportDt_
    return reportDt_
