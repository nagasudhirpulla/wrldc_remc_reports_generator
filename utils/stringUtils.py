import datetime as dt


def joinWith(strList, delimiter=','):
    reqStrList = [x.strip() for x in strList if isinstance(x, str)]
    combinedStr = ','.join(reqStrList)
    return combinedStr


def getFromJoined(combinedStr: str, delimiter=','):
    if not isinstance(combinedStr, str):
        return []
    strs = combinedStr.split(delimiter)
    strs = [x.strip() for x in strs]
    return strs


def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def isDate(s, dateFmt):
    try:
        res = dt.datetime.strptime(s, dateFmt)
        return True
    except ValueError:
        return False
