# https://pythoncircle.com/post/668/uploading-a-file-to-ftp-server-using-python/
# https://stackoverflow.com/questions/12613797/python-script-uploading-files-via-ftp
import os
from ftplib import FTP
import pandas as pd
import datetime as dt

configFilePath = "config/remc_report_config.xlsx"
configSheetName = 'app_config'
# get conf dataframe
confDf = pd.read_excel(
    configFilePath, sheet_name=configSheetName, header=None, index_col=0)
configDict = confDf[1].to_dict()
ftpHost = configDict['ftpHost']
ftpUsername = configDict['ftpUsername']
ftpPassword = configDict['ftpPassword']
ftpFolderPath = configDict['ftpDumpFolder']
yestDateStr = dt.datetime.strftime(
    dt.datetime.now() - dt.timedelta(days=1), '%Y_%m_%d')

srcFilePath = 'output/nldc/nldc_remc_data_{0}.csv'.format(yestDateStr)

# create FTP connection
ftpConn = FTP(host=ftpHost)
# login to ftp server
login_status = ftpConn.login(user=ftpUsername, passwd=ftpPassword)
if not(login_status[0:3] == '230'):
    print('Unable to login in NLDC ftp server for csv file transfer')
# change ftp working directory
ftpConn.cwd(ftpFolderPath)
# copy the file to remote ftp folder
reportFile = open(srcFilePath, 'rb')
ftpConn.storbinary('STOR %s' % os.path.basename(srcFilePath), reportFile, 1024)
# close file
reportFile.close()
# close FTP connection
ftpConn.quit()
print('ftp file transfer of NLDC csv file done')
