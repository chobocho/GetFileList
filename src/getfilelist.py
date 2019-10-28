import wx
from simpleguiframe import *

SW_TITLE = "Get file list v0.1105SJ1"
WINDOW_SIZE = 480

def main(): 
    app = wx.App()
    frm = SimpleGuiFrame(None, version= SW_TITLE, title=SW_TITLE, size=(WINDOW_SIZE,WINDOW_SIZE))
    frm.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()