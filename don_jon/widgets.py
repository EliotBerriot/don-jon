#!/usr/bin/python
# -*- coding: utf-8 -*-

from PySide import QtGui
from utils import get_asset, reverse


class Action(QtGui.QAction):

    def __init__(self, icon=None, label="", parent=None, toolbar=None, shortcut=None, callback=None, **kwargs):
        icon = QtGui.QIcon(get_asset(icon))
        self.parent = parent
        super(Action, self).__init__(icon, label, parent)

        if toolbar is not None:
            toolbar.addAction(self)

        if callback is not None:
            self.triggered.connect(callback)
        else:
            self.triggered.connect(self.on_trigger)

        if shortcut is not None:
            self.setShortcut(shortcut)

    def on_trigger(self):
        raise NotImplementedError

class ChangeViewAction(Action):
    def __init__(self, **kwargs):
        self.route = kwargs.get('route')
        super(ChangeViewAction, self).__init__(**kwargs)

    def on_trigger(self):
        self.parent.central_widget = reverse(self.route)
   

