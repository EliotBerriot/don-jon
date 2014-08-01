
from utils import NameObject
from registries import classes as classes_registry
from utils import ugettext_lazy as _

class BaseClass(NameObject):
    modify = {}
    life_dice = 5
@classes_registry.register
class Warrior(BaseClass):
    life_dice = 10
    verbose_name = _('Guerrier')

@classes_registry.register
class Barbarian(BaseClass):
    life_dice = 12
    verbose_name = _('Barbare')
