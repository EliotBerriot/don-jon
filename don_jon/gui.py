#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode PySide tutorial 

This example shows an icon
in the titlebar of the window.

author: Jan Bodnar
website: zetcode.com 
last edited: August 2011
"""

import sys, os
from PySide import QtGui

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(BASE_DIR))

from utils import reverse, get_asset, ugettext_lazy as _
from widgets import ChangeViewAction
from registries import routes
import routes
import sys



class DonJon(QtGui.QMainWindow):
    
    default_view = 'character.list'
    def __init__(self):
        super(DonJon, self).__init__()
        
        self.initUI()
     
    @property
    def central_widget(self):
        return self.central_widget

    @central_widget.setter
    def central_widget(self, new_value):
        self.setCentralWidget(new_value)

    def initUI(self):
        self.setWindowTitle('Don Jon')
        self.setWindowIcon(QtGui.QIcon(get_asset("icon.png")))      

        self.toolbar = self.addToolBar(_(u'Personnages'))
        g = ChangeViewAction(
            icon="character-generate.png", 
            label=_(u"Créer un personnage"), 
            parent=self,
            toolbar=self.toolbar,
            shortcut='Ctrl+A',
            route='character.create'
        )
        g = ChangeViewAction(
            icon="character-list.png", 
            label=_(u"Tous les personnages"), 
            parent=self,
            toolbar=self.toolbar,
            shortcut='Ctrl+L',
            route='character.list'
        )
        
        self.central_widget = reverse(self.default_view, parent=self)
        self.show()

    def generateCharacter(self):
        self.setCentralWidget(GenerateCharacter())
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = DonJon()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
