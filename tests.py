import unittest
from chars import BaseCharacter, Character
from races import Elf

class CharacterTestCase(unittest.TestCase):

    def test_can_override_character_attributes(self):

        b = BaseCharacter()
        self.assertEqual(b.strength, b.base_attributes.get('strength'))

        b = BaseCharacter(attributes={"strength": 42})
        self.assertEqual(b.strength, 42)


    def test_can_get_attribute_modifier(self):

        b = BaseCharacter(attributes={"strength": 10})
        self.assertEqual(b.attribute_mod('strength'), 0)

        b.intelligence = 20
        self.assertEqual(b.attribute_mod('intelligence'), 5)

        b.intelligence = 21
        self.assertEqual(b.attribute_mod('intelligence'), 5)

        b.intelligence = 1
        self.assertEqual(b.attribute_mod('intelligence'), -5)

    def test_can_autoassign_instance_attributes(self):
        b = BaseCharacter(level=12)
        self.assertEqual(b.level, 12)


    def test_char_can_inherit_attribute_from_race(self):

        b = Character(race=Elf, attributes={"dexterity":19, "constitution": 15})

        # elves have +2 in dex and -2 in const
        self.assertEqual(b.dexterity, 21)
        self.assertEqual(b.constitution, 13)

if __name__ == "__main__":
    unittest.main()