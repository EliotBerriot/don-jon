import unittest
from chars import BaseCharacter, Character
from races import Elf
from attributes import DefaultAttributesManager


class CharacterTestCase(unittest.TestCase):


    def test_can_get_attribute_modifier(self):

        b = BaseCharacter(strength=14)
        self.assertEqual(b.attributes('strength').mod, 2)

        b.attributes('intelligence').value = 20
        self.assertEqual(b.attributes('intelligence').mod, 5)

        b.attributes('intelligence').value = 21
        self.assertEqual(b.attributes('intelligence').mod, 5)

        b.attributes('intelligence').value = 1
        self.assertEqual(b.attributes('intelligence').mod, -5)

    def test_can_autoassign_instance_attributes(self):
        b = BaseCharacter(level=12)
        self.assertEqual(b.attributes("level").value, 12)


    def test_attributes_objects_can_declare_modifiers_on_other_attributes(self):

        b = Character(dexterity=19, constitution=15)

        self.assertEqual(b.attributes('armor_class').value, 10 + b.attributes('dexterity').mod)

    def test_can_access_attributemanager_keys_as_instance_attributes(self):
        b = Character(race=Elf)
        d = DefaultAttributesManager(character=b)
        self.assertEqual(d('strength').value, 10)

    def test_race(self):

        b = Character(race=Elf, dexterity=19, constitution=15)
        self.assertEqual(b.attributes('dexterity').value, 21)
        self.assertEqual(b.attributes('constitution').value, 13)


if __name__ == "__main__":
    unittest.main()