import requests
import json
from config import currencies


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(base, quote, amount):
        if base not in currencies:
            raise APIException("Неизвестная валюта")

        if quote not in currencies:
            raise APIException("Неизвестная валюта")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException("Количество должно быть числом")

        url = (
            f"https://api.exchangerate.host/convert"
            f"?from={currencies[base]}"
            f"&to={currencies[quote]}"
            f"&amount={amount}"
        )

        response = requests.get(url)
        data = json.loads(response.text)

        return data["result"]
