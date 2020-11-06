import os
import util.fileutil

class DoAction:
    def __init__(self):
        self.filelist = {}
        self.TAG = "DoAction"
        pass

    def Println(self, *msg):
        print(self.TAG, " ", msg)

    def getFileList(self, folername = "", filter=[]):
        self.Println("getFileList")
 
        if len(folername) == 0:
            return self.filelist

        self.filelist = util.fileutil.getFileList(folername)

        if len(filter) == 0:
            return self.filelist
        
        return self.getFilteredFileList(filter)
    
    def getFilteredFileList(self, filter):
        return util.fileutil.getFilteredFileList(self.filelist, filter)
