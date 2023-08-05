from xml.etree import ElementTree
import requests
import xmltodict
from classes.orders import OrderRequest
from utils.auth import requires_basic_auth
from flask import Flask, Response, request,send_file
from soap import app

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

@app.route("/integrateOrder", methods=["GET"])
def integrateOrder_wsdl():
    return send_file("static/OrderIntegration.wsdl", mimetype="text/xml")

@app.route("/schemas/BOOrderIntegration.xsd", methods=["GET"])
def boOrderIntegration():
    return send_file("static/schema/BOOrderIntegration.xsd", mimetype="text/xml")

@app.route("/DataModel/AcecOrder.xsd", methods=["GET"])
def AcecOrder():
    return send_file("static/DataModel/AcecOrder.xsd", mimetype="text/xml")