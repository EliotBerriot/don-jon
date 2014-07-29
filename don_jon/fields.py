from PySide import QtGui, QtCore

class BaseField(object):
    label = ""

    value_changed = QtCore.Signal()

    def __init__(self, *args, **kwargs):
        self.label = kwargs.get('label', '')
        self.initial = kwargs.get('initial')
        super(BaseField, self).__init__()
        self.default = kwargs.get('default')
        if self.default is not None:
            self.value = self.default

    def display(self, **kwargs):
        return self.label + " : ", self

    def emit_value_changed(self):
        self.value_changed.emit()

class IntegerField(BaseField, QtGui.QSpinBox):

    @property
    def value(self):
        return super(IntegerField, self).value()

    @value.setter
    def value(self, new_value):
        return self.setValue(new_value)
        self.emit_value_changed()


class SingleChoiceField(BaseField, QtGui.QComboBox):

    def __init__(self, *args, **kwargs):
        super(SingleChoiceField, self).__init__(*args, **kwargs)
        l = [i.verbose_name for i in self.initial]
        self.addItems(l)

    @property
    def value(self):
        return self.initial[self.currentIndex()]

    @value.setter
    def value(self, new_value):
        self.setCurrentIndex(self.initial.index(new_value))
        self.emit_value_changed()