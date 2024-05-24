import wx
from ui.getfilelistpanel import *
from ui.menu import *
from manager import ActionManager
import logging

class GetFileListFrame(wx.Frame):
    def __init__(self, *args, version, **kw):
        super(GetFileListFrame, self).__init__(*args, **kw)
        self.logger = logging.getLogger('getfilelist')
        self.textPanel = GetFileListPanel(self)
        self.version = version
        self.action = ActionManager.ActionManager()

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.textPanel, 1, wx.EXPAND)

        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        self._addMenubar()
        self._addShortKey()
        self.on_load_previous_folder_info()

    def _addMenubar(self):
        self.menu = GetFileListMenu(self)

    def _addShortKey(self):
        ctrl_C_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self.OnCopyToClipboard, id=ctrl_C_Id)

        ctrl_D_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self._OnCtrl_D, id=ctrl_D_Id)

        ctrl_H_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self._OnCtrl_H, id=ctrl_H_Id)

        ctrl_M_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self._OnCtrl_M, id=ctrl_M_Id)

        ctrl_O_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self._OnCtrl_O, id=ctrl_O_Id)

        ctrl_P_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self._OnCtrl_P, id=ctrl_P_Id)

        ctrl_Q_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self.OnQuit, id=ctrl_Q_Id)

        focus_on_search_box_id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self._OnFocusFilter, id=focus_on_search_box_id)

        alt_C_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self._OnClearFilter, id=alt_C_Id)

        accel_tbl = wx.AcceleratorTable([
            (wx.ACCEL_ALT, ord('C'), alt_C_Id),
            (wx.ACCEL_ALT, ord('D'), focus_on_search_box_id),
            (wx.ACCEL_CTRL, ord('C'), ctrl_C_Id),
            (wx.ACCEL_CTRL, ord('D'), ctrl_D_Id),
            (wx.ACCEL_CTRL, ord('F'), focus_on_search_box_id),
            (wx.ACCEL_CTRL, ord('H'), ctrl_H_Id),
            (wx.ACCEL_CTRL, ord('M'), ctrl_M_Id),
            (wx.ACCEL_CTRL, ord('O'), ctrl_O_Id),
            (wx.ACCEL_CTRL, ord('P'), ctrl_P_Id),
            (wx.ACCEL_CTRL, ord('Q'), ctrl_Q_Id)
        ])
        self.SetAcceleratorTable(accel_tbl)

    def OnQuit(self, event):
        self.Close()

    def OnSaveAsExcel(self, event):
        self.textPanel.OnSaveAsExcel()

    def OnReload(self, event):
        self.textPanel.OnReload()

    def OnCopyToClipboard(self, event):
        self.textPanel.OnCopyToClipboard()

    def _OnCtrl_D(self, event):
        filename = self.textPanel.OnGetChooseFile()
        if filename == None:
            return

        title = 'Do you want to delete'
        msg = '> ' + filename

        askDeleteDialog = wx.MessageDialog(None, msg, title, wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        if askDeleteDialog.ShowModal() == wx.ID_YES:
            self.action.on_run_command("delete", filename)
            self.textPanel.OnReload()
        askDeleteDialog.Destroy()

    def _OnCtrl_H(self, event):
        self.menu.toggle_show_menu()
        self.textPanel.show_file_path(self.menu.is_show_menu())

    def _OnCtrl_M(self, event):
        self.action.on_run_command("ctrl_m")

    def _OnCtrl_O(self, event):
        path = self.textPanel.OnGetChooseFilePath()
        self.action.on_run_command("explore", path)

    def _OnCtrl_P(self, event):
        self.action.on_run_command("ctrl_p")

    def _OnFocusFilter(self, event):
        self.textPanel.OnFocusFilter()

    def _OnClearFilter(self, event):
        self.textPanel.OnClearFilter()

    def OnAbout(self, event):
        msg = self.version + '\nhttp://chobocho.com'
        title = 'About'
        wx.MessageBox(msg, title, wx.OK | wx.ICON_INFORMATION)

    def on_show_file_path(self, event):
        self.textPanel.show_file_path(self.menu.is_show_menu())

    def on_show_folder_info(self, event):
        self.textPanel.show_folder_info(self.menu.is_show_folder_info_menu())

    def on_load_previous_folder_info(self):
        self.logger.info(".")
        filelist = fileutil.load_cfg("./getfilelist.cfg")
        if len(filelist) > 0:
            self.textPanel.OnCallback(filelist)

    def save_foler_info(self, event):
        self.textPanel.save_folder_info(self.menu.is_save_folder_info_menu())