from xml.etree import ElementTree
import requests
import xmltodict
from classes.customer import CustomerCreationRequest

from utils.auth import requires_basic_auth
from flask import Flask, Response, request,send_file
from soap import app

@app.route("/notifyCustomerCreationRequest", methods=["POST"])
@requires_basic_auth
def customer_creation_request():
    """
    This endpoint responds with a custom XML message.
    """
    data = xmltodict.parse(request.data.decode("utf-8"))
    customer = CustomerCreationRequest(data)
    xml = customer.soap_response()

    return Response(xml, mimetype="text/xml")

@app.route("/updateCustomerRequest", methods=["POST"])
@requires_basic_auth
def update_customer():
    data = xmltodict.parse(request.data.decode("utf-8"))
    customer = CustomerCreationRequest(data)
    xml = customer.soap_response()

    return Response(xml, mimetype="text/xml")

@app.route("/CustomerServices", methods=["GET"])
def CustomerServices():
    return send_file("static/CustomerServices.wsdl", mimetype="text/xml")

@app.route("/schemas/CustomerServices.xsd", methods=["GET"])
def CustomerServices_schema():
    return send_file("static/schema/CustomerServices.xsd", mimetype="text/xml")

@app.route("/DataModel/AcecCustomer.xsd", methods=["GET"])
def AcecCustomer():
    return send_file("static/DataModel/AcecCustomer.xsd", mimetype="text/xml")