#!/usr/bin/python
#-*- coding: utf-8 -*-
import os
from util import fileutil


class ActionManager:
    def __init__(self):
        pass

    def on_run_command(self, command, path=None):
        if command == 'delete':
            fileutil.delete(path)
        elif command == 'ctrl_p':
            os.startfile('mspaint')
        elif command == 'ctrl_m':
            os.startfile('notepad')
        elif command == 'explore':
            chosen_item = '"' + path + '"'
            os.startfile(chosen_item)
