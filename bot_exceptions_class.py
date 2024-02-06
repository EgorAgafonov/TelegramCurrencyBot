import telebot
from settings import *
from exchange_app import ExchangeRateAPI


class ConvertionException(Exception):
    pass


class CryptoConverter:

    @staticmethod
    def convert(quantity: str, base_code: str, target_code: str):

        currency_API = ExchangeRateAPI()

        status, result = currency_API.conversion_of_currency_pair(api_key, amount=quantity, base_code=base_code,
                                                                  target_code=target_code)

        if base_code == target_code:
            raise ConvertionException(f"Ошибка!\nУказаны две одинаковые валюты или числовое значение вместо "
                                      f"буквенного.\n"
                                      f"Логика вышла из чата😜.\n "
                                      f"Вот корректный пример ввода: '100 USD RUB'")
        try:
            keys[base_code]
            base_code.isalpha()
        except KeyError:
            raise ConvertionException(f"Ошибка!\nУказан неверный код валюты или числовое значение вместо буквенного: {base_code}.\n"
                                      f"Список поддерживаемых валют доступен по команде '/values' .")
        try:
            keys[target_code]
            target_code.isalpha()
        except KeyError:
            raise ConvertionException(f"Ошибка!\nУказан неверный код валюты или числовое значение вместо буквенного: {base_code}.\n"
                                      f"Список поддерживаемых валют доступен по команде '/values' .")

        try:
            float(quantity)
        except ValueError:
            raise ConvertionException(f"Ошибка!\n"
                                      f"Указанное значение: {quantity} не является числом.")

        return result['conversion_result']




