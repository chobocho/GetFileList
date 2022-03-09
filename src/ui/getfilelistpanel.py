import os
import wx

from util.filedrop import *
from action.doaction import *
import logging
import subprocess
import util.fileutil as fileutil


WINDOW_SIZE = 800
BTN_SIZE = 50
BTN_HEIGHT = 30


class GetFileListPanel(wx.Panel):
    def __init__(self, *args, **kw):
        super(GetFileListPanel, self).__init__(*args, **kw)
        filedrop = FileDrop(self)
        self.logger = logging.getLogger('getfilelist')
        self.doaction = DoAction()
        self.filter = []
        self.filelist = []
        self.current_files = []
        self.chosenItem = ""
        self.currentItem = -1
        self.is_show_file_path = True
        self.is_show_foler_info = True
        self.is_save_folder_info = True
        self.progress_bar = None
        self.SetDropTarget(filedrop)
        self._initUi()

    def on_set_filter(self, event):
        self.__on_set_filter()

    def __on_set_filter(self):
        self.filter = self.filter_text.GetValue()
        filtered_file_list = []
        if self.is_show_file_path:
            filtered_file_list = self.doaction.getFilteredFileList(self.filter, self.on_update_progress_bar)
        else:
            filtered_file_list = self.doaction.get_filtered_filelist_without_path(self.filter,
                                                                                self.on_update_progress_bar)
        self._printFileList(filtered_file_list)

    def _on_clear_filter(self, event):
        self.OnClearFilter()

    def OnClearFilter(self):
        self.filter_text.SetValue("")
        self.filter = []
        self._printFileList(self.doaction.getFileList())

    def _on_draw_fold_info_box(self, sizer):
        folderInfoBox = wx.BoxSizer(wx.HORIZONTAL)
        self.folderInfoText = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(WINDOW_SIZE-BTN_SIZE*2, BTN_HEIGHT*2))
        self.folderInfoText.SetValue("")
        folderInfoBox.Add(self.folderInfoText, 1, wx.EXPAND, 1)

        addFolderBtnId = wx.NewId()
        self.addFolderBtn = wx.Button(self, addFolderBtnId, "&Add", size=(BTN_SIZE, 30))
        self.addFolderBtn.Bind(wx.EVT_BUTTON, self._OnAddFolder)
        folderInfoBox.Add(self.addFolderBtn, 0, wx.ALIGN_CENTRE | wx.LEFT, 1)

        resetBtnId = wx.NewId()
        self.resetBtn = wx.Button(self, resetBtnId, "&Reset", size=(BTN_SIZE, 30))
        self.resetBtn.Bind(wx.EVT_BUTTON, self._OnReset)
        folderInfoBox.Add(self.resetBtn, 0, wx.ALIGN_CENTRE | wx.LEFT, 1)

        sizer.Add(folderInfoBox, 0, wx.EXPAND, 1)

    def _on_draw_filter_box(self, sizer):
        filter_box = wx.BoxSizer(wx.HORIZONTAL)
        self.filter_text = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER, size=(WINDOW_SIZE - BTN_SIZE, BTN_HEIGHT))
        self.filter_text.Bind(wx.EVT_TEXT_ENTER, self.on_set_filter)
        self.filter_text.SetValue("")
        self.filter_text.SetHint("Alt+D: Focus here! / Alt+C: Clear here!")
        filter_box.Add(self.filter_text, 1, wx.EXPAND, 1)

        clear_btn_id = wx.NewId()
        clear_btn = wx.Button(self, clear_btn_id, "&Clear", size=(BTN_SIZE, 30))
        clear_btn.Bind(wx.EVT_BUTTON, self._on_clear_filter)
        filter_box.Add(clear_btn, 0, wx.ALIGN_CENTRE | wx.LEFT, 1)

        sizer.Add(filter_box, 0, wx.EXPAND, 1)

    def __OnDrawCtrlBox(self, sizer, font):
        fileListID = wx.NewId()
        self.file_list_ctrl = wx.ListCtrl(self, fileListID,
                                          style=wx.LC_REPORT
                                          | wx.BORDER_NONE
                                          | wx.LC_EDIT_LABELS
                                          )
        self.sizer.Add(self.file_list_ctrl, 1, wx.EXPAND)

        self.file_list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
        self.file_list_ctrl.Bind(wx.EVT_LEFT_DCLICK, self.__OnDoubleClicked)
        self.file_list_ctrl.InsertColumn(0, "No", width=40)
        self.file_list_ctrl.InsertColumn(1, "File name", width=WINDOW_SIZE - 60)
        self.file_list_ctrl.SetFont(font)
        self.currentItem = -1

    def _initUi(self):
        font = wx.Font(12, wx.FONTFAMILY_TELETYPE, wx.NORMAL, wx.NORMAL)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self._on_draw_fold_info_box(self.sizer)
        self._on_draw_filter_box(self.sizer)
        self.__OnDrawCtrlBox(self.sizer, font)

        statusBox = wx.BoxSizer(wx.HORIZONTAL)

        self.statusText = wx.TextCtrl(self, style=wx.TE_READONLY, size=(int(WINDOW_SIZE * 0.8), 30))
        self.statusText.SetValue("")
        self.statusText.SetFont(font)
        statusBox.Add(self.statusText, 1, wx.ALIGN_LEFT, 1)

        self.statusInfoText = wx.TextCtrl(self, style=wx.TE_READONLY, size=(int(WINDOW_SIZE * 0.2), 30))
        self.statusInfoText.SetValue("")
        self.statusInfoText.SetFont(font)
        statusBox.Add(self.statusInfoText, 1, wx.ALIGN_LEFT, 1)

        self.sizer.Add(statusBox, 0, wx.ALL, 1)

        self.SetSizer(self.sizer)
        self.SetAutoLayout(True)

    def OnCallback(self, filelist):
        self.progress_bar = wx.ProgressDialog("Load file list", "Please wait", maximum=100, parent=self,
                                              style=wx.PD_APP_MODAL | wx.PD_AUTO_HIDE)
        self.current_files = filelist
        self.update_folder_info()
        checkFileList = []
        if self.is_show_file_path:
            checkFileList = self.doaction.getFileList(filelist, self.filter, self.on_update_progress_bar)
        else:
            checkFileList = self.doaction.get_file_list_without_path(filelist, self.filter, self.on_update_progress_bar)

        self.on_update_progress_bar(99)
        self.OnUpdateList(checkFileList)
        self.on_update_progress_bar(100)
        self.progress_bar.Destroy()
        self.progress_bar = None
        # self._printFileList(checkFileList)
        self.on_save_current_folder()

    def on_save_current_folder(self):
        self.logger.info(".")
        if not self.is_save_folder_info:
            self.logger.info(f'Save option : {self.is_save_folder_info}')
            fileutil.save_cfg([], "./getfilelist.cfg")
        else:
            fileutil.save_cfg(self.current_files, "./getfilelist.cfg")

    def on_update_progress_bar(self, progress):
        if self.progress_bar is None:
            return
        self.progress_bar.Update(progress, str(progress) + "% done!")

    def _printFileList(self, files):
        print("_printFileList")
        # fileList = "\n".join(files)
        # fileList += "\n\nTotal: " + str(len(files))
        # self.text.SetValue(fileList)
        self.OnUpdateList(files)

    def OnReload(self):
        print("Reload")
        self.chosenItem = ""

        check_file_list = []
        if self.is_show_file_path:
            check_file_list = self.doaction.getFileList(self.current_files, self.filter)
        else:
            check_file_list = self.doaction.get_file_list_without_path(self.current_files, self.filter)

        self.OnUpdateList(check_file_list)

    def show_file_path(self, is_show_file_path):
        self.is_show_file_path = is_show_file_path
        self.__on_set_filter()

    def show_folder_info(self, is_show_foler_info):
        self.is_show_foler_info = is_show_foler_info
        if self.is_show_foler_info:
            self.folderInfoText.Show()
            self.addFolderBtn.Show()
            self.resetBtn.Show()
        else:
            self.folderInfoText.Hide()
            self.addFolderBtn.Hide()
            self.resetBtn.Hide()
        self.Layout()

    def OnClearBtn(self, event):
        self.text.SetValue("")

    def OnCopyBtn(self, event):
        self.OnCopyToClipboard()

    def OnCopyToClipboard(self):
        if len(self.chosenItem) == 0:
            return

        chosenItemCount = self.file_list_ctrl.GetSelectedItemCount()
        nextItem = self.file_list_ctrl.GetFirstSelected()

        selectedItemList = []
        for _ in range(chosenItemCount):
            selectedItemList.append(self.file_list_ctrl.GetItem(nextItem, 1).GetText())
            nextItem = self.file_list_ctrl.GetNextItem(nextItem)

        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject('\n'.join(selectedItemList)))
            wx.TheClipboard.Close()

    def OnGetChooseFilePath(self):
        if self.file_list_ctrl.GetItemCount() == 0:
            return "c:/"
        index = self.currentItem
        if index < 0:
            index = 0
        chosenItem = self.file_list_ctrl.GetItem(index, 1).GetText()
        print(chosenItem)
        return fileutil.getPath(chosenItem)

    def OnGetChooseFile(self):
        if self.file_list_ctrl.GetItemCount() == 0:
            return None
        index = self.currentItem
        if index < 0:
            index = 0
        chosenItem = self.file_list_ctrl.GetItem(index, 1).GetText()
        # print(chosenItem)
        return chosenItem

    def OnItemSelected(self, event):
        self.currentItem = event.Index
        self._OnItemSelected(self.currentItem)

    def _OnItemSelected(self, index):
        self.chosenItem = ""
        if self.file_list_ctrl.GetItemCount() == 0:
            self.logger.info("List is empty!")
            return
        if index < 0:
            index = 0
        self.chosenItem = self.file_list_ctrl.GetItem(index, 1).GetText()
        # self.logger.info(str(index) + ':' + chosenItem)
        # print(self.chosenItem)
        self.OnUpdateFilename(str(index + 1) + ": " + fileutil.get_filename(self.chosenItem))

    def __OnDoubleClicked(self, event):
        print("__OnDoubleClicked")
        if self.file_list_ctrl.GetItemCount() == 0:
            return

        if (self.currentItem < 0) or (self.currentItem >= self.file_list_ctrl.GetItemCount()):
            return

        self._OnItemSelected(self.currentItem)
        if not os.path.exists(self.chosenItem):
            self.chosenItem = ""
            self.OnReload()
            return
        chosenItem = '"' + self.chosenItem + '"'
        os.startfile(chosenItem)

    def OnUpdateList(self, filelist):
        self.logger.info(len(filelist))
        self.file_list_ctrl.DeleteAllItems()
        index = -1
        for file in filelist:
            index = self.file_list_ctrl.InsertItem(self.file_list_ctrl.GetItemCount(), 1)
            self.file_list_ctrl.SetItem(index, 0, str(index + 1))
            self.file_list_ctrl.SetItem(index, 1, file)
            if index % 2 == 0:
                self.file_list_ctrl.SetItemBackgroundColour(index, "Light blue")
            if index > 20000:
                err_msg = "Over than 20000"
                print(err_msg, len(filelist))
                self.statusText.SetValue(err_msg)
                break

        self.statusInfoText.SetValue("Count: " + str(index + 1))

    def OnUpdateFilename(self, filename):
        self.statusText.SetValue(filename)

    def OnSaveAsExcel(self):
        self.doaction.OnSaveAsExcel()

    def OnFocusFilter(self):
        self.filter_text.SetFocus()

    def update_folder_info(self):
        self.folderInfoText.SetValue('\n'.join(self.current_files))

    def save_folder_info(self, is_save_folder_info):
        self.is_save_folder_info = is_save_folder_info
        self.logger.info(self.is_save_folder_info)

    def _OnReset(self, event):
        self.OnCallback([])
        self.doaction.OnReset()

    def _OnAddFolder(self, event):
        newFolder = ""
        dlg = wx.DirDialog (None, "Choose directory", "",
                            wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            newFolder = dlg.GetPath()
        dlg.Destroy()

        if len(newFolder) == 0:
            return

        if newFolder in self.current_files:
            return

        self.current_files.append(newFolder)
        self.OnCallback(self.current_files)

