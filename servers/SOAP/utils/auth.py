from functools import wraps

from flask import Response, request


def check_credentials(username, password):
    # Implement your logic to validate the credentials here
    # You can store the username and password securely in a database or other storage mechanism
    # Return True if the credentials are valid, False otherwise
    return username == "john" and password == "123456"


def requires_basic_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_credentials(auth.username, auth.password):
            return Response(
                "Unauthorized", 401, {"WWW-Authenticate": 'Basic realm="Login Required"'}
            )
        return f(*args, **kwargs)

    return decorated
