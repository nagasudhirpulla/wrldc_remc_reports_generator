def joinWith(strList, delimiter=','):
    reqStrList = [x for x in strList if isinstance(x, str)]
    combinedStr = ','.join(reqStrList)
    return combinedStr


def getFromJoined(combinedStr: str, delimiter=','):
    if not isinstance(combinedStr, str):
        return []
    strs = combinedStr.split(delimiter)
    return strs
