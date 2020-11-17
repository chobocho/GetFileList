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

    def getFileList(self, folername = "", filter=[]):
        self.Println("getFileList")
 
        if len(folername) == 0:
            return self.filelist

        self.filelist, self.filelist_without_path = util.fileutil.getFileList(folername)

        if len(filter) == 0:
            return self.filelist
        
        return self.getFilteredFileList(filter)

    def getFilteredFileList(self, filter):
        return util.fileutil.getFilteredFileList(self.filelist, filter)

    def get_filtered_filelist_without_path(self, filter):
        return util.fileutil.getFilteredFileList(self.filelist_without_path, filter)

    def get_file_list_without_path(self, folername = "", filter=[]):
        self.Println("get_file_list_withou_path")

        if len(folername) == 0:
            return self.filelist_without_path

        self.filelist, self.filelist_without_path = util.fileutil.getFileList(folername)

        if len(filter) == 0:
            return self.filelist_without_path

        return self.get_filtered_filelist_without_path(filter)