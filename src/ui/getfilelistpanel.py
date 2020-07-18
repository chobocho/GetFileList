import os
from util.filedrop import *
from action.doaction import *
import logging
import subprocess

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
        filterBox.Add(self.filterText, 1, wx.ALIGN_CENTRE|wx.ALL, 1)

        clearBtnId = wx.NewId()
        clearBtn = wx.Button(self, clearBtnId, "Clear", size=(BTN_SIZE,30))
        clearBtn.Bind(wx.EVT_BUTTON, self.OnClearFilter)
        filterBox.Add(clearBtn, 0, wx.ALIGN_CENTRE|wx.LEFT, 1)

        sizer.Add(filterBox, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

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
        self.sizer.Add(self.text, 1, wx.EXPAND)
        
        btnBox = wx.BoxSizer(wx.HORIZONTAL)

        clearBtnId = wx.NewId()
        clearBtn = wx.Button(self, clearBtnId, "Clear", size=(50,30))
        clearBtn.Bind(wx.EVT_BUTTON, self.OnClearBtn)
        btnBox.Add(clearBtn, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        copyBtnId = wx.NewId()
        copyBtn = wx.Button(self, copyBtnId, "Copy", size=(50,30))
        copyBtn.Bind(wx.EVT_BUTTON, self.OnCopyBtn)
        btnBox.Add(copyBtn, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.sizer.Add(btnBox, 0, wx.ALIGN_CENTER_VERTICAL, 5)
        self.SetSizer(self.sizer)
        self.SetAutoLayout(True)

    def OnCallback(self, filelist):
        checkFileList = self.doaction.getFileList(filelist, self.filter)
        self.OnUpdateList(checkFileList)
        #self._printFileList(checkFileList)

    def _printFileList(self, files):
        print("_printFileList")
        #fileList = "\n".join(files)
        #fileList += "\n\nTotal: " + str(len(files))
        #self.text.SetValue(fileList)
        self.OnUpdateList(files)

    def OnClearBtn(self, event):
        self.text.SetValue("")
        
    def OnCopyBtn(self, event):
        toCopyData = self.text.GetValue()
        
        if len(toCopyData) == 0:
            return 
            
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject(toCopyData))
            wx.TheClipboard.Close()

    def OnFindSameSize(self):
        sameSizeFileList = self.doaction.getSameSizefileList()

        fileList = []
        count = 0
        for files in sameSizeFileList:
            if count > 0:
                fileList.append("------------------------")
            fileList.append(self.GetSize(files))
            for f in sameSizeFileList[files]:
                fileList.append(f)
                count += 1

        fileList.append("\n\nTotal: " + str(count))
        self.text.SetValue("\n".join(fileList))

    def OnFindDuplicate(self):
        duplicateFileList = self.doaction.getDuplicatefileList()
        fileList = []
        count = 0
        for files in duplicateFileList:
            if count > 0:
                fileList.append("------------------------")
            fileList.append(self.GetSize(files))
            for f in duplicateFileList[files]:
                fileList.append(f)
                count += 1

        fileList.append("\n\nTotal: " + str(count))
        self.text.SetValue("\n".join(fileList))

    def GetSize(self, s):
        _1K = 1024
        _1M = 1048576

        if s < _1K:
            return str(s) + "B"
        if s < _1M:
            return str(int(s/_1K)) + "K = " + str(s) + "B"
        return str(int(s/_1M)) + "M = " + str(s) + "B"

    def OnItemSelected(self, event):
        self.currentItem = event.Index

    def _OnItemSelected(self, index):
        if self.fileList.GetItemCount() == 0:
            self.logger.info("List is empty!")
            return
        if index < 0:
            index = 0
        chosenItem = self.fileList.GetItem(index, 1).GetText()
        #self.logger.info(str(index) + ':' + chosenItem)
        print(chosenItem)
        chosenItem = '"' + chosenItem + '"'
        os.startfile(chosenItem)

    def __OnRClicked(self, event):
        print("__OnRClicked")
        self.currentItem = event.Index
        self._OnItemSelected(self.currentItem)

    def OnUpdateList(self, filelist):
        self.logger.info('.')
        self.fileList.DeleteAllItems()
        for file in filelist:
            index = self.fileList.InsertItem(self.fileList.GetItemCount(), 1)
            self.fileList.SetItem(index, 0, str(index))
            self.fileList.SetItem(index, 1, file)
            if index % 2 == 0:
                self.fileList.SetItemBackgroundColour(index, "Light blue")