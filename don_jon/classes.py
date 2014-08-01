
from utils import NameObject
from registries import classes as classes_registry
from utils import ugettext_lazy as _

class BaseClass(NameObject):
    modify = {}

@classes_registry.register
class Warrior(BaseClass):

    verbose_name = _('Guerrier')
