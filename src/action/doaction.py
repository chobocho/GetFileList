import os
import util.fileutil
from manager.excelmanager import *


class DoAction:
    def __init__(self):
        self.filelist = {}
        self.filelist_without_path = {}
        self.TAG = "DoAction"
        pass

    def Println(self, *msg):
        print(self.TAG, " ", msg)

    def getFileList(self, folername=None, filter=None, callback=None):
        self.Println("getFileList")

        if folername is None:
            if (filter is None) and len(self.filelist) > 0:
                return self.filelist
            return []

        if None != callback:
            callback(1)
        self.filelist, self.filelist_without_path = util.fileutil.getFileList(folername, callback)

        if filter is None:
            return self.filelist

        if None != callback:
            callback(71)
        return self.getFilteredFileList(filter, callback)

    def getFilteredFileList(self, filter, callback=None):
        return util.fileutil.getFilteredFileList(self.filelist, filter, callback)

    def get_filtered_filelist_without_path(self, filter, callback=None):
        return util.fileutil.getFilteredFileList(self.filelist_without_path, filter, callback)

    def get_file_list_without_path(self, foldername=[], filter=[], callback=None):
        self.Println("get_file_list_withou_path")

        if len(foldername) == 0:
            return []

        self.filelist, self.filelist_without_path = util.fileutil.getFileList(foldername, callback)

        if len(filter) == 0:
            return self.filelist_without_path

        if None != callback:
            callback(71)
        return self.get_filtered_filelist_without_path(filter, callback)

    def OnSaveAsExcel(self):
        if len(self.filelist) == 0:
            print("OnSaveAsExcel: There is no file in the list")
            return

        excelManager = ExcelManager()
        excelManager.saveData(self.filelist)


    def OnReset(self):
        self.filelist = {}
