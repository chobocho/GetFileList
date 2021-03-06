import wx


class GetFileListMenu:
    def __init__(self, parent):
        self.parent = parent
        self._addMenubar()

    def _addMenubar(self):
        menubar = wx.MenuBar()

        ##
        fileMenu = wx.Menu()

        reloadItemmId = wx.NewId()
        reloadItem = fileMenu.Append(reloadItemmId, 'Reload', 'Reload folders')
        self.parent.Bind(wx.EVT_MENU, self.parent.OnReload, reloadItem)

        quitItem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit App')
        self.parent.Bind(wx.EVT_MENU, self.parent.OnQuit, quitItem)
        menubar.Append(fileMenu, '&File')

        ##
        viewMenu = wx.Menu()

        show_filepath_id = wx.NewId()
        self.show_filepath = viewMenu.AppendCheckItem(show_filepath_id, 'Show file path', 'Show file path')
        self.parent.Bind(wx.EVT_MENU, self.parent.on_show_file_path, self.show_filepath)
        self.show_filepath.Check(True)

        menubar.Append(viewMenu, '&View')

        # findSameSizeItemId = wx.NewId()
        # findSameSizeItem = editMenu.Append(findSameSizeItemId, 'Find same size', 'Find same size files')
        # self.parent.Bind(wx.EVT_MENU, self.parent.OnFindSameSize, findSameSizeItem)

        # findDuplicateItemId = wx.NewId()
        # findDuplicateItem = editMenu.Append(findDuplicateItemId, 'Find duplicate', 'Find duplicate files')
        # self.parent.Bind(wx.EVT_MENU, self.parent.OnFindDuplicate, findDuplicateItem)
        # menubar.Append(editMenu, '&Edit')

        helpMenu = wx.Menu()
        aboutItemId = wx.NewId()
        aboutItem = helpMenu.Append(aboutItemId, 'About', 'About')
        self.parent.Bind(wx.EVT_MENU, self.parent.OnAbout, aboutItem)
        menubar.Append(helpMenu, '&Help')

        self.parent.SetMenuBar(menubar)

    def is_show_menu(self):
        return self.show_filepath.IsChecked() == True

    def toggle_show_menu(self):
        if self.show_filepath.IsChecked():
            self.show_filepath.Check(False)
        else:
            self.show_filepath.Check(True)