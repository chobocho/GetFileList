import wx
import os
from ui.getfilelistpanel import *
from ui.menu import *
from manager import ActionManager
import logging

from src.util import fileutil

MAX_TAB_COUNT = 5

class PanelManager:
    def __init__(self, parent, tab_idx, frame=None):
        self.panel = GetFileListPanel(parent, tab_idx=tab_idx, frame=frame)
        self.action = ActionManager.ActionManager()


class GetFileListFrame(wx.Frame):
    def __init__(self, *args, version, **kw):
        super(GetFileListFrame, self).__init__(*args, **kw)
        self.logger = logging.getLogger('getfilelist')
        self.notebook = wx.Notebook(self)
        self.notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.on_change_tab)
        self.panel_manager = []
        self.tab_name = []
        for i in range(MAX_TAB_COUNT):
            self.panel_manager.append(PanelManager(self.notebook, tab_idx=i, frame=self))
            self.notebook.AddPage(self.panel_manager[i].panel, "_EMPTY_")
            self.tab_name.append("_EMPTY_")
        self.textPanel = self.panel_manager[0].panel
        self.action = self.panel_manager[0].action
        self.version = version

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.notebook, 1, wx.EXPAND)

        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        self._add_menubar()
        self._addShortKey()

        tab_name = fileutil.load_tab_name("./tab_name.cfg")
        if len(tab_name) == 5:
            for i in range(self.notebook.GetPageCount()):
                self.notebook.SetPageText(i, tab_name[i])
                self.tab_name[i] = tab_name[i]

        self.on_load_previous_folder_info()

    def on_change_tab(self, event):
        self.select_tab(event.GetSelection())

    def on_select_tab0(self, event):
        self.select_tab(0)

    def on_select_tab1(self, event):
        self.select_tab(1)

    def on_select_tab2(self, event):
        self.select_tab(2)

    def on_select_tab3(self, event):
        self.select_tab(3)

    def on_select_tab4(self, event):
        self.select_tab(4)

    def on_select_next_tab(self, event):
        current_tab = (self.notebook.GetSelection() + 1) % self.notebook.GetPageCount()
        self.select_tab(current_tab)

    def select_tab(self, tab_idx):
        self.notebook.SetSelection(tab_idx)
        self.textPanel = self.panel_manager[tab_idx].panel
        self.action = self.panel_manager[tab_idx].action

        if self.textPanel.show_folder_info_menu() != self.menu.is_show_folder_info_menu():
            self.menu.toggle_show_folder_info_menu()

        if self.textPanel.load_folder_info() is False:
            self.on_load_previous_folder_info(tab_idx)

    def _add_menubar(self):
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
        self.Bind(wx.EVT_MENU, self.on_select_tab0, id=(select_tab0 := wx.NewIdRef()))
        self.Bind(wx.EVT_MENU, self.on_select_tab1, id=(select_tab1 := wx.NewIdRef()))
        self.Bind(wx.EVT_MENU, self.on_select_tab2, id=(select_tab2 := wx.NewIdRef()))
        self.Bind(wx.EVT_MENU, self.on_select_tab3, id=(select_tab3 := wx.NewIdRef()))
        self.Bind(wx.EVT_MENU, self.on_select_tab4, id=(select_tab4 := wx.NewIdRef()))
        self.Bind(wx.EVT_MENU, self.on_select_next_tab, id=(select_next_tab := wx.NewIdRef()))

        accel_tbl = wx.AcceleratorTable([
            (wx.ACCEL_ALT, ord('C'), alt_C_Id),
            (wx.ACCEL_ALT, ord('D'), focus_on_search_box_id),
            (wx.ACCEL_CTRL, ord('1'), select_tab0),
            (wx.ACCEL_CTRL, ord('2'), select_tab1),
            (wx.ACCEL_CTRL, ord('3'), select_tab2),
            (wx.ACCEL_CTRL, ord('4'), select_tab3),
            (wx.ACCEL_CTRL, ord('5'), select_tab4),
            (wx.ACCEL_CTRL, ord('C'), ctrl_C_Id),
            (wx.ACCEL_CTRL, ord('F'), focus_on_search_box_id),
            (wx.ACCEL_CTRL, ord('M'), ctrl_M_Id),
            (wx.ACCEL_CTRL, ord('L'), display_file_size_id),
            (wx.ACCEL_CTRL, ord('O'), ctrl_O_Id),
            (wx.ACCEL_CTRL, ord('P'), ctrl_P_Id),
            (wx.ACCEL_CTRL, ord('T'), select_next_tab),
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

    def on_load_previous_folder_info(self, tab_idx=0):
        self.logger.info(".")
        filelist = fileutil.load_cfg(f"./getfilelist{tab_idx}.cfg")
        if len(filelist) > 0:
            self.textPanel.OnCallback(filelist)

    def save_folder_info(self, event):
        self.textPanel.save_folder_info(self.menu.is_save_folder_info_menu())

    def update_notebook(self, tab_idx, tab_name):
        self.notebook.SetPageText(tab_idx, tab_name)
        if self.tab_name[tab_idx] != tab_name:
            self.tab_name[tab_idx] = tab_name
            fileutil.save_tab_name(self.tab_name, "./tab_name.cfg")
