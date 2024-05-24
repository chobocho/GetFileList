import hashlib
import json
import logging
import os
from util.common import get_chosung

isDebugMode = False
LIMITED_SIZE = 65536


def getFilteredFileList(filelist, filter, callback=None):
    logger = logging.getLogger('getfilelist')
    logger.info(".")

    if len(filter) == 0:
        return filelist

    if ',' in filter:
        return getAndFilteredFileList(filelist, filter, callback)

    filterList = []
    tmpFilterList = filter.split('|')
    # logger.debug (tmpFilterList)
    for it in tmpFilterList:
        if len(it) == 0:
            continue
        filterList.append(it.lower())

    if len(filterList) == 0:
        return filelist

    if None != callback:
        callback(72)
    filteredFile = []

    tick = 0
    progress = 72
    gap = int(len(filelist)/28)

    for f in filelist:
        fn = f.lower()
        for it in filterList:
            if it in fn:
                filteredFile.append(f)
                break
        tick+=1
        if tick >= gap:
            tick = 0
            if (None != callback) and (progress < 99):
                progress += 1
                callback(progress)

    return filteredFile


def getAndFilteredFileList(filelist, filter, callback=None):
    logger = logging.getLogger('getfilelist')
    logger.info(".")

    if len(filter) == 0:
        return filelist

    filterList = []
    tmpFilterList = filter.split(',')
    print(tmpFilterList)
    for it in tmpFilterList:
        if len(it) == 0:
            continue
        filterList.append(it.lower())
    # logger.debug (filterList)

    if len(filterList) == 0:
        return filelist

    if None != callback:
        callback(72)
    tick = 0
    progress = 72
    gap = int(len(filelist)/28)

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

        tick += 1
        if tick >= gap:
            tick = 0
            if (None != callback) and (progress < 99):
                progress += 1
                callback(progress)

    return filteredFile


def getFileList(folders, callback=None):
    logger = logging.getLogger('getfilelist')
    global isDebugMode
    folder_list = []
    file_list = []
    tick = 0
    progress = 0
    gap = 200

    for folder in folders:
        if os.path.exists(folder):
            if os.path.isfile(folder):
                logger.debug("File : " + folder)
                folder_list.append(folder)
                file_list.append(folder)
                continue

            for (path, dir, files) in os.walk(folder):
                for filename in files:
                    tf = os.path.join(path, filename)
                    if "\\.git\\" not in tf:
                        folder_list.append(tf)
                        file_list.append(filename)

                    tick += 1
                    if tick > gap:
                        tick = 0
                        if (None != callback) and (progress < 70):
                            progress += 1
                            callback(progress)
        else:
            logger.warning("Error:", folder, " is not exist")

    logger.info(str(len(folder_list)) + " " + str(len(file_list)))

    file_info = {}
    file_info['chosung_folder'] = [get_chosung(f) for f in folder_list]
    file_info['chosung_file'] = [get_chosung(f) for f in file_list]
    file_info['folder'] = folder_list
    file_info['file'] = file_list
    return file_info


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


def delete(filename):
    if not os.path.exists(filename):
        return

    try:
        os.remove(filename)
        print("File delete success!")
    except OSError as error:
        print("File: ", error)


def load_cfg(filename=""):
    logger = logging.getLogger('getfilelist')

    if len(filename) == 0:
        return []

    if not os.path.exists(filename):
        logger.info(f"CFG({filename}) is not exist!")
        return []

    json_data = {}
    try:
        with open(filename) as json_file:
            json_data = json.load(json_file)
    except:
        logger.info("Error to load CFG file")

    raw_folder_info = json_data.get('folder_info', [])
    folder_info = []
    for f in raw_folder_info:
        if os.path.exists(f):
            folder_info.append(f)

    return folder_info


def save_cfg(folder_info, filename=""):
    logger = logging.getLogger('getfilelist')
    print(folder_info)

    save_data = {'folder_info': folder_info}
    try:
        with open(filename, 'w') as jsonfile:
            json.dump(save_data, jsonfile, indent=2)
    except:
        logger.info("Error to SAVE CFG file")
