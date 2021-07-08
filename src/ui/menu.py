import wx


class GetFileListMenu:
    def __init__(self, parent):
        self.parent = parent
        self._addMenubar()

    def _addMenubar(self):
        menubar = wx.MenuBar()

        self._add_filemenu(menubar)
        self._add_viewmenu(menubar)
        self._add_helpmenu(menubar)

        self.parent.SetMenuBar(menubar)

    def _add_helpmenu(self, menubar):
        helpMenu = wx.Menu()
        aboutItemId = wx.NewId()
        aboutItem = helpMenu.Append(aboutItemId, '&About', 'About')
        self.parent.Bind(wx.EVT_MENU, self.parent.OnAbout, aboutItem)
        menubar.Append(helpMenu, '&Help')

    def _add_viewmenu(self, menubar):
        viewMenu = wx.Menu()
        show_filepath_id = wx.NewId()
        self.show_filepath = viewMenu.AppendCheckItem(show_filepath_id, '%Show file path', 'Show file path')
        self.parent.Bind(wx.EVT_MENU, self.parent.on_show_file_path, self.show_filepath)
        self.show_filepath.Check(True)
        menubar.Append(viewMenu, '&View')

    def _add_filemenu(self, menubar):
        fileMenu = wx.Menu()

        saveFilelistId = wx.NewId()
        saveFilelist = fileMenu.Append(saveFilelistId, '&Save as Excel', 'Save as Excel')
        self.parent.Bind(wx.EVT_MENU, self.parent.OnSaveAsExcel, saveFilelist)

        reloadItemId = wx.NewId()
        reloadItem = fileMenu.Append(reloadItemId, '&Reload', 'Reload folders')
        self.parent.Bind(wx.EVT_MENU, self.parent.OnReload, reloadItem)

        quitItem = fileMenu.Append(wx.ID_EXIT, '&Quit', 'Quit App')
        self.parent.Bind(wx.EVT_MENU, self.parent.OnQuit, quitItem)

        menubar.Append(fileMenu, '&File')

    def is_show_menu(self):
        return self.show_filepath.IsChecked() is True

    def toggle_show_menu(self):
        if self.show_filepath.IsChecked():
            self.show_filepath.Check(False)
        else:
            self.show_filepath.Check(True)