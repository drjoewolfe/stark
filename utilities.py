from decimal import Decimal

def get_int(text):
    return float(text.replace(',', ''))


def get_decimal(text):
    try:
        return Decimal(text.replace(',', ''))
    except:
        return 0