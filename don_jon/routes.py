import views
from registries import routes
from routing import Route

routes.register(Route(views.TestOne, name='test.one', accepted_kwargs=['data', 'something']))
routes.register(Route(views.CharacterCreate, name='character.create'))
routes.register(Route(views.CharacterList, name='character.list'))
