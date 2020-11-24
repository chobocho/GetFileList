import os
import util.fileutil

class DoAction:
    def __init__(self):
        self.filelist = {}
        self.filelist_without_path = {}
        self.TAG = "DoAction"
        pass

    def Println(self, *msg):
        print(self.TAG, " ", msg)

    def getFileList(self, folername = "", filter=[], callback=None):
        self.Println("getFileList")
 
        if len(folername) == 0:
            return self.filelist

        if None != callback:
            callback(1)
        self.filelist, self.filelist_without_path = util.fileutil.getFileList(folername, callback)

        if len(filter) == 0:
            return self.filelist

        if None != callback:
            callback(71)
        return self.getFilteredFileList(filter, callback)

    def getFilteredFileList(self, filter, callback=None):
        return util.fileutil.getFilteredFileList(self.filelist, filter, callback)

    def get_filtered_filelist_without_path(self, filter, callback=None):
        return util.fileutil.getFilteredFileList(self.filelist_without_path, filter, callback)

    def get_file_list_without_path(self, folername = "", filter=[], callback=None):
        self.Println("get_file_list_withou_path")

        if len(folername) == 0:
            return self.filelist_without_path

        self.filelist, self.filelist_without_path = util.fileutil.getFileList(folername, callback)

        if len(filter) == 0:
            return self.filelist_without_path

        if None != callback:
            callback(71)
        return self.get_filtered_filelist_without_path(filter, callback)