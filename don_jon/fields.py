from PySide import QtGui, QtCore
from widgets import Icon

class BaseField(object):
    label = ""

    value_changed = QtCore.Signal()
    base_value_changed_signal = None

    # If true, form will add signal to update field value on character change
    keep_synced = True

    def __init__(self, *args, **kwargs):
        self.label = kwargs.get('label', '')
        self.initial = kwargs.get('initial')
        self.attribute = kwargs.get('attribute')
        super(BaseField, self).__init__()
        self.default = kwargs.get('default')
        if self.default is not None:
            self.value = self.default

        getattr(self, self.base_value_changed_signal).connect(self.emit_value_changed)

    def randomize(self):
        self.value = self.attribute.roll()

    def display(self, **kwargs):
        widgets = [self.label + " : ", self]
        if self.attribute.random:
            randomize = QtGui.QPushButton(Icon('dice.png'), u"Relancer")
            randomize.clicked.connect(lambda: self.randomize())        
            
            widgets.append(randomize)
        return widgets

    def emit_value_changed(self, *args, **kwargs):
        self.value_changed.emit()

    @property
    def value(self):
        raise NotImplementedError

    @value.setter
    def value(self, new_value):
        self.blockSignals(True)
        self.change_value(new_value)
        self.blockSignals(False)


class StringField(BaseField, QtGui.QLineEdit):

    base_value_changed_signal = 'textChanged'

    @BaseField.value.getter
    def value(self):
        return self.text()   

    def change_value(self, new_value):
        self.setText(new_value)

class IntegerField(BaseField, QtGui.QSpinBox):

    base_value_changed_signal = 'valueChanged'

    def __init__(self, *args, **kwargs):
        super(IntegerField, self).__init__(*args, **kwargs)
        self.setMinimum(1)
        self.setMaximum(999999)

    @BaseField.value.getter
    def value(self):
        return QtGui.QSpinBox.value(self)   

    def change_value(self, new_value):
        self.setValue(new_value)

class SingleChoiceField(BaseField, QtGui.QComboBox):

    base_value_changed_signal = 'currentIndexChanged'

    def __init__(self, *args, **kwargs):
        super(SingleChoiceField, self).__init__(*args, **kwargs)
        self.display_list = [i.verbose_name for i in self.initial]
        self.addItems(self.display_list)

    @BaseField.value.getter
    def value(self):
        return self.initial[self.currentIndex()]

    def change_value(self, new_value):
        choices = [c.clsname() for c in self.initial]
        self.setCurrentIndex(choices.index(new_value))