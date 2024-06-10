from gui.wmm_gui import WMMGui
import wx

if __name__ == '__main__':
    app = wx.App()
    frame = WMMGui(None, "Reports", 800, 300)
    app.MainLoop()