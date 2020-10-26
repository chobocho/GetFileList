import wx
from ui.getfilelistpanel import *
from ui.menu import *
from manager import ActionManager

class GetFileListFrame(wx.Frame):
    def __init__(self, *args, version, **kw):
        super(GetFileListFrame, self).__init__(*args, **kw)
        self.textPanel = GetFileListPanel(self)
        self.version = version
        self.action = ActionManager.ActionManager()
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.textPanel, 1, wx.EXPAND)

        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        self._addMenubar()
        self._addShortKey()

    def _addMenubar(self):
        self.menu = GetFileListMenu(self)

    def _addShortKey(self):
        ctrl_D_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self._OnCtrl_D, id=ctrl_D_Id)

        ctrl_M_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self._OnCtrl_M, id=ctrl_M_Id)

        ctrl_P_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self._OnCtrl_P, id=ctrl_P_Id)

        ctrl_Q_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self.OnQuit, id=ctrl_Q_Id)

        accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CTRL, ord('D'), ctrl_D_Id),
                                         (wx.ACCEL_CTRL, ord('M'), ctrl_M_Id),
                                         (wx.ACCEL_CTRL, ord('P'), ctrl_P_Id),
                                         (wx.ACCEL_CTRL, ord('Q'), ctrl_Q_Id)])
        self.SetAcceleratorTable(accel_tbl)

    def OnQuit(self, event):
        self.Close()

    def _OnCtrl_D(self, event):
        path = self.textPanel.OnGetChooseFilePath()
        self.action.OnRunCommand("explore", path)

    def _OnCtrl_M(self, event):
        self.action.OnRunCommand("ctrl_m")

    def _OnCtrl_P(self, event):
        self.action.OnRunCommand("ctrl_p")

    def OnAbout(self, event):
        msg = self.version + '\nhttp://chobocho.com'
        title = 'About'
        wx.MessageBox(msg, title, wx.OK | wx.ICON_INFORMATION)



