import wx
import os
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
        self.Bind(wx.EVT_MENU, self.OnCopyToClipboard, id=(ctrl_C_Id := wx.NewIdRef()))
        self.Bind(wx.EVT_MENU, self._OnCtrl_D, id=(ctrl_D_Id := wx.NewIdRef()))
        self.Bind(wx.EVT_MENU, self._OnCtrl_M, id=(ctrl_M_Id := wx.NewIdRef()))
        self.Bind(wx.EVT_MENU, self._OnCtrl_O, id=(ctrl_O_Id := wx.NewIdRef()))
        self.Bind(wx.EVT_MENU, self._OnCtrl_P, id=(ctrl_P_Id := wx.NewIdRef()))
        self.Bind(wx.EVT_MENU, self.OnQuit, id=(ctrl_Q_Id := wx.NewIdRef()))
        self.Bind(wx.EVT_MENU, self._on_rename, id=(rename_id := wx.NewIdRef()))
        self.Bind(wx.EVT_MENU, self._OnFocusFilter, id=(focus_on_search_box_id := wx.NewIdRef()))
        self.Bind(wx.EVT_MENU, self._OnClearFilter, id=(alt_C_Id := wx.NewIdRef()))
        self.Bind(wx.EVT_MENU, self.on_display_file_size, id=(display_file_size_id := wx.NewIdRef()))

        accel_tbl = wx.AcceleratorTable([
            (wx.ACCEL_ALT, ord('C'), alt_C_Id),
            (wx.ACCEL_ALT, ord('D'), focus_on_search_box_id),
            (wx.ACCEL_CTRL, ord('C'), ctrl_C_Id),
            (wx.ACCEL_CTRL, ord('F'), focus_on_search_box_id),
            (wx.ACCEL_CTRL, ord('M'), ctrl_M_Id),
            (wx.ACCEL_CTRL, ord('L'), display_file_size_id),
            (wx.ACCEL_CTRL, ord('O'), ctrl_O_Id),
            (wx.ACCEL_CTRL, ord('P'), ctrl_P_Id),
            (wx.ACCEL_CTRL, ord('Q'), ctrl_Q_Id),
            (wx.ACCEL_CTRL | wx.ACCEL_ALT, ord('D'), ctrl_D_Id),
            (wx.ACCEL_SHIFT, wx.WXK_F6, rename_id)
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
        if filename is None:
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

    def _on_rename(self, event):
        file_name = self.textPanel.OnGetChooseFile()
        file_path = self.textPanel.OnGetChooseFilePath()
        if file_name is None or file_path is None:
            return

        title = 'Input new file name'
        file_name_only = os.path.basename(file_name)
        msg = f'{file_path}\\\n  {file_name_only}'

        rename_dialog = wx.TextEntryDialog(None, msg, title, style = wx.OK|wx.CANCEL)
        rename_dialog.SetValue(file_name_only)
        rename_dialog.SetMaxLength(128)
        new_file_name = ""
        if rename_dialog.ShowModal() == wx.ID_OK:
            new_file_name = rename_dialog.GetValue()
        rename_dialog.Destroy()

        if len(new_file_name) == 0:
            return
        if self.action.on_rename(file_name, os.path.join(file_path, new_file_name)):
            self.textPanel.OnReload()

    def _OnFocusFilter(self, event):
        self.textPanel.OnFocusFilter()

    def _OnClearFilter(self, event):
        self.textPanel.on_clear_filter()

    def on_display_file_size(self, event):
        file_name = self.textPanel.OnGetChooseFile()
        file_path = self.textPanel.OnGetChooseFilePath()

        if file_name is None or file_path is None:
            return

        title = file_path
        file_name_only = os.path.basename(file_name)

        file_size = os.path.getsize(file_name)
        msg = f'\n{file_name_only}\n\n' \
              f'{file_size / (1000 * 1000 * 1000):,.2f} GB\n' \
              f'\n{file_size / (1000 * 1000):,.1f} MB\n\n' \
              f'{file_size // 1000:,} KB\n' \
              f'{file_size:,} Bytes\n'
        wx.MessageBox(msg, title, wx.OK | wx.ICON_INFORMATION)

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