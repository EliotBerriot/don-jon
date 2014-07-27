from views import TestOne
from registries import routes
from routing import Route

routes.register(Route(TestOne, name='test.one'))

