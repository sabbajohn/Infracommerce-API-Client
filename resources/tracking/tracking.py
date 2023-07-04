from .resource import Resource

# PUT/UPDATE Ack feed
# GET Get tracking feed
class Tracking(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__("ihub/","trackings/feed", *args, **kwargs)
