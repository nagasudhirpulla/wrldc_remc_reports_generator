from report_generators.nldc_report_generator import generateNldcReport

srcReportPath = 'output/report_template.xlsx'
srcShNames = ["Daily REMC Report_Part1",
              "Daily REMC Report_Part2", "Daily REMC Report_Part3"]
outputCsvPath = 'output/nldc_remc_data.csv'

generateNldcReport(srcReportPath, srcShNames, outputCsvPath)
