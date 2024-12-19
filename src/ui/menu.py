import wx


class GetFileListMenu:
    def __init__(self, parent):
        self.parent = parent
        self._add_menubar()

    def _add_menubar(self):
        menubar = wx.MenuBar()

        self._add_file_menu(menubar)
        self._add_view_menu(menubar)
        self._add_help_menu(menubar)

        self.parent.SetMenuBar(menubar)

    def _add_help_menu(self, menubar):
        help_menu = wx.Menu()
        about_item_id = wx.NewId()
        about_item = help_menu.Append(about_item_id, '&About', 'About')
        self.parent.Bind(wx.EVT_MENU, self.parent.OnAbout, about_item)
        menubar.Append(help_menu, '&Help')

    def _add_view_menu(self, menubar):
        view_menu = wx.Menu()
        # TODO fix this code
        # show_filepath_id = wx.NewId()
        # self.show_filepath = viewMenu.AppendCheckItem(show_filepath_id, '&Show file path', 'Show file path')
        # self.parent.Bind(wx.EVT_MENU, self.parent.on_show_file_path, self.show_filepath)
        # self.show_filepath.Check(True)

        show_folder_info_id = wx.NewId()
        self.show_folder_info = view_menu.AppendCheckItem(show_folder_info_id, 'Show folder &info', 'Show folder info')
        self.parent.Bind(wx.EVT_MENU, self.parent.on_show_folder_info, self.show_folder_info)
        self.show_folder_info.Check(True)
        menubar.Append(view_menu, '&View')

    def _add_file_menu(self, menubar):
        file_menu = wx.Menu()

        save_folder_info_id = wx.NewId()
        self.save_folder_info = file_menu.AppendCheckItem(save_folder_info_id, 'Save folder &info', 'Save folder info')
        self.parent.Bind(wx.EVT_MENU, self.parent.save_foler_info, self.save_folder_info)
        self.save_folder_info.Check(True)

        save_filelist_id = wx.NewId()
        save_filelist = file_menu.Append(save_filelist_id, '&Save as Excel', 'Save as Excel')
        self.parent.Bind(wx.EVT_MENU, self.parent.OnSaveAsExcel, save_filelist)

        reload_item_id = wx.NewId()
        reload_item = file_menu.Append(reload_item_id, '&Reload', 'Reload folders')
        self.parent.Bind(wx.EVT_MENU, self.parent.OnReload, reload_item)

        quit_item = file_menu.Append(wx.ID_EXIT, '&Quit', 'Quit App')
        self.parent.Bind(wx.EVT_MENU, self.parent.OnQuit, quit_item)

        menubar.Append(file_menu, '&File')

    def is_show_menu(self):
        return self.show_filepath.IsChecked() is True

    def toggle_show_menu(self):
        if self.show_filepath.IsChecked():
            self.show_filepath.Check(False)
        else:
            self.show_filepath.Check(True)

    def is_show_folder_info_menu(self):
        return self.show_folder_info.IsChecked() is True

    def is_save_folder_info_menu(self):
        return self.save_folder_info.IsChecked() is True

