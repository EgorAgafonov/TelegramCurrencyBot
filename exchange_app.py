import json
import requests


class ExchangeRateAPI:
    """Класс с методами отправки запросов на API-сервис https://v6.exchangerate-api.com/
    (информация о текущих курсах мировых валют)."""

    def __init__(self):
        self.base_url = "https://v6.exchangerate-api.com/v6/"

    def get_exchange_rate(self, api_key: str, currency_code: str):
        """Метод стандартного GET-запроса для предоставления сведений о курсах мировых валют по отношению к выбранной
        единице базовой валюты. В качестве значения аргумента currency_code необходимо указать строковый код валюты
        согласно стандарта ISO 4217."""

        response = requests.get(self.base_url + api_key + "latest/" + currency_code)

        status = response.status_code
        result = ""
        try:
            result = response.json()
        except json.JSONDecodeError:
            result = response.text

        return status, result

    def conversion_of_currency_pair(self, api_key: str, base_code: str, target_code: str, amount=None) -> object:
        """Метод отправки GET-запроса для предоставления сведений об отношении обменного курса целевой валюты
        (target_code) по отношению к одной единице базовой валюте(base_code). """

        if not amount:
            response = requests.get(self.base_url + api_key + "pair/" + f"{base_code}/" + f"{target_code}")
        else:
            response = requests.get(self.base_url + api_key + "pair/" + f"{base_code}/" + f"{target_code}/"
                                    + str(amount))

        status = response.status_code
        result = ""
        try:
            result = response.json()
        except json.JSONDecodeError:
            result = response.text

        return status, result
