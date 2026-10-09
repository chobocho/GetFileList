import wx

SHORTCUT_LIST = [
    ("Tab", [
        ("Ctrl + 1 ~ 8", "Select tab 1 ~ 8"),
        ("Ctrl + T", "Next tab"),
        ("Ctrl + Shift + T", "Previous tab"),
    ]),
    ("Filter", [
        ("Ctrl + F / Alt + D", "Focus filter"),
        ("Alt + C", "Clear filter"),
    ]),
    ("File", [
        ("Ctrl + C", "Copy file list to clipboard"),
        ("Ctrl + Shift + V", "Append folder from clipboard"),
        ("Ctrl + Shift + L", "Reload folders"),
        ("Ctrl + L", "Show file size"),
        ("Ctrl + O", "Open selected file"),
        ("Ctrl + R / Ctrl + Shift + 6 / Shift + F6", "Rename selected file"),
        ("Ctrl + Alt + D", "Delete selected file"),
    ]),
    ("Tool", [
        ("Ctrl + M", "Run Notepad"),
        ("Ctrl + P", "Run MS Paint"),
    ]),
    ("App", [
        ("F1", "Show this help"),
        ("Ctrl + Q", "Quit"),
    ]),
]


class HelpDialog(wx.Dialog):
    def __init__(self, parent, title="Shortcuts"):
        super(HelpDialog, self).__init__(parent, title=title, size=(520, 560),
                                         style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        shortcut_list_ctrl = wx.ListCtrl(self, style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_HRULES)
        shortcut_list_ctrl.InsertColumn(0, "Shortcut", width=240)
        shortcut_list_ctrl.InsertColumn(1, "Description", width=240)

        bold_font = shortcut_list_ctrl.GetFont().Bold()
        for group, shortcuts in SHORTCUT_LIST:
            idx = shortcut_list_ctrl.InsertItem(shortcut_list_ctrl.GetItemCount(), f"[{group}]")
            shortcut_list_ctrl.SetItemFont(idx, bold_font)
            shortcut_list_ctrl.SetItemBackgroundColour(idx, wx.Colour(230, 230, 230))
            for key, desc in shortcuts:
                idx = shortcut_list_ctrl.InsertItem(shortcut_list_ctrl.GetItemCount(), "    " + key)
                shortcut_list_ctrl.SetItem(idx, 1, desc)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(shortcut_list_ctrl, 1, wx.EXPAND | wx.ALL, 8)
        sizer.Add(self.CreateButtonSizer(wx.OK), 0, wx.ALIGN_RIGHT | wx.ALL, 8)
        self.SetSizer(sizer)
        self.CenterOnParent()
