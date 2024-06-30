import wx
from gui.wmm_gui import WMMGui

if __name__ == '__main__':
    app = wx.App()
    frame = WMMGui(None, title='WMM Excel Generator', size=(800, 300))
    frame.Show()
    app.MainLoop()