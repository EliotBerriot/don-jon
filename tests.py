import unittest
from don_jon.chars import BaseCharacter, Character, CharacterGenerator
from don_jon.races import Elf, Human
from don_jon.attributes import DefaultAttributesManager
from don_jon.registries import attributes, races
from PySide import QtGui
import sys

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


    def test_character_generator(self):
        g = CharacterGenerator(race=Elf)
        c1 = g.create()
        self.assertEqual(c1.attributes('race').value, Elf)


    def test_can_override_character_generator_defaults(self):
        g = CharacterGenerator(race=Elf)
        c1 = g.create(level=12)
        self.assertEqual(c1.attributes('level').value, 12)

class FormsTestCase(unittest.TestCase):

    def test_can_build_field_from_attribute(self):
        field = attributes.get('race').form_field()
        self.assertEqual(field.initial[0], Elf)

    def test_can_retrieve_value_from_single_choice_field(self):
        field = attributes.get('race').form_field()

        self.assertEqual(field.currentText(), 'Elfe')
        self.assertEqual(field.value, Elf)

    def test_can_update_single_choice_field(self):

        field = attributes.get('race').form_field()

        field.value = Human
        self.assertEqual(field.currentText(), "Humain")



if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    unittest.main()