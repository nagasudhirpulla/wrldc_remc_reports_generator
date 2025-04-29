def joinWith(strList, delimiter=','):
    reqStrList = [x for x in strList if isinstance(x, str)]
    combinedStr = ','.join(reqStrList)
    return combinedStr
