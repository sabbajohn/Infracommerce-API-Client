import copy
import json
import os
from xml.etree import ElementTree

import requests
import xmltodict
from flask import Flask, Response, request

app = Flask(__name__)

from datetime import datetime


class CustomerCreationRequest:
    def __init__(self, request):
        self.request = request
        customer = request["soapenv:Envelope"]["soapenv:Body"]["cus:notifyCustomerCreationRequest"][
            "customer"
        ]
        self.documentNr = self.validate_string(customer.get("documentNr", None), 15, True)
        self.name = self.validate_string(customer.get("name", None), 100, True)
        self.email = self.validate_string(customer.get("email", None), 255, True)
        self.stateSubscription = (
            customer.get("stateSubscription", None)
            if customer.get("stateSubscription", None)
            else ""
        )
        self.representativeNm = (
            customer.get("representativeNm", None) if customer.get("representativeNm", None) else ""
        )
        self.createDate = (
            customer.get("createDate", None) if customer.get("createDate", None) else datetime.now()
        )
        self.addressList = [Address(**addr) for addr in customer["addressList"].get("address", [])]
        self.phoneList = [Phone(**phone) for phone in customer["phoneList"].get("phone", [])]

    def validate_string(self, value, limit, required):
        if value:
            if len(value) > limit:
                raise ValueError(f"String exceeds limit of {limit} characters")
            return value
        elif required:
            raise ValueError("Value is required")
        else:
            return ""

    def is_valid(self):
        failed_fields = []

        # Check if all required fields are valid
        if not self.documentNr:
            failed_fields.append("documentNr")
        if not self.name:
            failed_fields.append("name")
        if not self.email:
            failed_fields.append("email")

        # Check address validity
        for index, address in enumerate(self.addressList):
            if not address.is_valid():
                failed_fields.append(f"addressList[{index}]")

        # Check phone validity
        for index, phone in enumerate(self.phoneList):
            if not phone.is_valid():
                failed_fields.append(f"phoneList[{index}]")

        if failed_fields:
            return failed_fields
        else:
            return True

    def save(self):
        # Check validity
        valid = self.is_valid()
        if isinstance(valid, list):
            return valid
        else:
            # Save to database
            # ...
            pass

        return True

    def soap_response(self):
        request = copy.deepcopy(self.request)
        del request["soapenv:Envelope"]["soapenv:Body"]["cus:notifyCustomerCreationRequest"][
            "customer"
        ]

        root = ElementTree.Element("soapenv:Envelope")
        envelope = request["soapenv:Envelope"]

        for key, value in envelope.items():
            if key.startswith("@"):
                attr_name = key.replace("@", "")
                root.set(attr_name, value)

        header = ElementTree.SubElement(root, "soapenv:Header")
        body = ElementTree.SubElement(root, "soapenv:Body")
        resp = ElementTree.SubElement(body, "cus:notifyCustomerCreationResponse")
        status = ElementTree.SubElement(resp, "cus:status")
        status.text = "PEN"

        xml_response = ElementTree.tostring(root, encoding="utf-8", method="xml")
        return xml_response.decode()


class Address:
    def __init__(
        self, recipientNm, address, addressNr, additionalInfo, quarter, city, state, postalCd
    ):
        self.recipientNm = self.validate_string(recipientNm, 100, True)
        self.address = self.validate_string(address, 100, True)
        self.addressNr = self.validate_string(addressNr, 10, True)
        self.additionalInfo = self.validate_string(additionalInfo, 100, False)
        self.quarter = self.validate_string(quarter, 80, True)
        self.city = self.validate_string(city, 60, True)
        self.state = self.validate_string(state, 2, True)
        self.postalCd = self.validate_string(postalCd, 8, True)

    def validate_string(self, value, limit, required):
        if value:
            if len(value) > limit:
                raise ValueError(f"String exceeds limit of {limit} characters")
            return value
        elif required:
            raise ValueError("Value is required")
        else:
            return ""

    def is_valid(self):
        # Check if all required fields are valid
        if not all(
            [
                self.recipientNm,
                self.address,
                self.addressNr,
                self.quarter,
                self.city,
                self.state,
                self.postalCd,
            ]
        ):
            return False

        return True


class Phone:
    def __init__(self, phoneTp, areaCd, phoneNr):
        self.phoneTp = self.validate_phone_type(phoneTp)
        self.areaCd = self.validate_string(areaCd, 4, True)
        self.phoneNr = phoneNr

    def validate_phone_type(self, value):
        if int(value) not in [1, 2]:
            raise ValueError("Invalid phone type. Valid values are 1 (Comercial) and 2 (Celular)")
        else:
            if int(value) == 1:
                return "COM"
            elif int(value) == 2:
                return "CEL"

    def validate_string(self, value, limit, required):
        if value:
            if len(value) > limit:
                raise ValueError(f"String exceeds limit of {limit} characters")
            return value
        elif required:
            raise ValueError("Value is required")
        else:
            return ""

    def is_valid(self):
        # Check if all required fields are valid
        if not all([self.phoneTp, self.areaCd]):
            return False

        return True


@app.route("/helloworld", methods=["POST"])
def helloworld():
    """
    This endpoint responds with a custom XML message.
    """
    data = xmltodict.parse(request.data.decode("utf-8"))
    Customer = CustomerCreationRequest(data)
    xml = Customer.soap_response()

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
