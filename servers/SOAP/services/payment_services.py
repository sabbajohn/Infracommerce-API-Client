from xml.etree import ElementTree
import requests
import xmltodict

from classes.payments import PaymentRequest
from utils.auth import requires_basic_auth
from flask import Flask, Response, request,send_file
from soap import app


@app.route("/confirmPaymentRequest", methods=["POST"])
@requires_basic_auth
def confirm_payment():
    data = xmltodict.parse(request.data.decode("utf-8"))
    payment = PaymentRequest(data)
    xml = payment.save()
    return Response(xml, mimetype="text/xml")


@app.route("/PaymentServices", methods=["GET"])
def PaymentServices():
    return send_file("static/PaymentServices.wsdl", mimetype="text/xml")

@app.route("/schemas/PaymentServices.xsd", methods=["GET"])
def schema_paymentServices():
    return send_file("static/schema/PaymentServices.xsd", mimetype="text/xml")

@app.route("/schemas/ErrorLog.xsd", methods=["GET"])
def schema_errorLog():
    return send_file("static/schema/ErrorLog.xsd", mimetype="text/xml")

