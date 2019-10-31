import wx
from simpleguipanel import *
from menu import * 

class SimpleGuiFrame(wx.Frame):
    def __init__(self, *args, version, **kw):
        super(SimpleGuiFrame, self).__init__(*args, **kw)
        self.panel = SimpleGuiPanel(self)
        self.version = version
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(sizer)

        self._addMenubar()

    def _addMenubar(self):
        self.menu = SimpleGuiMenu(self)

    def OnQuit(self, event):
        self.Close()

    def OnAbout(self, event):
        msg = self.version + '\nhttp://chobocho.com'
        title = 'About'
        wx.MessageBox(msg, title, wx.OK | wx.ICON_INFORMATION)

    def OnFindSameSize(self, event):
        print ("OnFindSameSize")
        self.panel.OnFindSameSize()

    def OnFindDuplicate(self, event):
        print ("OnFindDuplicate")
        self.panel.OnFindDuplicate()

