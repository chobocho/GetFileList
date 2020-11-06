#!/usr/bin/python
#-*- coding: utf-8 -*-
import os

class ActionManager:
    def __init__(self):
        pass

    def on_run_command(self, command, path=None):
        if command == 'ctrl_p':
            os.startfile('mspaint')
        elif command == 'ctrl_m':
            os.startfile('notepad')
        elif command == 'explore':
            chosen_item = '"' + path + '"'
            os.startfile(chosen_item)
