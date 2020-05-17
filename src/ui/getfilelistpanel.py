import wx
from util.filedrop import *
from action.doaction import *

WINDOW_SIZE = 480
BTN_SIZE = 50
BTN_HEIGHT = 30

class GetFileListPanel(wx.Panel):
    def __init__(self, *args, **kw):
        super(GetFileListPanel, self).__init__(*args, **kw)
        filedrop = FileDrop(self)
        self.doaction = DoAction()
        self.filter = []
        self.filelist = []
        self.SetDropTarget(filedrop)
        self._initUi()
        self.SetAutoLayout(True)

    def OnSetFilter(self, event):
        self.filter = self.filterText.GetValue()
        filteredFileList = self.doaction.getFilteredFileList(self.filter)
        self._printFileList(filteredFileList)

    def OnClearFilter(self, event):
        self.filterText.SetValue("")
        self.filter = []
        self._printFileList(self.doaction.getFileList())

    def _OnDrawFilterBox(self, sizer):
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

    def _initUi(self):
        font = wx.Font(12, wx.FONTFAMILY_TELETYPE, wx.NORMAL, wx.NORMAL)
    
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self._OnDrawFilterBox(self.sizer)

        self.text = wx.TextCtrl(self, style = wx.TE_PROCESS_ENTER|wx.TE_READONLY|wx.TE_MULTILINE, size=(WINDOW_SIZE,WINDOW_SIZE))
        self.text.SetValue("")
        self.text.SetFont(font)
        self.sizer.Add(self.text, 1, wx.EXPAND)
        
        btnBox = wx.BoxSizer(wx.HORIZONTAL)

        clearBtnId = wx.NewId()
        clearBtn = wx.Button(self, clearBtnId, "Clear", size=(50,30))
        clearBtn.Bind(wx.EVT_BUTTON, self.OnClearBtn)
        btnBox.Add(clearBtn, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.sizer.Add(btnBox, 0, wx.ALIGN_CENTER_VERTICAL, 5)
        self.SetSizer(self.sizer)

    def OnCallback(self, filelist):
        checkFileList = self.doaction.getFileList(filelist, self.filter)
        self._printFileList(checkFileList)

    def _printFileList(self, files):       
        fileList = "\n".join(files)
        fileList += "\n\nTotal: " + str(len(files))
        self.text.SetValue(fileList)

    def OnClearBtn(self, event):
        self.text.SetValue("")

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