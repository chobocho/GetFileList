import wx
from filedrop import *
import fileutil

WINDOW_SIZE = 480
BTN_SIZE = 50
BTN_HEIGHT = 30

class SimpleGuiPanel(wx.Panel):
    def __init__(self, *args, **kw):
        super(SimpleGuiPanel, self).__init__(*args, **kw)
        filedrop = FileDrop(self)
        self.filter = []
        self.filelist = []
        self.SetDropTarget(filedrop)
        self._initUi()
        self.SetAutoLayout(True)

    def OnSetFilter(self, event):
        self.filter = self.filterText.GetValue()
        filteredFileList = fileutil.getFilteredFileList(self.filelist, self.filter)
        self._printFileList(filteredFileList)

    def OnClearFilter(self, event):
        self.filterText.SetValue("")
        self.filter = []
        self._printFileList(self.filelist)

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
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self._OnDrawFilterBox(self.sizer)

        self.text = wx.TextCtrl(self, style = wx.TE_PROCESS_ENTER|wx.TE_READONLY|wx.TE_MULTILINE, size=(WINDOW_SIZE,WINDOW_SIZE))
        self.text.SetValue("")
        self.sizer.Add(self.text, 1, wx.EXPAND)
        
        btnBox = wx.BoxSizer(wx.HORIZONTAL)

        clearBtnId = wx.NewId()
        clearBtn = wx.Button(self, clearBtnId, "Clear", size=(50,30))
        clearBtn.Bind(wx.EVT_BUTTON, self.OnClearBtn)
        btnBox.Add(clearBtn, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.sizer.Add(btnBox, 0, wx.ALIGN_CENTER_VERTICAL, 5)
        self.SetSizer(self.sizer)

    def OnCallback(self, filelist):
        checkFileList, checkFileSize = fileutil.getFileList(filelist)
        # print (checkFileList)
        self.filelist = checkFileList
        filteredFileList = fileutil.getFilteredFileList(checkFileList, self.filter)
        self._printFileList(filteredFileList)

    def _printFileList(self, files):
        fileList = ""
        for file in files:
            #print(file)
            fileList += file + "\n"
        fileList += "\n\nTotal: " + str(len(files))
        self.text.SetValue(fileList)

    def OnClearBtn(self, event):
        self.text.SetValue("")