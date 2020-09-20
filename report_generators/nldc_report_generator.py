import xlwings as xw
import csv
from typing import List


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
