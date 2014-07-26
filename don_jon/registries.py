from persisting_theory import Registry


class Attributes(Registry):

    look_into = "builtin_attributes"

    def prepare_data(self, data):
        return data()

    def prepare_name(self, data, name=None):
        return data.clsname()

attributes = Attributes()

class SpecificAttributes(Attributes):

   pass

class Races(Registry):

    look_into = "races"
    
    def prepare_name(self, data, name=None):
        return data.clsname()

races = Races()

