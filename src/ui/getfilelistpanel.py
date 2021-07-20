import os
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
        self.SetDropTarget(filedrop)
        self._initUi()

    def OnSetFilter(self, event):
        self.__on_set_filter()

    def __on_set_filter(self):
        self.filter = self.filterText.GetValue()
        filteredFileList = []
        if self.is_show_file_path:
            filteredFileList = self.doaction.getFilteredFileList(self.filter, self.on_update_progress_bar)
        else:
            filteredFileList = self.doaction.get_filtered_filelist_without_path(self.filter, self.on_update_progress_bar)
        self._printFileList(filteredFileList)

    def OnClearFilter(self, event):
        self.filterText.SetValue("")
        self.filter = []
        self._printFileList(self.doaction.getFileList())

    def __OnDrawFilterBox(self, sizer):
        filterBox = wx.BoxSizer(wx.HORIZONTAL)
        self.filterText = wx.TextCtrl(self,style = wx.TE_PROCESS_ENTER,size=(WINDOW_SIZE-BTN_SIZE*2,BTN_HEIGHT))
        self.filterText.Bind(wx.EVT_TEXT_ENTER, self.OnSetFilter)
        self.filterText.SetValue("")
        filterBox.Add(self.filterText, 1, wx.ALIGN_LEFT|wx.ALL, 1)

        clearBtnId = wx.NewId()
        clearBtn = wx.Button(self, clearBtnId, "Clear", size=(BTN_SIZE,30))
        clearBtn.Bind(wx.EVT_BUTTON, self.OnClearFilter)
        filterBox.Add(clearBtn, 0, wx.ALIGN_CENTRE|wx.LEFT, 1)

        sizer.Add(filterBox, 0, wx.ALIGN_LEFT, 5)

    def __OnDrawCtrlBox(self, sizer, font):
        fileListID = wx.NewId()
        self.fileList = wx.ListCtrl(self, fileListID,
                                    style=wx.LC_REPORT
                                 | wx.BORDER_NONE
                                 | wx.LC_EDIT_LABELS
                                    )
        self.sizer.Add(self.fileList, 1, wx.EXPAND)

        self.fileList.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
        self.fileList.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.__OnRClicked)
        self.fileList.InsertColumn(0, "No", width=40)
        self.fileList.InsertColumn(1, "File name", width=WINDOW_SIZE-60)
        self.fileList.SetFont(font)
        self.currentItem = -1

    def _initUi(self):
        font = wx.Font(12, wx.FONTFAMILY_TELETYPE, wx.NORMAL, wx.NORMAL)
    
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.__OnDrawFilterBox(self.sizer)
        self.__OnDrawCtrlBox(self.sizer, font)

        #self.text = wx.TextCtrl(self, style = wx.TE_PROCESS_ENTER|wx.TE_READONLY|wx.TE_MULTILINE, size=(WINDOW_SIZE,WINDOW_SIZE))
        #self.text.SetValue("")
        #self.text.SetFont(font)
        #self.text.Show(False)
        #self.sizer.Add(self.text, 0, wx.EXPAND)
        
        #btnBox = wx.BoxSizer(wx.HORIZONTAL)

        #clearBtnId = wx.NewId()
        #clearBtn = wx.Button(self, clearBtnId, "Clear", size=(50,30))
        #clearBtn.Bind(wx.EVT_BUTTON, self.OnClearBtn)
        #btnBox.Add(clearBtn, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        #BtnId = wx.NewId()
        #copyBtn = wx.Button(self, copyBtnId, "Copy", size=(50,30))
        #copyBtn.Bind(wx.EVT_BUTTON, self.OnCopyBtn)
        #btnBox.Add(copyBtn, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        #self.sizer.Add(btnBox, 0, wx.ALL, 1)

        statusBox = wx.BoxSizer(wx.HORIZONTAL)

        self.statusText = wx.TextCtrl(self, style = wx.TE_READONLY, size=(int(WINDOW_SIZE * 0.8), 30))
        self.statusText.SetValue("")
        self.statusText.SetFont(font)
        statusBox.Add(self.statusText, 1, wx.ALIGN_LEFT, 1)

        self.statusInfoText = wx.TextCtrl(self, style = wx.TE_READONLY, size=(int(WINDOW_SIZE * 0.2), 30))
        self.statusInfoText.SetValue("")
        self.statusInfoText.SetFont(font)
        statusBox.Add(self.statusInfoText, 1, wx.ALIGN_LEFT, 1)

        self.sizer.Add(statusBox, 0, wx.ALL, 1)

        self.SetSizer(self.sizer)
        self.SetAutoLayout(True)

    def OnCallback(self, filelist):
        self.progress_bar = wx.ProgressDialog("Load file list", "Please wait", maximum=100, parent=self, style=wx.PD_APP_MODAL | wx.PD_AUTO_HIDE)
        self.current_files = filelist
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
        #self._printFileList(checkFileList)

    def on_update_progress_bar(self, progress):
        if None == self.progress_bar:
            return
        self.progress_bar.Update(progress, str(progress) + "% done!")

    def _printFileList(self, files):
        print("_printFileList")
        #fileList = "\n".join(files)
        #fileList += "\n\nTotal: " + str(len(files))
        #self.text.SetValue(fileList)
        self.OnUpdateList(files)


    def OnReload(self):
        print("Reload")
        self.chosenItem = ""

        checkFileList = []
        if self.is_show_file_path:
            checkFileList = self.doaction.getFileList(self.current_files, self.filter)
        else:
            checkFileList = self.doaction.get_file_list_without_path(self.current_files, self.filter)

        self.OnUpdateList(checkFileList)


    def show_show_file_path(self, is_show_file_path):
        self.is_show_file_path = is_show_file_path
        self.__on_set_filter()


    def OnClearBtn(self, event):
        self.text.SetValue("")


    def OnCopyBtn(self, event):
        self.OnCopyToClipboard()


    def OnCopyToClipboard(self):
        if len(self.chosenItem) == 0:
            return

        chosenItemCount = self.fileList.GetSelectedItemCount()
        nextItem = self.fileList.GetFirstSelected()

        selectedItemList = []
        for _ in range(chosenItemCount):
            selectedItemList.append(self.fileList.GetItem(nextItem, 1).GetText())
            nextItem = self.fileList.GetNextItem(nextItem)

        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject('\n'.join(selectedItemList)))
            wx.TheClipboard.Close()


    def OnGetChooseFilePath(self):
        if self.fileList.GetItemCount() == 0:
            return "c:/"
        index = self.currentItem
        if index < 0:
            index = 0
        chosenItem = self.fileList.GetItem(index, 1).GetText()
        print(chosenItem)
        return fileutil.getPath(chosenItem)


    def OnGetChooseFile(self):
        if self.fileList.GetItemCount() == 0:
            return None
        index = self.currentItem
        if index < 0:
            index = 0
        chosenItem = self.fileList.GetItem(index, 1).GetText()
        # print(chosenItem)
        return chosenItem


    def OnItemSelected(self, event):
        self.currentItem = event.Index
        self._OnItemSelected(self.currentItem)


    def _OnItemSelected(self, index):
        self.chosenItem = ""
        if self.fileList.GetItemCount() == 0:
            self.logger.info("List is empty!")
            return
        if index < 0:
            index = 0
        self.chosenItem = self.fileList.GetItem(index, 1).GetText()
        #self.logger.info(str(index) + ':' + chosenItem)
        #print(self.chosenItem)
        self.OnUpdateFilename(str(index+1) + ": " + fileutil.get_filename(self.chosenItem))


    def __OnRClicked(self, event):
        print("__OnRClicked")
        self.currentItem = event.Index
        self._OnItemSelected(self.currentItem)
        if not os.path.exists(self.chosenItem):
            self.chosenItem = ""
            self.OnReload()
            return
        chosenItem = '"' + self.chosenItem + '"'
        os.startfile(chosenItem)


    def OnUpdateList(self, filelist):
        self.logger.info('.')
        self.fileList.DeleteAllItems()
        index = -1
        for file in filelist:
            index = self.fileList.InsertItem(self.fileList.GetItemCount(), 1)
            self.fileList.SetItem(index, 0, str(index+1))
            self.fileList.SetItem(index, 1, file)
            if index % 2 == 0:
                self.fileList.SetItemBackgroundColour(index, "Light blue")
            if index > 20000:
                err_msg = "Over than 20000"
                print(err_msg, len(filelist))
                self.statusText.SetValue(err_msg)
                break

        self.statusInfoText.SetValue("Count: " + str(index+1))


    def OnUpdateFilename(self, filename):
        self.statusText.SetValue(filename)

    def OnSaveAsExcel(self):
        self.doaction.OnSaveAsExcel()