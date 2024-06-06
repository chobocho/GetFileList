import os
import util.fileutil
from manager.excelmanager import *


class DoAction:
    def __init__(self):
        self.filelist = {}
        self.filelist_without_path = {}
        self.file_info = {}
        self.TAG = "DoAction"
        pass

    def println(self, *msg):
        print(self.TAG, " ", msg)

    def get_file_list(self, foler_name=None, filters=None, callback=None):
        self.println("getFileList")

        if foler_name is None:
            if (filters is None) and len(self.filelist) > 0:
                return self.filelist
            return []

        if None is not callback:
            callback(1)
        self.file_info = util.fileutil.get_file_list(foler_name, callback)
        self.filelist = self.file_info['folder']
        self.filelist_without_path = self.file_info['file']

        if filters is None:
            return self.filelist

        if None is not callback:
            callback(71)
        return self.get_filtered_file_list(filters, callback)

    def get_filtered_file_list(self, filters, callback=None):
        return util.fileutil.get_filtered_file_list(self.file_info, filters, callback)

    def get_filtered_filelist_without_path(self, filter, callback=None):
        return util.fileutil.get_filtered_file_list(self.filelist_without_path, filter, callback)

    def get_file_list_without_path(self, foldername=[], filter=[], callback=None):
        self.println("get_file_list_withou_path")

        if len(foldername) == 0:
            return []

        self.file_info = util.fileutil.get_file_list(foldername, callback)
        self.filelist = self.file_info['folder']
        self.filelist_without_path = self.file_info['file']

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
