import os
from util.filedrop import *
from action.doaction import *
import logging
import subprocess
import util.fileutil as fileutil

WINDOW_SIZE = 640
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
        self.SetDropTarget(filedrop)
        self._initUi()

    def OnSetFilter(self, event):
        self.filter = self.filterText.GetValue()
        filteredFileList = self.doaction.getFilteredFileList(self.filter)
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

        self.text = wx.TextCtrl(self, style = wx.TE_PROCESS_ENTER|wx.TE_READONLY|wx.TE_MULTILINE, size=(WINDOW_SIZE,WINDOW_SIZE))
        self.text.SetValue("")
        self.text.SetFont(font)
        self.text.Show(False)
        self.sizer.Add(self.text, 0, wx.EXPAND)
        
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
        self.SetSizer(self.sizer)
        self.SetAutoLayout(True)

    def OnCallback(self, filelist):
        self.current_files = filelist
        checkFileList = self.doaction.getFileList(filelist, self.filter)
        self.OnUpdateList(checkFileList)
        #self._printFileList(checkFileList)

    def _printFileList(self, files):
        print("_printFileList")
        #fileList = "\n".join(files)
        #fileList += "\n\nTotal: " + str(len(files))
        #self.text.SetValue(fileList)
        self.OnUpdateList(files)

    def OnReload(self):
        print("Reload")
        self.chosenItem = ""
        checkFileList = self.doaction.getFileList(self.current_files, self.filter)
        self.OnUpdateList(checkFileList)

    def OnClearBtn(self, event):
        self.text.SetValue("")
        
    def OnCopyBtn(self, event):
        self.OnCopyToClipboard()

    def OnCopyToClipboard(self):
        if len(self.chosenItem) == 0:
            return

        print("C2C: " + self.chosenItem)
            
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject(self.chosenItem))
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
        print(self.chosenItem)

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
        for file in filelist:
            index = self.fileList.InsertItem(self.fileList.GetItemCount(), 1)
            self.fileList.SetItem(index, 0, str(index))
            self.fileList.SetItem(index, 1, file)
            if index % 2 == 0:
                self.fileList.SetItemBackgroundColour(index, "Light blue")
            if index > 10000:
                print("Over than 10000", len(filelist))
                break