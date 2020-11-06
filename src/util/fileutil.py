import os
import hashlib
import logging

isDebugMode = False
LIMITED_SIZE = 65536


def getFilteredFileList(filelist, filter):
    logger = logging.getLogger('getfilelist')
    logger.info(".")

    if len(filter) == 0:
        return filelist

    if filter[0] == '&':
        return getAndFilteredFileList(filelist, filter)

    filterList = []
    tmpFilterList = filter.split('|')
    # logger.debug (tmpFilterList)
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
    logger = logging.getLogger('getfilelist')
    logger.info(".")

    if len(filter) == 0:
        return filelist

    filterList = []
    tmpFilterList = filter.split('&')
    print(tmpFilterList)
    for it in tmpFilterList:
        if len(it) == 0:
            continue
        filterList.append(it.lower())
    # logger.debug (filterList)

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
            # logger.debug("Append: " + f)
            filteredFile.append(f)

    return filteredFile


def getFileList(folders):
    logger = logging.getLogger('getfilelist')
    global isDebugMode
    folder_list = []

    for folder in folders:
        if os.path.exists(folder):
            if os.path.isfile(folder):
                logger.debug("File : " + folder)
                folder_list.append(folder)
                continue

            for (path, dir, files) in os.walk(folder):
                for filename in files:
                    tf = os.path.join(path, filename)
                    if "\\.git\\" not in tf:
                        folder_list.append(tf)
        else:
            logger.warning("Error:", folder, " is not exist")

    logger.info(len(folder_list))
    return folder_list


def getPath(filename):
    ridx = filename.rfind('\\')
    if ridx == -1:
        return filename

    return filename[:ridx]


def get_filename(filename):
    ridx = filename.rfind('\\')
    if ridx == -1:
        return filename

    return filename[ridx+1:]


def isSameFile(f1, f2):
    bufsize = LIMITED_SIZE
    with open(f1, 'rb') as fp1, open(f2, 'rb') as fp2:
        b1 = fp1.read(bufsize)
        b2 = fp2.read(bufsize)
        if b1 != b2:
            return False
        return True


def getHashValue(filepath):
    chunksize = LIMITED_SIZE
    hash = hashlib.md5()

    with open(filepath, 'rb') as afile:
        buf = afile.read(chunksize)
        while len(buf) > 0:
            buf = afile.read(chunksize)
            hash.update(buf)

    retHash = hash.hexdigest()
    return retHash


def getMyHash(filepath):
    chunksize = 1024

    with open(filepath, 'rb') as afile:
        buf = afile.read(chunksize)

    bound = '0.1105' * 171
    if len(buf) < 1024:
        myHash = buf.decode('utf-8') + bound
    else:
        myHash = buf
    print(myHash)
    return myHash[0:1024]
