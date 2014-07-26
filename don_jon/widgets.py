from PySide import QtGui


class SingleChoice(QtGui.QComboBox):

    def __init__(self, initial=[], parent=None, **kwargs):
        super(SingleChoice, self).__init__(parent)
        self.initial = initial
        l = [i.verbose_name for i in self.initial]
        self.addItems(l)

    @property
    def value(self):
        return self.initial[self.currentIndex()]

    @value.setter
    def value(self, new_value):
        self.setCurrentIndex(self.initial.index(new_value))