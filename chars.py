from utils import autoassign


class BaseCharacter(object):

    base_attributes = {
        "strength": 10,
        "dexterity": 10,
        "constitution": 10,
        "intelligence": 10,
        "wisdom": 10,
        "charisma": 10,    
    }
    attributes = {}

    level = 1

    @autoassign('level', 'attributes')
    def __init__(self, *args, **kwargs):

        self.attributes = dict(self.base_attributes.items() + kwargs.get('attributes', {}).items())
        for a, v in self.attributes.items():
            setattr(self, a, v)

    def attribute_mod(self, attribute):
        return (getattr(self, attribute) / 2) - 5

class Character(BaseCharacter):

    race = None

    @autoassign('race')
    def __init__(self, *args, **kwargs):
        super(Character, self).__init__(*args, **kwargs)
        for a, v in self.race.attributes.items():
            setattr(self, a, getattr(self, a) + v) 