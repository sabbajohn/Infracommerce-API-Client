from copy import deepcopy
from xml.etree import ElementTree
from datetime import datetime


class CustomerCreationRequest:
    def __init__(self, request):
        self.request = request

        customer = request["soapenv:Envelope"]["soapenv:Body"]["cus:notifyCustomerCreationRequest"][
            "customer"
        ]
        self.Customer = Customer(**customer)

    def save(self):
        valid = self.is_valid()
        if isinstance(valid, list):
            return valid
        else:
            # Save to database
            # ...
            pass

        return True

    def soap_response(self):
        request = deepcopy(self.request)
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


class Customer:
    def __init__(self, *args, **kwargs):
        if kwargs.get("customerId"):
            for key, value in kwargs.items():
                setattr(self, key, value)
            return
        self.documentNr = self.validate_string(kwargs.get("documentNr", None), 15, True)
        self.name = self.validate_string(kwargs.get("name", None), 100, True)
        self.email = self.validate_string(kwargs.get("email", None), 255, True)
        self.stateSubscription = kwargs.get("stateSubscription", "")
        self.representativeNm = kwargs.get("representativeNm", "")
        self.createDate = kwargs.get("createDate", datetime.now())

        if type(kwargs["addressList"]["address"]) is list:
            self.addressList = [
                Address(**addr) for addr in kwargs["addressList"].get("address", [])
            ]
        else:
            self.addressList = [Address(**kwargs["addressList"].get("address", {}))]
        if type(kwargs["phoneList"]["phone"]) is list:
            self.phoneList = [Phone(**phone) for phone in kwargs["phoneList"].get("phone", [])]
        else:
            self.phoneList = [Phone(**kwargs["phoneList"].get("phone", {}))]

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

        if not self.documentNr:
            failed_fields.append("documentNr")
        if not self.name:
            failed_fields.append("name")
        if not self.email:
            failed_fields.append("email")

        for index, address in enumerate(self.addressList):
            if not address.is_valid():
                failed_fields.append(f"addressList[{index}]")

        for index, phone in enumerate(self.phoneList):
            if not phone.is_valid():
                failed_fields.append(f"phoneList[{index}]")

        if failed_fields:
            return failed_fields
        else:
            return True


class Address:
    def __init__(
        self,
        recipientNm="",
        address="",
        addressNr="",
        additionalInfo="",
        quarter="",
        city="",
        state="",
        postalCd="",
        addressId=None,
        **kwargs,
    ):
        if kwargs.get("addressId"):
            for key, value in kwargs.items():
                setattr(self, key, value)
            return
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
        return all(
            [
                self.recipientNm,
                self.address,
                self.addressNr,
                self.quarter,
                self.city,
                self.state,
                self.postalCd,
            ]
        )


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
        return all([self.phoneTp, self.areaCd])
