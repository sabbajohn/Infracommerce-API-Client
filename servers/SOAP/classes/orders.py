from .customer import Address, Customer
from xml.etree import ElementTree

class OrderRequest:
    def __init__(self, request):
        self.request = request
        self.Order = Order(
            request["soapenv:Envelope"]["soapenv:Body"]["boor:integrateOrderRequest"]["order"]
        )

    def save(self):
        valid = self.is_valid()
        if valid:
            # Save to database
            # ...
            pass

        return True

    def soap_response(self):
        root = ElementTree.Element("env:Envelope")
        root.set("xmlns:env", "http://schemas.xmlsoap.org/soap/envelope/")

        body = ElementTree.SubElement(root, "env:Body")
        resp = ElementTree.SubElement(body, "integrateOrderResponse")
        resp.set("xmlns", "http://www.accurate.com/acec/AcecBOSOAIntegration/BOOrderIntegration")
        status = ElementTree.SubElement(resp, "status")
        status.text = "OK"

        message = ElementTree.SubElement(resp, "message")
        if self.Order.new_order:
            message.text = "Pedido integrado com sucesso"
        else:
            message.text = "Pedido já existe no ERP"

        xml_response = ElementTree.tostring(root, encoding="utf-8", method="xml")
        return xml_response.decode()


class Order:
    def __init__(self, order):
        self.OrderId = order.get("orderId")
        # TODO: Check if this order is already integrated
        self.new_order = True

        self.total_amount = order.get("totalAmount")
        self.total_discount_amount = order.get("totalDiscountAmount")
        self.purchase_date = order.get("purchaseDate")
        self.session_creation_date = order.get("sessionCreationDate")
        self.application_version = order.get("applicationVersion")
        self.list_id = order.get("listId")
        self.sale_channel = order.get("saleChannel")
        self.sales_operator_id = order.get("salesOperatorId")
        self.sales_operator_name = order.get("salesOperatorName")
        self.purchase_order = order.get("purchaseOrder")
        self.origin = order.get("origin")

        self.deliveries = (
            Delivery(**deliv) for deliv in order["deliveries"].get("delivery", [])
        ) if isinstance(order["deliveries"]["delivery"], list) else [
            Delivery(**order["deliveries"].get("delivery", {}))]
        
        self.customer = (
            Customer(**customer) for customer in order.get("customer", [])
        ) if isinstance(order["customer"], list) else [
            Customer(**order.get("customer", {}))]

        self.billing_address = (
            Address(**addr) for addr in order.get("billingAddress", [])
        ) if isinstance(order["billingAddress"], list) else [
            Address(**order.get("billingAddress", {}))]

        self.payment_list = (
            Payment(payment) for payment in order.get("PaymentList", {}).get("payment", [])
        ) if isinstance(order["paymentList"]["payment"], list) else [
            Payment(order.get("paymentList", {}).get("payment", {}))]

        self.freight_charged_amount = order.get("freightChargedAmount")
        self.freight_actual_amount = order.get("freightActualAmount")
        self.count_distinct_sku = order.get("countDistinctSku")


class Delivery:
    def __init__(
        self,
        orderId,
        deliveryId,
        totalAmount,
        totalDiscountAmount,
        orderLineList,
        freightAmount,
        deliveryAddress,
        *args,
        **kwargs,
    ):
        self.orderId = orderId
        self.deliveryId = deliveryId
        self.totalAmount = float(totalAmount)
        self.totalDiscountAmount = float(totalDiscountAmount)
        self.orderLineList = (
            OrderLine(**order_line) for order_line in orderLineList.get("orderLine", [])
        ) if isinstance(orderLineList["orderLine"], list) else [
            OrderLine(**orderLineList.get("orderLine", {}))]

        self.freightAmount = Freight(**kwargs.get("freightAmount", {}))
        self.deliveryAddress = deliveryAddress


class OrderLine:
    def __init__(self, *args, **kwargs):
        self.sku = kwargs.get("sku", None)
        self.skuType = kwargs.get("skuType", None)
        self.quantity = kwargs.get("quantity", None)
        self.catalogListPrice = kwargs.get("catalogListPrice", None)
        self.listPrice = kwargs.get("listPrice", None)
        self.salePrice = kwargs.get("salePrice", None)
        self.unconditionalDiscountAmount = kwargs.get("unconditionalDiscountAmount", None)
        self.roundingDiscountAmount = kwargs.get("roundingDiscountAmount", None)
        if kwargs["promotionList"]:
            self.promotionList = (
                Promotion(**promotion) for promotion in kwargs.get("promotionList", {}).get("promotion", [])
            ) if isinstance(kwargs["promotionList"]["promotion"], list) else [
                Promotion(**kwargs.get("promotionList", {}).get("promotion", {}))]
        
        self.freight = Freight(**kwargs.get("freight", {}))
        self.kitSkuId = kwargs.get("kitSkuId", "")
        self.kitSkuName = kwargs.get("kitSkuName", "")
        self.kitQuantity = kwargs.get("kitQuantity", 0)
        self.service = kwargs.get("service", None)
        self.skuName = kwargs.get("skuName", None)


class Promotion:
    def __init__(self, *args, **kwargs):
        self.promotionId = kwargs.get("promotionId", None)
        self.promotionName = kwargs.get("promotionName", None)
        self.promotionStartDate = kwargs.get("promotionStartDate", None)
        self.promotionEndDate = kwargs.get("promotionEndDate", None)
        self.campaignId = kwargs.get("campaignId", None)
        self.label = kwargs.get("label", None)
        self.type = kwargs.get("type", None)
        self.amount = kwargs.get("amount", None)
        self.roundingAmount = kwargs.get("roundingAmount", 0.0)
        self.minimumQuantity = kwargs.get("minimumQuantity", 0)
        self.couponPromo = kwargs.get("couponPromo", False)


class Freight:
    def __init__(self, *args, **kwargs):
        self.chargedAmount = kwargs.get("chargedAmount", None)
        self.actualAmount = kwargs.get("actualAmount", None)
        self.commercialAmount = kwargs.get("commercialAmount", None)
        self.freightTime = kwargs.get("freightTime", None)
        self.pickupLeadTime = kwargs.get("pickupLeadTime", None)
        self.logisticContract = kwargs.get("logisticContract", None)
        self.expectedDeliveryDate = kwargs.get("expectedDeliveryDate", None)
        self.adjustedDeliveryDate = kwargs.get("adjustedDeliveryDate", None)


class Payment:
    def __init__(self, payment):
        if "abstractPayment" in payment:
            for key, value in payment["abstractPayment"].items():
                setattr(self, key, value)
        elif "creditCardPayment" in payment:
            for key, value in payment["creditCardPayment"].items():
                setattr(self, key, value)
