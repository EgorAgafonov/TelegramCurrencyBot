import json
from typing import BinaryIO
import easyocr
import requests
import segno
from dadata import Dadata
from settings import *
import datetime


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
    def find_org_by_name(organization_data: str) -> list:
        """ Метод отправки запроса API сайта https://dadata.ru для предоставления сведений о юридическом лице
        из открытых источников (ЕГРЮЛ). Формирует из полученного массива данных список с необходимыми сведениями
        о ЮЛ."""

        dadata = Dadata(TOKEN_DADATA)
        response = dadata.suggest('party', organization_data)
        metro = response[0]["data"]["address"]["data"]['metro']
        tax_system = response[0]['data']['finance']
        if metro is None:
            metro_check = "нет"
            metro_dist = "нет"
        else:
            metro_check = metro[0]['name']
            metro_dist = metro[0]['distance']
        if tax_system is None:
            tax_check = "сведения отсутствуют"
        else:
            tax_check = tax_system['tax_system']

        full_with_opf = response[0]['data']['name']['full_with_opf']
        short_with_opf = response[0]['data']['name']['short_with_opf']
        inn = response[0]['data']['inn']
        kpp = response[0]['data']['kpp']
        ogrn = response[0]['data']['ogrn']
        reg_date = datetime.datetime.fromtimestamp(((response[0]['data']['state']['registration_date']) / 1000))
        heads_name = response[0]['data']['management']['name']
        heads_post = response[0]['data']['management']['post']
        company_status = response[0]['data']['state']['status']
        tax_office_num = response[0]['data']['address']['data']['tax_office']
        main_okved = response[0]['data']['okved']
        licenses = response[0]['data']['licenses']
        tax_system = tax_check
        reg_address = response[0]['data']['address']['value']
        nearest_metro = metro_check
        metro_distance = metro_dist

        result = [full_with_opf, short_with_opf, inn, kpp, ogrn, reg_date, heads_name, heads_post,
                  company_status, tax_office_num, main_okved, licenses, tax_system, reg_address, nearest_metro,
                  metro_distance]

        return result


class TextImageReader:

    @staticmethod
    def text_recognition(file_path: str, langs: list) -> str:
        """Метод для оптического распознавания текста(OCR) на изображении, переданного пользователем в чат бота.
        Возвращает распознанный текст в виде машинописных, текстовых символов. В аргумент file_path передается строковое
        значение пути к файлу для распознавания, аргумент langs принимает список с названием языков(а), символы
        которых(ого) содержатся на распознаваемом изображении."""

        reader = easyocr.Reader(langs)
        recognized_list = reader.readtext(file_path, detail=0, paragraph=True, text_threshold=0.5)
        recognized_string = '\n'.join(recognized_list)
        result = recognized_string.replace("<", "'").replace(">", "'").replace("/", "'") # из-за неверного распознавания
        # отдельных символов в тексте, при передаче строк в чат, API Telegram ошибочно распознает их как теги /.
        # При использовании аргумента parse_mode='html' это может привести к вызову исключений. По этой причине,
        # после распознавания из текстовой строки удаляется и меняется (.replace("/", "'") нежелательный знак "/".
        return result


class QRcodeMaker:
    @staticmethod
    def make_QR_code(content: str) -> BinaryIO:
        """Метод для генерации стандартного QR-кода из сообщения чата, содержащего html-ссылку или
        простой текст от пользователя. Возвращает байтовое представление сгенерированного qr-кода, хранящееся в
        буфере памяти."""

        qrcode = segno.make_qr(content, error='h')
        file_path = "qrcode_scale_25.png"
        qrcode.save(file_path, scale=25, light='lightgreen')
        result = open(file_path, mode="rb")
        return result

