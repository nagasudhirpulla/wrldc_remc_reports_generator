
'''
all the inputs are lists
output will be a list of errors wrt AVC

Steps:
errWrtAvc = (actual-forecast)*100/avc
'''


def calcErrPercWithRespectToAvc(actVals, forecastVals, avcVals):
    if (len(actVals) != len(forecastVals)) and (len(actVals) != len(avcVals)):
        return None
    errVals = []
    for valIter in range(len(actVals)):
        if avcVals[valIter] != 0:
            errVal = (actVals[valIter] - forecastVals[valIter]) * \
                100/avcVals[valIter]
        else:
            errVal = 0
        errVals.append(errVal)
    return errVals


'''
all the inputs are lists
output will be a list of errors wrt Forecast

Steps:
errWrtForecast = (actual-forecast)*100/forecast
'''


def calcErrPercWithRespectToForecast(actVals, forecastVals, avcVals):
    if (len(actVals) != len(forecastVals)) and (len(actVals) != len(avcVals)):
        return None
    errVals = []
    for valIter in range(len(actVals)):
        if forecastVals[valIter] != 0:
            errVal = (actVals[valIter] - forecastVals[valIter]) * \
                100/forecastVals[valIter]
        else:
            errVal = 0
        errVals.append(errVal)
    return errVals


'''
all the inputs are lists
output will be number, i.e., RMSE %

steps:
errSquare = (actual-forecast)^2
errMeanSquare = Summation(errSquare)/num_of_blks
rootMeanSquareError = Sqrt(errMeanSquare)
'''


def calcRmsePerc(actVals, forecastVals):
    if len(actVals) == 0:
        return None
    if (len(actVals) != len(forecastVals)):
        return None
    rmse = 0
    for valIter in range(len(actVals)):
        errSquare = ((actVals[valIter] - forecastVals[valIter]))**2
        rmse = rmse + errSquare
    rmse = (rmse/len(actVals))**0.5
    return rmse


'''
all the inputs are lists
output will be number, i.e., NRMSE %

steps:
errSquare = (actual-forecast)^2
errMeanSquare = Summation(errSquare)/num_of_blks
rootMeanSquareError = Sqrt(errMeanSquare)
avcMean = Summation(avc)/num_of_blks
nrmsePerc = rootMeanSquareError*100/avcMean
'''


def calcNrmsePerc(actVals, forecastVals, avcVals):
    if len(actVals) == 0:
        return None
    if (len(actVals) != len(forecastVals)) and (len(actVals) != len(avcVals)):
        return None
    nrmse = 0
    avcMean = 0
    for valIter in range(len(actVals)):
        errSquare = (actVals[valIter] - forecastVals[valIter])**2
        nrmse = nrmse + errSquare
        avcMean = avcMean + avcVals[valIter]

    avcMean = avcMean / len(actVals)
    nrmse = (((nrmse/len(actVals))**0.5)*100/avcMean)

    return nrmse


'''
all the inputs are lists
output will be number, i.e., MAPE %

steps:
x = abs(actual-forecast)/avc
mapePerc = Summation(x)*100/num_of_blks
'''


def calcMapePerc(actVals, forecastVals, avcVals):
    if len(actVals) == 0:
        return None
    if (len(actVals) != len(forecastVals)) and (len(actVals) != len(avcVals)):
        return None
    mape = 0
    for valIter in range(len(actVals)):
        if avcVals[valIter] != 0:
            mape = mape + abs(actVals[valIter] -
                            forecastVals[valIter])/avcVals[valIter]

    mape = mape*100/len(actVals)
    return mape


'''
all the inputs are lists
output will be number, i.e., NMAE

steps:
mae = Summation(absolute(actual - forecast))/num_of_blks
avcMean = Summation(avc)/num_of_blks
nmae = mae/avcMean
'''


def calcNmae(actVals, forecastVals, avcVals):
    if len(actVals) == 0:
        return None
    if (len(actVals) != len(forecastVals)) and (len(actVals) != len(avcVals)):
        return None
    nmae = 0
    avcMean = 0
    for valIter in range(len(actVals)):
        nmae = nmae + abs(actVals[valIter] -
                          forecastVals[valIter])
        avcMean = avcMean + avcVals[valIter]

    avcMean = avcMean/len(actVals)
    nmae = nmae/len(actVals)
    nmae = nmae / avcMean
    return nmae
