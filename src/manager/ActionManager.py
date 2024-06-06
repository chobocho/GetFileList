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

    def on_rename(self, origin_path, new_filename) -> bool:
        if len(origin_path) == 0 or len(new_filename) == 0:
            print(f"Lenth of {new_filename} is 0\n")
            return False

        if origin_path == new_filename:
            print("Not changed!")
            return False

        try:
            os.rename(origin_path, new_filename)
            return True
        except:
            print(f"Fail to change {origin_path} to {new_filename}\n")
        return False