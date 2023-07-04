from .resource import Resource

# Just create and List
class Inventories(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__("ihub/","inventories", *args, **kwargs)
