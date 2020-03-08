import os
import util.fileutil

class DoAction():
    def __init__(self):
        self.filelist = {}
        self.duplicatefile = {}
        self.sameSizeFile = {}
        self.TAG = "DoAction"
        pass

    def Println(self, *msg):
        print(self.TAG, " ", msg)

    def getFileList(self, folername = "", filter=[]):
        self.Println("getFileList")
 
        if len(folername) == 0:
            return self.filelist

        self.filelist, sameSizeFile = util.fileutil.getFileList(folername)
        
        self.sameSizeFile = {key: value for (key, value) in sameSizeFile.items() if len(value) >= 2}
        
        self.Println("Same size file set: ", len(self.sameSizeFile))
        if len(filter) == 0:
            return self.filelist
        
        return self.getFilteredFileList(filter)
    
    def getFilteredFileList(self, filter):
        return util.fileutil.getFilteredFileList(self.filelist, filter)

    def getSameSizefileList(self):
        return self.sameSizeFile

    def getDuplicatefileList(self):
        print("getDuplicatefileList")
        self.duplicatefile = {}
        
        for key, value  in self.sameSizeFile.items():
            if len(value) == 2:
                if fileutil.isSameFile(value[0], value[1]):
                    self.duplicatefile[key] = value
            else:
                pass
        return self.duplicatefile