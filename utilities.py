import json
import easyocr
import requests
import segno
from dadata import Dadata
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
                                      f"{base_code}.\n")
        try:
            check_1 = keys[target_code]
            check_2 = target_code.isalpha()
        except KeyError:
            raise ConvertionException(f"Ошибка!\n"
                                      f"Указан неверный код валюты или числовое значение вместо буквенного: "
                                      f"'{target_code}'.\n")

        return status, result


class RequestsToEGRYUL:
    @staticmethod
    def find_org_by_name(organization_data):
        dadata = Dadata(TOKEN_DADATA)
        response = dadata.suggest('party', organization_data)
        # metro = response[0].get("data").get("address").get("data").get("metro")

        # print(response[0].get("data").get('name').get("full_with_opf"))  # полное наименование ЮЛ
        # print(response[0].get("value"))  # краткое наименование
        # print(response[0].get("data").get('inn'))  # ИНН
        # print(response[0].get("data").get('kpp'))  # КПП
        # print(response[0].get("data").get('ogrn'))  # ОГРН
        # print(datetime.datetime.fromtimestamp(((response[0].get("data").get('state').get("registration_date")) / 1000)))
        # # Дата регистрации
        # print(response[0].get("data").get('management').get("name"))  # ФИО директора
        # print(response[0].get("data").get('management').get("post"))  # Наименование должности
        # print(response[0].get("data").get('state').get("status"))  # Статус организации (действ-ее/недействующее)
        # print(response[0].get("data").get("address").get("data").get("tax_office"))  # номер налоговой инспекции
        # print(response[0].get("data").get('okved'))  # ОКВЭД
        # print(response[0].get("data").get('licenses'))  # сведения о лицензиях
        # print(response[0].get("data").get('finance').get("tax_system"))  # система налогообложения
        # print(response[0].get("data").get('address').get("value"))  # адрес местонахождения
        # print(metro[0].get("name"))  # ближайшее метро
        # print(metro[0].get("distance"))  # расстояние от метро в км.

        text = response[0].get('data').get('name').get('full_with_opf')
        return text


class TextImageReader:

    @staticmethod
    def text_recognition(file_path: str, langs: list) -> str:
        """Метод для оптического распознавания текста(OCR) на изображении, переданного пользователем в чат бота.
        Возвращает распознанный текст в виде строкового, машинописного кода. В атрибут file_path передается строковое
        значение пути к файлу для распознавания. """

        reader = easyocr.Reader(langs)
        recognized_list = reader.readtext(file_path, detail=0, paragraph=True, text_threshold=0.5)
        recognized_string = '\n'.join(recognized_list)
        result = recognized_string.replace("<", "'").replace(">", "'").replace("/", "'")
        return result


class QRcodeMaker:
    @staticmethod
    def make_QR_code(content):
        qrcode = segno.make_qr(content, error='h')
        file_path = "./chat_images/qrcode_scale_25.png"
        qrcode.save(file_path, scale=25, light='lightgreen')
        result = open(file_path, mode="rb")
        return result

