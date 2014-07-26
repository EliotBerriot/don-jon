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
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

from utils import ugettext_lazy as _
import chars
import races
from registries import attributes

def get_asset(name):
    return os.path.join(ASSETS_DIR, name)

class GenerateCharacterWidget(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(GenerateCharacterWidget, self).__init__(*args, **kwargs)
        self.layout = QtGui.QVBoxLayout()       

        self.form_layout = QtGui.QFormLayout()
           
        self.form_layout.addRow( *attributes.get('race').form_row())
        self.layout.addLayout(self.form_layout)
        self.setLayout(self.layout) 

class DonJon(QtGui.QMainWindow):
    
    default_widget = GenerateCharacterWidget
    def __init__(self):
        super(DonJon, self).__init__()
        
        self.initUI()
        
    def initUI(self):
        self.setMinimumWidth(400)
        self.setMinimumHeight(400)
        self.setWindowTitle('Don Jon')
        self.setWindowIcon(QtGui.QIcon(get_asset("icon.png")))      

        generateCharAction = QtGui.QAction(
            QtGui.QIcon(get_asset("character-generate.png")), 
            _(u"Créer un personnage"), 
            self
        )
        generateCharAction.setShortcut('Ctrl+A')
        generateCharAction.triggered.connect(self.generateCharacter)
        self.toolbar = self.addToolBar(_(u'Personnages'))
        self.toolbar.addAction(generateCharAction)
        self.setCentralWidget(self.default_widget())
        self.show()

    def generateCharacter(self):
        self.setCentralWidget(GenerateCharacterWidget())
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = DonJon()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
