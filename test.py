# https://pythoncircle.com/post/668/uploading-a-file-to-ftp-server-using-python/
# https://stackoverflow.com/questions/12613797/python-script-uploading-files-via-ftp
import datetime as dt
from utils.wbesUtils import getWbesAcronymsSch

schData = getWbesAcronymsSch("config/config.json", ["SIPAT1", "SOLAPUR"],
                   dt.datetime.now())
print(schData)
