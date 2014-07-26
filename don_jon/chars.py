from attributes import DefaultAttributesManager
from utils import NameObject

class BaseCharacter(NameObject):

    def __init__(self, *args, **kwargs):
        super(BaseCharacter, self).__init__(*args, **kwargs)
        self.attributes = DefaultAttributesManager(character=self, **kwargs)
        

class Character(BaseCharacter):

    def __init__(self, *args, **kwargs):
        super(Character, self).__init__(*args, **kwargs)

    def display(self):

        for section, attributes in self.attributes._attributes_list.items():
            print('{0}\n{1}\n'.format(section, "*" * len(section)))

            for a in attributes:
                attribute = self.attributes(a.clsname())
                key = attribute.clsname()
                if isinstance(attribute.value, type):
                    value = attribute.value.clsname()
                else:
                    value = attribute.value
                print('{0}: {1}'.format(key, value))

            print('\n')

class CharacterGenerator(object):

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def create(self, **kwargs):
        kw = self.kwargs.copy()
        kw.update(kwargs)
        return Character(**kw)
