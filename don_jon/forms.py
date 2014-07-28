from models import Character
from PySide import QtGui


class CharacterForm(object):
    enabled_fields = ('race', 'level')

    model = Character
    def __init__(self, instance=None, **kwargs):
        if instance is not None:
            self.instance = instance
        else:
            self.instance = self.model()

        self.fields = {}
        for field in self.enabled_fields:
            self.fields[field] = self.instance.attributes.get(field).form_field()


    def validate(self):
        return True

    def process(self):
        if self.validate():
            for field in self.enabled_fields:
                self.instance.attributes.get(field).base_value = self.fields[field].value

            return self.instance
        else:
            raise ValidationError 

    def display(self):
        form_layout = QtGui.QFormLayout()
           
        for field in self.enabled_fields:
            form_layout.addRow(*self.fields[field].display())
        return form_layout