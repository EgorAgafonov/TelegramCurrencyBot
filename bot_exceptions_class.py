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
        try:
            float(quantity)
        except ValueError:
            raise ConvertionException(f"Ошибка!\n"
                                      f"Указанное значение: '{quantity}' не является числом.")

        if base_code == target_code:
            raise ConvertionException(f"Ошибка!\nУказаны две одинаковые валюты или числовое значение вместо "
                                      f"буквенного.\n"
                                      f"Логика вышла из чата😜.\n "
                                      f"Вот корректный пример ввода: '100 USD RUB'")
        try:
            check_1 = keys[base_code]
            check_1 = base_code.isalpha()
        except KeyError:
            raise ConvertionException(f"Ошибка!\n"
                                      f"Указан неверный код валюты или числовое значение вместо буквенного: "
                                      f"{base_code}.\n"
                                      f"Список поддерживаемых валют доступен по команде '/values' .")
        try:
            check_1 = keys[target_code]
            check_2 = target_code.isalpha()
        except KeyError:
            raise ConvertionException(f"Ошибка!\n"
                                      f"Указан неверный код валюты или числовое значение вместо буквенного: "
                                      f"'{base_code}'.\n"
                                      f"Список поддерживаемых валют доступен по команде '/values' .")

        return result['conversion_result']




