from openpyxl import load_workbook
import pandas as pd

## todo create excel if not exists

def deleteSheetIfExists(filePath, sheetName):
    wb = load_workbook(filePath)   # open an Excel file and return a workbook
    if sheetName in wb.sheetnames:
        # delete sheet
        wb.remove_sheet(wb.get_sheet_by_name(sheetName))
        wb.save(filePath)
    wb.close()

def saveDfToExcelSheet(filePath, sheetName, dataDf):
    deleteSheetIfExists(filePath, sheetName)
    with pd.ExcelWriter(filePath, mode='a') as writer: # pylint: disable=abstract-class-instantiated
        dataDf.to_excel(writer, sheet_name=sheetName, index=False)