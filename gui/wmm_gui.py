import wx
import wx.adv
from src.models.wmm_model import WMMModel
from src.services.wmm_calculator import WMMCalculator
from src.services.excel_generator import ExcelGenerator
from src.utils.date_utils import DateUtils

class WMMGui(wx.Frame):
    def __init__(self, parent, title, size):
        super().__init__(parent, title=title, size=size)
        self.init_ui()

    def init_ui(self):
        panel = wx.Panel(self)

        # Create input fields, labels, and buttons
        self.txt_lat = wx.TextCtrl(panel, pos=(80, 55))
        self.txt_lon = wx.TextCtrl(panel, pos=(80, 130))
        self.txt_alt = wx.TextCtrl(panel, pos=(80, 210))
        self.txt_start_date = wx.adv.DatePickerCtrl(panel, pos=(220, 40), style=wx.adv.DP_DROPDOWN)
        self.txt_end_date = wx.adv.DatePickerCtrl(panel, pos=(500, 40), style=wx.adv.DP_DROPDOWN)
        self.txt_step_days = wx.TextCtrl(panel, pos=(290, 210), size=(50, 25))
        self.txt_output_file = wx.TextCtrl(panel, pos=(585, 210))

        btn_generate = wx.Button(panel, label="Generate", pos=(435, 200), size=(75, 50))
        btn_generate.Bind(wx.EVT_BUTTON, self.on_generate)

        # Add labels
        wx.StaticText(panel, label="Latitude", pos=(20, 55))
        wx.StaticText(panel, label="Longitude", pos=(20, 130))
        wx.StaticText(panel, label="Altitude", pos=(20, 210))
        wx.StaticText(panel, label="Start Date", pos=(300, 10))
        wx.StaticText(panel, label="End Date", pos=(585, 10))
        wx.StaticText(panel, label="Step (days)", pos=(250, 210))
        wx.StaticText(panel, label="Output File", pos=(535, 210))

        # Add radio buttons
        self.rb_north = wx.RadioButton(panel, label="North", pos=(50, 10), style=wx.RB_GROUP)
        self.rb_south = wx.RadioButton(panel, label="South", pos=(50, 30))
        self.rb_east = wx.RadioButton(panel, label="East", pos=(50, 90), style=wx.RB_GROUP)
        self.rb_west = wx.RadioButton(panel, label="West", pos=(50, 110))
        self.rb_km = wx.RadioButton(panel, label="KM", pos=(50, 165), style=wx.RB_GROUP)
        self.rb_ft = wx.RadioButton(panel, label="Feet", pos=(50, 185))

        self.Center()

    def on_generate(self, event):
        # Get input values from text fields
        lat = float(self.txt_lat.GetValue())
        lon = float(self.txt_lon.GetValue())
        alt = float(self.txt_alt.GetValue())
        start_date = self.txt_start_date.GetValue().Format('%Y-%m-%d')
        end_date = self.txt_end_date.GetValue().Format('%Y-%m-%d')
        step_days = int(self.txt_step_days.GetValue())
        output_file = self.txt_output_file.GetValue()

        # Adjust latitude based on radio button selection
        if self.rb_south.GetValue():
            lat = -lat

        # Adjust longitude based on radio button selection
        if self.rb_west.GetValue():
            lon = -lon

        # Adjust altitude based on radio button selection
        if self.rb_ft.GetValue():
            alt = alt * 0.3048  # Convert feet to kilometers

        # Generate date range
        dates = DateUtils.date_range(start_date, end_date, step_days)

        # Create ExcelGenerator instance
        excel_generator = ExcelGenerator(output_file)
        excel_generator.generate_header()

        # Perform calculations and add data to Excel
        for date in dates:
            model = WMMModel(lat, lon, alt, date)
            WMMCalculator.calculate(model)
            next_model = WMMCalculator.calculate_next_year(model)
            variation = WMMCalculator.calculate_variation(model, next_model)
            excel_generator.add_data(model, variation)

        # Save the Excel file
        excel_generator.save()

        # Show completion message
        wx.MessageBox("Excel file generated successfully!", "Complete", wx.OK | wx.ICON_INFORMATION)