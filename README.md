# Steps to generate REMC report using the script

### Open the folder of the script
### Collect the input data excel files
* Paste the SCADA files in the volt, tot_gen, ists_gen folders
* Download the REMC zip files of all forecast providers (FCA, IFT, Aleasoft, Enercast, RES) from REMC portal
* Paste the appropriate files in the folders fca, ift, aleasoft, enercast, res. A sample list of filenames for creating the reports for 15-Jul-2020 are
    * fca/DAY_AHED_2020-07-16.csv
    * fca/FC_VS_AC_2020-07-16.csv
    * fca/FC_VS_AC_2020-07-15.csv
    * ift/FC_VS_AC_2020-07-16.csv
    * aleasoft/FC_VS_AC_2020-07-16.csv
    * enercast/FC_VS_AC_2020-07-16.csv
    * res/FC_VS_AC_2020-07-16.csv

### Next steps
* double click the run.bat 
* Open the report_template.xlsx file and save it in order to trigger evaluation of formulas
* Save as in a separate folder with name like 'REMC_Report_2020_07_15.xlsx'
* Ctrl + select all sheets execpt 'remc_graph_data', 'scada_graph_data' sheets and print the excel as pdf
* Make sure all the files and folders are closed after successful report generation

