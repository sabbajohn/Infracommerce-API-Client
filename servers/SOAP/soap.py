from xml.etree import ElementTree

import xmltodict
from classes.customer import CustomerCreationRequest
# from classes.orders import OrderRequest
from classes.payments import PaymentRequest
from flask import Flask, Response, request
# from utils.auth import requires_basic_auth

app = Flask(__name__)
from services.order_services import *
from services.customer_services import *
from services.payment_services import *

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=4443,  # Change this to the desired port number for your HTTPS server
        ssl_context=("certs/Mondelez_test.crt", "certs/ca.key")
    )
