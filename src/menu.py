import wx

class SimpleGuiMenu():
    def __init__(self, parent):
        self.parent = parent
        self._addMenubar()

    def _addMenubar(self):
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fileItem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit App')
        self.parent.Bind(wx.EVT_MENU, self.parent.OnQuit, fileItem)
        menubar.Append(fileMenu, '&File')

        editMenu = wx.Menu()

        findSameSizeItemId = wx.NewId()
        findSameSizeItem = editMenu.Append(findSameSizeItemId, 'Find same size', 'Find same size files')
        self.parent.Bind(wx.EVT_MENU, self.parent.OnFindSameSize, findSameSizeItem)

        findDuplicateItemId = wx.NewId()
        findDuplicateItem = editMenu.Append(findDuplicateItemId, 'Find duplicate', 'Find duplicate files')
        self.parent.Bind(wx.EVT_MENU, self.parent.OnFindDuplicate, findDuplicateItem)
        menubar.Append(editMenu, '&Edit')

        helpMenu = wx.Menu()
        aboutItemId = wx.NewId()
        aboutItem = helpMenu.Append(aboutItemId, 'About', 'About')
        self.parent.Bind(wx.EVT_MENU, self.parent.OnAbout, aboutItem)
        menubar.Append(helpMenu, '&Help')

        self.parent.SetMenuBar(menubar)
