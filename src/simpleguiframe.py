import wx
from simpleguipanel import *

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
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fileItem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit App')
        self.Bind(wx.EVT_MENU, self.OnQuit, fileItem)
        menubar.Append(fileMenu, '&File')

        helpMenu = wx.Menu()
        aboutItemId = wx.NewId()
        aboutItem = helpMenu.Append(aboutItemId, 'About', 'About')
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)
        menubar.Append(helpMenu, '&Help')

        self.SetMenuBar(menubar)

    def OnQuit(self, event):
        self.Close()

    def OnAbout(self, event):
        msg = self.version + '\nhttp://chobocho.com'
        title = 'About'
        wx.MessageBox(msg, title, wx.OK | wx.ICON_INFORMATION)
