import wx
from src.models.wmm_model import WMMModel
from src.services.wmm_calculator import WMMCalculator
from src.utils.date_utils import DateUtils

class WMMGui(wx.Frame):
    # ... (existing GUI code remains the same)

    def onClickGen(self, event):
        # ...
        self.writerBook(self.generateDates())

    def generateDates(self):
        # ...
        return cup

    def writerBook(self, dates):
        # ...
        for x in dates:
            model = WMMModel(self.lat, self.lon, self.alt, x)
            x = DateUtils.decimal_year(x)
            WMMCalculator.calculate(model)
            # ...
        # ...