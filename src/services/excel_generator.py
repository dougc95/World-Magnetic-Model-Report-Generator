import openpyxl
from src.models.wmm_model import WMMModel

class ExcelGenerator:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.workbook = openpyxl.Workbook()
        self.sheet = self.workbook.active
        self.sheet.title = "WMM"
        self.row_index = 1

    def generate_header(self):
        headers = [
            "Date",
            "Total Field",
            "Horizontal",
            "North",
            "East",
            "Vertical",
            "Declination",
            "Inclination",
            "",
            "Δ Total Field",
            "Δ Horizontal",
            "Δ North",
            "Δ East",
            "Δ Vertical",
            "Δ Declination",
            "Δ Inclination"
        ]
        for col_index, header in enumerate(headers, start=1):
            self.sheet.cell(row=self.row_index, column=col_index, value=header)
        self.row_index += 1

    def add_data(self, model: WMMModel, variation: dict):
        data = [
            model.year,
            model.ti,
            model.bh,
            model.bx,
            model.by,
            model.bz,
            model.dec,
            model.dip,
            "",
            variation["ti"],
            variation["bh"],
            variation["bx"],
            variation["by"],
            variation["bz"],
            variation["dec"],
            variation["dip"]
        ]
        for col_index, value in enumerate(data, start=1):
            self.sheet.cell(row=self.row_index, column=col_index, value=value)
        self.row_index += 1

    def save(self):
        self.workbook.save(self.file_path)