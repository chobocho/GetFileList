import os
import fileutil

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

        self.filelist, sameSizeFile = fileutil.getFileList(folername)
        
        for item in sameSizeFile:
            s = len(sameSizeFile[item])
            if s == 1:
                continue
            self.sameSizeFile[item] = sameSizeFile[item]
            #self.Println(item, len(self.duplicatefile[item]))
        
        self.Println("Same size file set: ", len(self.sameSizeFile))
        if len(filter) == 0:
            return self.filelist
        
        return self.getFilteredFileList(filter)
    
    def getFilteredFileList(self, filter):
        return fileutil.getFilteredFileList(self.filelist, filter)

    def getSameSizefileList(self):
        return self.sameSizeFile

    def getDuplicateFileList(self):
        return self.duplicatefile