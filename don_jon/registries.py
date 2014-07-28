from persisting_theory import Registry

class ManagedAttributes(Registry):

    look_into = None    

    

class Modifiers(Registry):

    look_into = None


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


from routing import Route

class Routes(Registry):

    look_into = "routes"

    def prepare_name(self, data, name=None):
        return data.name

    def validate(self, data):
        if isinstance(data, Route):
            return True
        return False

routes = Routes()
