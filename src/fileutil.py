import os

isDebugMode = False

def getFilteredFileList(filelist, filter):
    print ("getFilteredFileList")

    if len(filter) == 0:
        return filelist

    if filter[0] == '&':
        return getAndFilteredFileList(filelist, filter)

    filterList = []
    tmpFilterList = filter.split('|')
    #print (tmpFilterList)
    for it in tmpFilterList:
        if len(it) == 0:
            continue
        filterList.append(it.lower())

    if len(filterList) == 0:
        return filelist

    filteredFile = []

    for f in filelist:
        fn = f.lower()
        for it in filterList:
            if it in fn:
                filteredFile.append(f)
                break
    
    return filteredFile

def getAndFilteredFileList(filelist, filter):
    print ("getAndFilteredFileList")

    if len(filter) == 0:
        return filelist

    filterList = []
    tmpFilterList = filter.split('&')
    print (tmpFilterList)
    for it in tmpFilterList:
        if len(it) == 0:
            continue
        filterList.append(it.lower())
    #print (filterList)

    if len(filterList) == 0:
        return filelist

    filteredFile = []

    for f in filelist:
        fn = f.lower()
        isMatch = True
        for it in filterList:
            if it not in fn:
                isMatch = False
                break
        if isMatch:
            #print("Append: " + f)
            filteredFile.append(f)
    
    return filteredFile

def getFileList(folders):
    print ("getFileList")
    global isDebugMode
    error_msg = []
    aResult = {}  
    folderInfo = {}  

    for folder in folders:
        if os.path.exists(folder):
            for (path, dir, files) in os.walk(folder):
                for filename in files:
                    tf = os.path.join(path, filename)
                    if isDebugMode: 
                        print (tf)
                    try:
                        folderInfo[tf] = os.path.getsize(tf);
                        #if isDebugMode: print ("%s/%s " % (path, filename))
                        if isDebugMode: print ("%s : %d" % (tf, folderInfo[tf]))
                        if aResult.get(folderInfo[tf]) == None:
                            aResult[folderInfo[tf]] = [tf]
                        else:
                            aResult[folderInfo[tf]].append(tf)
                    except:
                        error_msg.append('Fail to get size of ' + tf)
                        print (error_msg[-1])
 
        else:
            print ("Error:",folder," is not exist")           

    #print (folderInfo)
    return folderInfo, aResult