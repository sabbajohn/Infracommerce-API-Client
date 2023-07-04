from .resource import Resource


class Category(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__("catalog/admin/","categories", *args, **kwargs)