import hashlib
import json
import logging
import os
from util.common import get_chosung

isDebugMode = False
LIMITED_SIZE = 65536


def get_filtered_file_list(fileinfo, filter, callback=None):
    logger = logging.getLogger('getfilelist')
    logger.info(".")

    if len(filter) == 0:
        return fileinfo['folder']

    if ',' in filter:
        return get_and_filtered_file_list(fileinfo['folder'], filter, callback)

    filter_list = []
    tmp_filter_list = filter.split('|')
    # logger.debug (tmpFilterList)
    for it in tmp_filter_list:
        if len(it) == 0:
            continue
        filter_list.append(it.lower().strip())

    if len(filter_list) == 0:
        return fileinfo['folder']

    if None is not callback:
        callback(72)
    filtered_file = []

    tick = 0
    progress = 72
    gap = int(len(fileinfo['folder']) / 28)

    progress, tick = search_folder(callback, fileinfo, filter_list, filtered_file, gap, progress, tick, 90)
    chosung_search(callback, fileinfo, filter_list, filtered_file, gap, progress, tick, 99)
    return filtered_file


def search_folder(callback, fileinfo, filter_list, filtered_file, gap, progress, tick, max_progress):
    for f in fileinfo['folder']:
        fn = f.lower()
        for it in filter_list:
            if it in fn:
                filtered_file.append(f)
                break
        tick += 1
        if tick >= gap:
            tick = 0
            if (None is not callback) and (progress < max_progress):
                progress += 1
                callback(progress)
    return progress, tick


def chosung_search(callback, fileinfo, filter_list, filtered_file, gap, progress, tick, max_progress):
    for i in range(len(fileinfo['chosung_folder'])):
        f = fileinfo['chosung_folder'][i]
        fn = f.lower()
        for it in filter_list:
            if it in fn:
                filtered_file.append(fileinfo['folder'][i])
                break
        tick += 1
        if tick >= gap:
            tick = 0
            if (None is not callback) and (progress < max_progress):
                progress += 1
                callback(progress)
    return progress, tick


def get_and_filtered_file_list(filelist, filter, callback=None):
    logger = logging.getLogger('getfilelist')
    logger.info(".")

    if len(filter) == 0:
        return filelist

    filter_list = []
    tmp_filter_list = filter.split(',')
    print(tmp_filter_list)
    for it in tmp_filter_list:
        if len(it) == 0:
            continue
        filter_list.append(it.lower().strip())
    # logger.debug (filterList)

    if len(filter_list) == 0:
        return filelist

    if None is not callback:
        callback(72)
    tick = 0
    progress = 72
    gap = int(len(filelist)/28)

    filtered_file = []

    for f in filelist:
        fn = f.lower()
        is_match = True
        for it in filter_list:
            if it not in fn:
                is_match = False
                break
        if is_match:
            # logger.debug("Append: " + f)
            filtered_file.append(f)

        tick += 1
        if tick >= gap:
            tick = 0
            if (None is not callback) and (progress < 99):
                progress += 1
                callback(progress)

    return filtered_file


def get_file_list(folders, callback=None):
    logger = logging.getLogger('getfilelist')
    global isDebugMode
    folder_list = []
    file_list = []
    tick = 0
    progress = 0
    gap = 200
    max_file_size = 50_000

    for folder in folders:
        if len(file_list) > max_file_size:
            break

        if os.path.exists(folder):
            if os.path.isfile(folder):
                logger.debug("File : " + folder)
                folder_list.append(folder)
                file_list.append(folder)
                continue

            for (path, dir, files) in os.walk(folder):
                if len(file_list) > max_file_size:
                    break
                for filename in files:
                    if len(file_list) > max_file_size:
                       break
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


def get_path(filename):
    ridx = filename.rfind('\\')
    if ridx == -1:
        return filename

    return filename[:ridx]


def get_filename(filename):
    ridx = filename.rfind('\\')
    if ridx == -1:
        return filename

    return filename[ridx+1:]


def is_same_file(f1, f2):
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


def save_tab_name(tab_name, filename=""):
    logger = logging.getLogger('getfilelist')
    save_data = {'tab_name': tab_name}
    try:
        with open(filename, 'w') as jsonfile:
            json.dump(save_data, jsonfile, indent=2)
    except:
        logger.info("Error to SAVE TAB NAME file")


def load_tab_name(filename=""):
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
        logger.info("Error to load TAB NAME file")

    tab_name = json_data.get('tab_name', [])
    return tab_name