import unittest
import sys
import os

if __name__ == "__main__":

    if __package__ is None:
        sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
        

from don_jon.models import Character, CharacterGenerator
from don_jon.races import Elf, Human
from don_jon.registries import attributes, races, routes
from don_jon.forms import CharacterForm
from don_jon.utils import reverse
from don_jon import gui
from don_jon.settings import test_database, Base

from sqlalchemy.orm import sessionmaker
from PySide import QtGui


class CharacterTestCase(unittest.TestCase):

    def setUp(self):
        Base.metadata.create_all(test_database) 
        self.session = sessionmaker(bind=test_database)()


    def test_can_get_attribute_base_value(self):
        b = Character(strength=14)
        self.assertEqual(b.attributes.strength.base_value, 14)


    def test_can_get_attribute_modifier(self):

        b = Character(strength=14)
        self.assertEqual(b.attributes.strength.mod, 2)

        b.attributes.intelligence.base_value = 20
        self.assertEqual(b.attributes.intelligence.mod, 5)

        b.attributes.intelligence.base_value = 21
        self.assertEqual(b.attributes.intelligence.mod, 5)

        b.attributes.intelligence.base_value = 1
        self.assertEqual(b.attributes.intelligence.mod, -5)

    def test_can_persist_character_to_db(self):
        b = Character(strength=14, charisma=666)
        self.session.add(b)

        q = self.session.query(Character).filter(Character.charisma==666).first()
        self.assertEqual(q, b)

    def test_can_query_using_classic_operators(self):

        a = Character(intelligence=14, level=6)
        b = Character(intelligence=16, level=9)
        c = Character(intelligence=18, level=12)
        d = Character(intelligence=20, level=15)
        self.session.add_all((a, b, c, d))
        self.session.commit()

        q = self.session.query(Character).filter(Character.level>=9).count()
        self.assertEqual(q, 3)

        q = self.session.query(Character).filter(Character.level>=9, Character.intelligence==20).count()
        self.assertEqual(q, 1)

        q = self.session.query(Character).filter(Character.level<=9, Character.intelligence==16).count()
        self.assertEqual(q, 1)

    def test_can_save_character_race_via_foreign_key(self):
        a = Character(race="elf")
        self.session.add(a)
        self.session.commit()
        q = self.session.query(Character).filter(Character.race=='elf')
        self.assertEqual(q[0], a)

    def test_character_modified_attributes_values_are_persisted_in_database(self):
        a = Character(dexterity=15, constitution=12, race="elf")
        self.assertEqual(a.attributes.dexterity.value, 17)
        self.assertEqual(a.attributes.constitution.value, 10)
        self.session.add(a)
        self.session.commit()
        q = self.session.query(Character).filter(Character.dexterity==17)
        self.assertEqual(q[0], a)

    def test_attribute_value_are_also_accessible_directly_from_instance(self):
        b = Character(strength=14, charisma=32)
        self.assertEqual(b.attributes.strength.base_value, 14)
        self.assertEqual(b.strength, 14)
        self.assertEqual(b.charisma, 32)

    def test_can_autoassign_instance_attributes(self):
        b = Character(level=12)
        self.assertEqual(b.attributes.level.base_value, 12)


    def test_attributes_objects_can_declare_modifiers_on_other_attributes(self):

        b = Character(dexterity=19, constitution=15)

        self.assertEqual(b.attributes.armor_class.value, 10 + b.attributes.dexterity.mod)

    def test_race_add_modifiers(self):
        b = Character(race="elf", dexterity=19, constitution=15)
        self.assertEqual(b.attributes.dexterity.value, 21)
        self.assertEqual(b.attributes.constitution.value, 13)

    def test_character_generator(self):
        g = CharacterGenerator(race="elf")
        c1 = g.create()
        self.assertEqual(c1.attributes.race.raw_value, Elf)

    def test_can_override_character_generator_defaults(self):
        g = CharacterGenerator(race="elf")
        c1 = g.create(level=12)
        self.assertEqual(c1.attributes.level.base_value, 12)

    def test_can_use_route(self):
        r = reverse('test.one', data="test", something="hello")
        self.assertEqual(r, {"data":"test", "something":"hello"})

        from don_jon.routing import NoReverseMatch
        with self.assertRaises(NoReverseMatch):
            r = reverse('test.one', data="test", something="hello", error="yeah")

    def test_modifiers_are_properly_registered_for_each_character(self):
        b = Character(race="elf", dexterity=19, constitution=15)
        self.assertEqual(b.attributes.get('dexterity').modifiers.get('race'), Elf.modify.get('dexterity'))

    def test_can_get_modifier_value_per_attribute(self):
        b = Character(race="elf", dexterity=19, constitution=15)
        self.assertEqual(b.attributes.get('dexterity').modifiers_descriptions, [("race", 2)])
        self.assertEqual(b.attributes.get('constitution').modifiers_descriptions, [("race", -2)])
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

    def test_can_create_character_from_form(self):

        form = CharacterForm()
        form.fields['race'].value = Human
        form.fields['level'].value = 26
        character = form.process()
        self.assertEqual(character.attributes.race.raw_value, Human)
        self.assertEqual(character.attributes.level.base_value, 26)

if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    unittest.main()