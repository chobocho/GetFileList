import xlwt

class ExcelManager:
    def __init__(self, filename="example.xls"):
        self.filename = filename

    def saveData(self, filelist):
        excel_file = xlwt.Workbook(encoding='utf-8')
        worksheet = excel_file.add_sheet('file_list')

        for i in range(len(filelist)):
            worksheet.write(i, 0, filelist[i])

        excel_file.save(self.filename)