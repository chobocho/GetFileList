from ui.getfilelistframe import *
import logging
import logging.handlers
from buildinfo.info import *

WINDOW_SIZE = 640
MAX_LOG_SIZE = 512 * 1024

def initLogger():
    logger = logging.getLogger('getfilelist')
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s [%(levelno)s] %(filename)s:%(funcName)s() > %(message)s')

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    fh = logging.handlers.RotatingFileHandler(filename='getfilelist.log', maxBytes=MAX_LOG_SIZE)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    
    logger.info("=== " + SW_TITLE + " ===")

def printEnd():
    logger = logging.getLogger('getfilelist')
    logger.info("=== END ===")

def main(): 
    initLogger()
    app = wx.App()
    frm = GetFileListFrame(None, version= SW_TITLE, title=SW_TITLE, size=(WINDOW_SIZE,WINDOW_SIZE))
    frm.Show()
    app.MainLoop()
    printEnd()

if __name__ == '__main__':
    main()
