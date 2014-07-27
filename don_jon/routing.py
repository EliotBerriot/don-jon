
class Unlimited:
    pass
    
class NoReverseMatch(Exception):
    pass

class Route(object):

    def __init__(self, view, name, accepted_kwargs=Unlimited):
        self._view = view
        self.name = name
        self.accepted_kwargs = accepted_kwargs

    def view(self, **kwargs):
        if self.accepted_kwargs == Unlimited:
            # view accept any number of args
            return self._view(**kwargs)

        elif self.accepted_kwargs == None:
            if len(kwargs) == 0:
                # view accepts no args
                return self._view()

            else:
                raise NoReverseMatch(
                    "View for route '{0}' does not take any arguments".format(self.name)                     
                )
        else:
            for key in kwargs:
                try:
                    self.accepted_kwargs.accepted_kwargs

                except ValueError:
                    raise NoReverseMatch(
                    "View for route '{0}' does not take any argument '{2}'".format(
                        self.name, key
                        )                     
                    )
            return self._view(**kwargs)


    