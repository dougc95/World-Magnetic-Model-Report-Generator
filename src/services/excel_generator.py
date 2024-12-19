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
            "Δ Inclination",
        ]
        for col_index, header in enumerate(headers, start=1):
            self.sheet.cell(row=self.row_index, column=col_index, value=header)
        self.row_index += 1

    def add_inputs(self, lat, lon, alt, start_date, end_date, step_days, output_file):
        # Create a new sheet for inputs
        input_sheet = self.workbook.create_sheet(title="Inputs")
        input_sheet.cell(row=1, column=1, value="Parameter")
        input_sheet.cell(row=1, column=2, value="Value")

        # Store the input parameters
        inputs = [
            ("Latitude", lat),
            ("Longitude", lon),
            ("Altitude (km)", alt),
            ("Start Date", start_date),
            ("End Date", end_date),
            ("Step Days", step_days),
            ("Output File", output_file),
        ]

        for i, (param, val) in enumerate(inputs, start=2):
            input_sheet.cell(row=i, column=1, value=param)
            input_sheet.cell(row=i, column=2, value=val)

    def add_data(self, model: WMMModel, variation: dict):
        data = [
            model.date,
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
            variation["dip"],
        ]
        for col_index, value in enumerate(data, start=1):
            self.sheet.cell(row=self.row_index, column=col_index, value=value)
        self.row_index += 1

    def save(self):
        self.workbook.save(self.file_path)
