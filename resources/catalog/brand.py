from .resource import Resource


class Brand(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__("catalog/admin/","brands", *args, **kwargs)
