import wx
from ui.getfilelistpanel import *
from ui.menu import * 

class GetFileListFrame(wx.Frame):
    def __init__(self, *args, version, **kw):
        super(GetFileListFrame, self).__init__(*args, **kw)
        self.textPanel = GetFileListPanel(self)
        self.version = version
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.textPanel, 1, wx.EXPAND)

        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        self._addMenubar()

    def _addMenubar(self):
        self.menu = GetFileListMenu(self)

    def OnQuit(self, event):
        self.Close()

    def OnAbout(self, event):
        msg = self.version + '\nhttp://chobocho.com'
        title = 'About'
        wx.MessageBox(msg, title, wx.OK | wx.ICON_INFORMATION)

    def OnFindSameSize(self, event):
        print ("OnFindSameSize")
        self.textPanel.OnFindSameSize()

    def OnFindDuplicate(self, event):
        print ("OnFindDuplicate")
        self.textPanel.OnFindDuplicate()

