
class View(object):
    def __init__(self, **kwargs):
        super(View, self).__init__()
        self.kwargs = kwargs

    def __call__(self, **kwargs):
        return self.process(**kwargs)

    def process(self, **kwargs):
        return None

class TestOne(View):

    def process(self, **kwargs):
        return self.kwargs

from PySide import QtGui
from forms import CharacterForm

class CharacterCreate(View, QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(CharacterCreate, self).__init__(*args, **kwargs)
        self.layout = QtGui.QVBoxLayout()       

        self.layout.addLayout(CharacterForm().display())
        self.setLayout(self.layout) 

    def process(self, **kwargs):
        return self