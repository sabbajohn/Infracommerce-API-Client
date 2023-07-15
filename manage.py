from werkzeug.middleware.dispatcher import DispatcherMiddleware

from spyne.server.wsgi import WsgiApplication

from apps.spyne import spyned
from apps.flask_app.flasked import app


# SOAP services are distinct wsgi applications, we should use dispatcher
# middleware to bring all aps together
app.app.wsgi_app = DispatcherMiddleware(app.app.wsgi_app, {
        '/soap': WsgiApplication(spyned.create_app(app))
})


if __name__ == '__main__':
    app.run()