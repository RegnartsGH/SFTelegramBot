import requests
import json
from config import exchanges


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            sym_key = exchanges[sym.lower()]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {sym}')

        if base_key == sym_key:
            raise APIException(f'Невозможно конвертировать одинаковые валюты {base}.')

        try:
            amount = float(amount.replace(",", "."))
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        r = requests.get(
            f"https://min-api.cryptocompare.com/data/price?api_key=161263f4191306b0fa0e2cdb8532611c91ccf3a89cbdb873347b1cc14eed5571&fsym={base_key}&tsyms={sym_key}")
        resp = json.loads(r.content)
        new_price = resp[sym_key] * float(amount)
        return round(new_price, 2)