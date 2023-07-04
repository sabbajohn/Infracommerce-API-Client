from .resource import Resource
class Supplier(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__("catalog/admin/","suppliers", *args, **kwargs)