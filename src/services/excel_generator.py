import openpyxl

class ExcelGenerator:
    @staticmethod
    def generate_excel_topics():
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.title = "WMM"
        print(sheet.title)
        # Topics
        sheet.cell(row=1, column=1, value='Date')
        # ... (rest of the code remains the same)
        wb.save("output.xlsx")