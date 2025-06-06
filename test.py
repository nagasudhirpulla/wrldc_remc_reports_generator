# https://pythoncircle.com/post/668/uploading-a-file-to-ftp-server-using-python/
# https://stackoverflow.com/questions/12613797/python-script-uploading-files-via-ftp
import datetime as dt
from utils.wbesUtils import getWbesSch, WbesSchTypeEnum

schMu = getWbesSch("config/config.json", "SIPAT1",
                   dt.datetime.now(), schType=WbesSchTypeEnum.NET_MU)
print(schMu)
trasEmMu = getWbesSch("config/config.json", "SIPAT1",
                      dt.datetime.now(), schType=WbesSchTypeEnum.TRAS_EMERGENCY)
print(trasEmMu)
