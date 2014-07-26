from attributes import DefaultAttributesManager

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

    def __init__(self, *args, **kwargs):
        self.attributes = DefaultAttributesManager(character=self, **kwargs)
        

class Character(BaseCharacter):

    race = None

    def __init__(self, *args, **kwargs):
        super(Character, self).__init__(*args, **kwargs)
        # for a, v in self.race.attributes.items():
        #     setattr(self, a, getattr(self, a) + v) 