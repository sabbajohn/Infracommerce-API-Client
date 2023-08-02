import copy
import json
import os
from xml.etree import ElementTree

import requests
import xmltodict
from classes.customer import CustomerCreationRequest
from classes.orders import OrderRequest
from flask import Flask, Response, request

app = Flask(__name__)

from datetime import datetime


@app.route("/notifyCustomerCreationRequest", methods=["POST"])
def notifyCustomerCreationRequest():
    """
    This endpoint responds with a custom XML message.
    """
    data = xmltodict.parse(request.data.decode("utf-8"))
    Customer = CustomerCreationRequest(data)
    xml = Customer.soap_response()

    return Response(
        xml, mimetype="text/xml"
    )  # Returns the custom XML message as the response with the specified mimetype


@app.route("/integrateOrderRequest", methods=["POST"])
def integrateOrderRequest():
    """
    This endpoint responds with a custom XML message.
    """
    data = xmltodict.parse(request.data.decode("utf-8"))
    Order = OrderRequest(data)
    xml = Order.soap_response()

    return Response(
        xml, mimetype="text/xml"
    )  # Returns the custom XML message as the response with the specified mimetype

@app.route("/wsdl")
def wsdl():
    """
    This endpoint returns the WSDL document for the service.
    """
    wsdl = """<?xml version="1.0" encoding="UTF-8"?>
    <wsdl:definitions xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"
                      xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
                      xmlns:tns="http://www.example.com/"
                      xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                      targetNamespace="http://www.example.com/">
        <wsdl:types>
            <xsd:schema targetNamespace="http://www.example.com/" elementFormDefault="qualified">
                <xsd:element name="name" type="xsd:string"/>
                <xsd:element name="greeting" type="xsd:string"/>
            </xsd:schema>
        </wsdl:types>
        <wsdl:service name="HelloWorld">
            <wsdl:port name="HelloWorld" binding="tns:HelloWorld">
                <soap:address location="http://localhost:8080/helloworld"/>
            </wsdl:port>
        </wsdl:service>

        <wsdl:message name="HelloWorldRequest">
            <wsdl:part name="name" type="xsd:string"/>
        </wsdl:message>

        <wsdl:message name="HelloWorldResponse">
            <wsdl:part name="greeting" type="xsd:string"/>
        </wsdl:message>

        <wsdl:types>
            <xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema">
                <xsd:element name="name" type="xsd:string"/>
                <xsd:element name="greeting" type="xsd:string"/>
            </xsd:schema>
        </wsdl:types>

    </wsdl:definitions>
    """
    return Response(wsdl, mimetype="text/xml")


if __name__ == "__main__":
    app.run(port=8080)
