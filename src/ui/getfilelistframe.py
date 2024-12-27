import wx
import os
from ui.getfilelistpanel import *
from ui.menu import *
from manager import ActionManager
import logging
import util.fileutil as fileutil

MAX_TAB_COUNT = 8
EMPTY_TAB_NAME = "__EMPTY__"

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
            self.notebook.AddPage(self.panel_manager[i].panel, EMPTY_TAB_NAME)
            self.tab_name.append(EMPTY_TAB_NAME)
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
        tab_count = min(len(tab_name), MAX_TAB_COUNT)
        for i in range(tab_count):
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

    def on_select_tab5(self, event):
        self.select_tab(5)

    def on_select_tab6(self, event):
        self.select_tab(6)

    def on_select_tab7(self, event):
        self.select_tab(7)

    def on_select_next_tab(self, event):
        current_tab = (self.notebook.GetSelection() + 1) % self.notebook.GetPageCount()
        self.select_tab(current_tab)

    def on_select_previous_tab(self, event):
        current_tab = (self.notebook.GetSelection() + self.notebook.GetPageCount() - 1) % self.notebook.GetPageCount()
        self.select_tab(current_tab)

    def on_append_folder(self, event):
        self.textPanel.on_append_folder(event)

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
        accel_tbl = []
        for item in self.init_key_map():
            self.Bind(wx.EVT_MENU, item['func'], id=(new_id := wx.NewIdRef()))
            accel_tbl.append((item["key"][0], item["key"][1], new_id))

        self.SetAcceleratorTable(wx.AcceleratorTable(accel_tbl))

    def init_key_map(self):
        key_map = []
        key_map.append({"key": (wx.ACCEL_ALT, ord('C')), "func": self._OnClearFilter})
        key_map.append({"key": (wx.ACCEL_ALT, ord('D')), "func": self._OnFocusFilter})
        key_map.append({"key": (wx.ACCEL_CTRL, ord('1')), "func": self.on_select_tab0})
        key_map.append({"key": (wx.ACCEL_CTRL, ord('2')), "func": self.on_select_tab1})
        key_map.append({"key": (wx.ACCEL_CTRL, ord('3')), "func": self.on_select_tab2})
        key_map.append({"key": (wx.ACCEL_CTRL, ord('4')), "func": self.on_select_tab3})
        key_map.append({"key": (wx.ACCEL_CTRL, ord('5')), "func": self.on_select_tab4})
        key_map.append({"key": (wx.ACCEL_CTRL, ord('6')), "func": self.on_select_tab5})
        key_map.append({"key": (wx.ACCEL_CTRL, ord('7')), "func": self.on_select_tab6})
        key_map.append({"key": (wx.ACCEL_CTRL, ord('8')), "func": self.on_select_tab7})
        key_map.append({"key": (wx.ACCEL_CTRL, ord('C')), "func": self.OnCopyToClipboard})
        key_map.append({"key": (wx.ACCEL_CTRL, ord('F')), "func": self._OnFocusFilter})
        key_map.append({"key": (wx.ACCEL_CTRL, ord('M')), "func": self._OnCtrl_M})
        key_map.append({"key": (wx.ACCEL_CTRL, ord('L')), "func": self.on_display_file_size})
        key_map.append({"key": (wx.ACCEL_CTRL, ord('O')), "func": self._OnCtrl_O})
        key_map.append({"key": (wx.ACCEL_CTRL, ord('P')), "func": self._OnCtrl_P})
        key_map.append({"key": (wx.ACCEL_CTRL, ord('T')), "func": self.on_select_next_tab})
        key_map.append({"key": (wx.ACCEL_CTRL, ord('Q')), "func": self.OnQuit})
        key_map.append({"key": (wx.ACCEL_CTRL | wx.ACCEL_ALT, ord('D')), "func": self._OnCtrl_D})
        key_map.append({"key": (wx.ACCEL_CTRL | wx.ACCEL_SHIFT, ord('L')), "func": self.on_reload})
        key_map.append({"key": (wx.ACCEL_CTRL | wx.ACCEL_SHIFT, ord('T')), "func": self.on_select_previous_tab})
        key_map.append({"key": (wx.ACCEL_CTRL | wx.ACCEL_SHIFT, ord('V')), "func": self.on_append_folder})
        key_map.append({"key": (wx.ACCEL_SHIFT, wx.WXK_F6), "func": self._on_rename})
        return key_map

    def OnQuit(self, event):
        self.Close()

    def OnSaveAsExcel(self, event):
        self.textPanel.OnSaveAsExcel()

    def on_reload(self, event):
        self.textPanel.on_reload()

    def OnCopyToClipboard(self, event):
        self.textPanel.OnCopyToClipboard()

    def _OnCtrl_D(self, event):
        filename = self.textPanel.OnGetChooseFile()
        if filename is None:
            return

        title = 'Do you want to delete'
        msg = '> ' + filename

        ask_delete_dialog = wx.MessageDialog(None, msg, title, wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        if ask_delete_dialog.ShowModal() == wx.ID_YES:
            self.action.on_run_command("delete", filename)
            self.textPanel.on_reload()
        ask_delete_dialog.Destroy()

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
            self.textPanel.on_reload()

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
        msg = f'\n{file_name_only}\n'

        if file_size > 1000 * 1000 * 1000:
            msg += f'\n{file_size / (1000 * 1000 * 1000):,.2f} GB\n'

        msg += f'\n{file_size / (1000 * 1000):,.1f} MB\n\n' \
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
        if self.tab_name[tab_idx] != tab_name:
            if len(tab_name) > 25:
                tab_name = tab_name[:22] + "..."
            self.tab_name[tab_idx] = tab_name
            fileutil.save_tab_name(self.tab_name, "./tab_name.cfg")
        self.notebook.SetPageText(tab_idx, tab_name)