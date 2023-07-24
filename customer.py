from datetime import datetime
from resources import Customer
def get_timestamp():

    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


PEOPLE = {

    "Fairy": {

        "fname": "Tooth",

        "lname": "Fairy",

        "timestamp": get_timestamp(),

    },

    "Ruprecht": {

        "fname": "Knecht",

        "lname": "Ruprecht",

        "timestamp": get_timestamp(),

    },

    "Bunny": {

        "fname": "Easter",

        "lname": "Bunny",

        "timestamp": get_timestamp(),

    }

}


def list_all():
    return Customer().list()
def create(customer):
    return Customer().create(customer)