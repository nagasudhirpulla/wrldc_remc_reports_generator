import xlwings as xw
import csv
from typing import List
import pandas as pd
import os
from ftplib import FTP


def generateNldcReport(srcReportPath: str, srcShNames: List[str], outputCsvPath: str):
    """creates nldc csv report by copying data from main report

    Args:
        srcReportPath (str): file path of main report excel file
        srcShNames (List[str]): sheet names to copy data from
        outputCsvPath (str): file path of the nldc report csv file for dumping data
    """
    wb = xw.Book(srcReportPath)
    app = xw.apps.active
    try:
        wb.save()
        with open(outputCsvPath, 'w', newline="") as f:
            for sName in srcShNames:
                sh = wb.sheets[sName]
                c = csv.writer(f)
                shRange = sh.used_range
                for rNum in range(shRange.shape[0]):
                    c.writerow(shRange.value[rNum])
    finally:
        # wb.close()
        app.quit()

# https://pythoncircle.com/post/668/uploading-a-file-to-ftp-server-using-python/
# https://stackoverflow.com/questions/12613797/python-script-uploading-files-via-ftp
def transferNldcRepToFtpLocation(configFilePath: str, configSheetName: str, srcFilePath: str) -> bool:
    """Transfers NLDC report to remote FTP location as per excel configuration

    Args:
        configFilePath (str): path of config file
        configSheetName (str): sheet name for ftp configuration
        srcFilePath (str): file path of NLDC report to be transfered

    Returns:
        bool: True if process is a success
    """    
    # get conf dataframe
    confDf = pd.read_excel(
        configFilePath, sheet_name=configSheetName, header=None, index_col=0)
    configDict = confDf[1].to_dict()
    ftpHost = configDict['ftpHost']
    ftpUsername = configDict['ftpUsername']
    ftpPassword = configDict['ftpPassword']
    ftpFolderPath = configDict['ftpDumpFolder']
    # start ftp file transfer process
    try:
        # create FTP connection
        ftpConn = FTP(host=ftpHost)
        # login to ftp server
        login_status = ftpConn.login(user=ftpUsername, passwd=ftpPassword)
        if not(login_status[0:3] == '230'):
            print('Unable to login in NLDC ftp server for csv file transfer')
            return False
        # change ftp working directory
        ftpConn.cwd(ftpFolderPath)
        # copy the file to remote ftp folder
        reportFile = open(srcFilePath, 'rb')
        ftpConn.storbinary('STOR %s' % os.path.basename(
            srcFilePath), reportFile, 1024)
        # close file
        reportFile.close()
        # close FTP connection
        ftpConn.quit()
        return True
    except:
        return False
