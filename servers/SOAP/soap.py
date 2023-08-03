from xml.etree import ElementTree

import requests
import xmltodict
from classes.customer import CustomerCreationRequest
from classes.orders import OrderRequest
from classes.payments import PaymentRequest
from flask import Flask, Response, request
from utils.auth import requires_basic_auth

app = Flask(__name__)


@app.route("/notifyCustomerCreationRequest", methods=["POST"])
@requires_basic_auth
def notify_customer_creation_request():
    """
    This endpoint responds with a custom XML message.
    """
    data = xmltodict.parse(request.data.decode("utf-8"))
    customer = CustomerCreationRequest(data)
    xml = customer.soap_response()

    return Response(xml, mimetype="text/xml")


@app.route("/integrateOrder", methods=["POST"])
@requires_basic_auth
def integrate_order_request():
    """
    This endpoint responds with a custom XML message.
    """
    data = xmltodict.parse(request.data.decode("utf-8"))
    order = OrderRequest(data)
    xml = order.save()

    return Response(xml, mimetype="text/xml")


@app.route("/confirmPaymentRequest", methods=["POST"])
@requires_basic_auth
def confirm_payment_request():
    data = xmltodict.parse(request.data.decode("utf-8"))
    payment = PaymentRequest(data)
    xml = payment.save()
    return Response(xml, mimetype="text/xml")


@app.route("/wsdl")
def wsdl():
    """
    This endpoint returns the WSDL document for the service.
    """
    wsdl = """
        ...  # WSDL content goes here
    """
    return Response(wsdl, mimetype="text/xml")


if __name__ == "__main__":
    app.run(port=8080)
