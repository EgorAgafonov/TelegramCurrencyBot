import json
import requests
import easyocr
from settings import *


class ConvertionException(Exception):
    pass


class CryptoConverter:

    @staticmethod
    def convert(token: str, quantity: str, base_code: str, target_code: str, ) -> object:
        """Метод отправки GET-запроса для предоставления сведений о стоимости(amount) одной/нескольких единиц базовой
        валюты(base_code) по отношению к целевой валюте(target_code), т.е. стоимость покупки одной валюты в
        единицах другой."""

        base_url = "https://v6.exchangerate-api.com/v6/"
        response = requests.get(base_url + token + "pair/" + f"{base_code}/" + f"{target_code}/" + str(quantity))

        status = response.status_code
        result = ""
        try:
            result = response.json()
        except json.JSONDecodeError:
            result = response.text

        try:
            check_1 = float(quantity)
            check_2 = quantity.isdigit()
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
            check_2 = base_code.isalpha()
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
                                      f"'{target_code}'.\n"
                                      f"Список поддерживаемых валют доступен по команде '/values' .")

        return status, result


class TextImageReader:

    @staticmethod
    def text_recognition(file_path) -> str:
        reader = easyocr.Reader(['ru', "en"])
        result = reader.readtext(file_path, detail=0, paragraph=True)
        recognized_string = '\n'.join(result)
        return recognized_string




