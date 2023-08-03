from xml.etree import ElementTree

class PaymentRequest:
    def __init__(self, request):
        payment = request["soapenv:Envelope"]["soapenv:Body"]["confirmPaymentRequest"]
        for key, value in payment.items():
                setattr(self, key, value)

    def save(self):
        # Update the Order status and Proceed the process
        try:
            # Save the payment details in the database
            pass
        except Exception as e:
            # Log the exception
            return self.__soap_response(False)
        else:
            return self.__soap_response(True)
    
    @staticmethod
    def __soap_response(status):
        root = ElementTree.Element("env:Envelope")
        root.set("xmlns:env", "http://schemas.xmlsoap.org/soap/envelope/")
        root.set("xmlns:wsa","http://www.w3.org/2005/08/addressing")

        body = ElementTree.SubElement(root, "env:Body")
        resp = ElementTree.SubElement(body, "confirmPaymentResponse")
        resp.set("xmlns", "http://www.accurate.com/acec/PaymentServices")
        success = ElementTree.SubElement(resp, "success")
        success.text = str(status)

        xml_response = ElementTree.tostring(root, encoding="utf-8", method="xml")
        return xml_response.decode()