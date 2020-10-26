#!/usr/bin/python
#-*- coding: utf-8 -*-
import os

class ActionManager:
    def __init__(self):
        pass

    def OnRunCommand(self, command, path=None):
        if command == 'ctrl_p':
            os.startfile('mspaint')
        elif command == 'ctrl_m':
            os.startfile('notepad')
        elif command == 'explore':
            chosenItem = '"' + path + '"'
            os.startfile(chosenItem)
