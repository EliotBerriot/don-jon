from attributes import DefaultAttributesManager
from utils import NameObject

class BaseCharacter(NameObject):

    def __init__(self, *args, **kwargs):
        self.attributes = DefaultAttributesManager(character=self, **kwargs)
        

class Character(BaseCharacter):

    def __init__(self, *args, **kwargs):
        super(Character, self).__init__(*args, **kwargs)

    def __unicode__(self):
        return u"{0} - {1}".format(self.name, self.attributes('race'))