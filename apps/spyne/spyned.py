from spyne import (
    Application,
    Array,
    ComplexModel,
    Date,
    Integer,
    Iterable,
    ServiceBase,
    String,
    Unicode,
    rpc,
)
from spyne.protocol.http import HttpRpc
from spyne.protocol.json import JsonDocument
from spyne.protocol.soap import Soap11,Soap12


class Customer(ComplexModel):
    name = String
    email = String
    documenNr = String
    createDate = String
    stateSubscription = String

class InfracommerceService(ServiceBase):
    @rpc(Unicode, Integer, _returns=Iterable(Unicode))
    def hello(ctx, name, times):
        name = name or ctx.udc.config['HELLO']
        for i in range(times):
            yield u'Hello, %s' % name

    @rpc(Unicode, Integer, _returns=Iterable(Unicode))
    def bye(ctx, name, times):
        name = name or ctx.udc.config['HELLO']
        for i in range(times):
            yield u'Bye, %s' % name
    
    @rpc(Customer, _returns=(Customer))
    def notifyCustomerCreationRequest(ctx, customer):
        data = customer.as_dict()
        return data


class UserDefinedContext(object):
    def __init__(self, flask_config):
        self.config = flask_config


def create_app(flask_app):
    """Creates SOAP services application and distribute Flask config into
    user con defined context for each method call.
    """
    application = Application(
        [InfracommerceService], 'customer', 
        # The input protocol is set as HttpRpc to make our service easy to call.
        in_protocol=Soap11(validator='soft',ns_clean=True),
        out_protocol=Soap11(),
    )

    # Use `method_call` hook to pass flask config to each service method
    # context. But if you have any better ideas do it, make a pull request.
    # NOTE. I refuse idea to wrap each call into Flask application context
    # because in fact we inside Spyne app context, not the Flask one.
    def _flask_config_context(ctx):
        ctx.udc = UserDefinedContext(flask_app)
    application.event_manager.add_listener('method_call', "_flask_config_context")

    return application