import win32com.client
import os
from utils.dateUtils import getReportForDate, setReportForDate
from utils.printUtils import printWithTs
from report_generators.nldc_report_generator import generateNldcReport
from openpyxl import load_workbook


# create NLDC CSV file
srcReportPath = 'output/report_template.xlsx'
srcShNames = ["Daily REMC Report_Part1",
              "Daily REMC Report_Part2", "Daily REMC Report_Part3"]

# get reportFor date from excel
templWb = load_workbook(srcReportPath)
dateStr = templWb[srcShNames[0]]["K3"].value.strftime('%Y-%m-%d')
setReportForDate(dateStr)
templWb.close()

reportDate = getReportForDate()
outputCsvPath = f'output/nldc/nldc_remc_data_{reportDate.strftime("%Y_%m_%d")}.csv'
generateNldcReport(srcReportPath, srcShNames, outputCsvPath)
printWithTs('NLDC Report preparation done !', clr='green')

# PDF output path
pdf_file_path = os.path.abspath(
    f'output/pdfs/REMC report_Night_{reportDate.strftime("%d_%m_%Y")}.pdf')

# List of sheet names to be printed
sheet_names = ["Daily REMC Report_Part1", "Daily REMC Report_Part2", "Daily REMC Report_Part3",
               "WR_GRAPHS", "STATE_GRAPHS", "PS_GRAPHS", "VOLT_GRAPHS"]

# Create Excel application object
excel = win32com.client.Dispatch("Excel.Application")
# excel.Visible = False  # Optional: Hide Excel window

# Open the Excel workbook
excel_file_path = os.path.abspath(srcReportPath)
workbook = excel.Workbooks.Open(excel_file_path)

# Create an empty list to store the worksheet objects
worksheets = []

# Iterate through the sheet names and add them to the worksheets list
for sheet_name in sheet_names:
    try:
        worksheet = workbook.Sheets(sheet_name)
        worksheets.append(worksheet)
    except Exception as e:
        printWithTs(f"Sheet '{sheet_name}' not found: {e}", clr='magenta')

# Select the desired sheets
workbook.Worksheets(tuple(worksheet.Name for worksheet in worksheets)).Select()

# Export selected sheets to PDF
try:
    workbook.ActiveSheet.ExportAsFixedFormat(0, pdf_file_path)
    printWithTs('PDF created successfully !', clr='green')
except Exception as e:
    printWithTs(f"Error creating PDF: {e}", clr='magenta')

# Select the first sheet
workbook.Worksheets((worksheets[0].Name)).Select()

# Close the workbook and quit Excel application
workbook.Close(SaveChanges=True)
excel.Quit()

# Optional: Delete the Excel application object
del excel
