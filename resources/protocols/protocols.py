from resources import Resource




class _Refund(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__("ihub/","finance/refunds", *args, **kwargs)
    
    def list(self):
        self.override_endpoint("finance/refunds/feed")
        super.list()


# CREATE, GET
class Protocols(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__("ihub/","orders/protocols", *args, **kwargs)
        self.Refund = _Refund()
