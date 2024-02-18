import json
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
    def find_org_by_name(organization_data):
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

        full_with_opf = response[0].get('data').get('name').get('full_with_opf')
        short_with_opf = response[0].get('data').get('name').get('short_with_opf')


        result = []

        # result = (f"Полное наимен-ие: <b>{}</b>\n"
        #           f"Краткое наимен-ие: <b>{}</b>\n"
        #           f"ИНН: <b>{response[0].get('data').get('inn')}</b>\n"
        #           f"КПП: <b>{response[0].get('data').get('kpp')}</b>\n"
        #           f"ОГРН: <b>{response[0].get('data').get('ogrn')}</b>\n"
        #           f"Дата рег-ии: "
        #           f"<b>{datetime.datetime.fromtimestamp(((response[0].get('data').get('state').get('registration_date')) / 1000))}</b>\n"
        #           f"ФИО руков-ля(ЕИО): <b>{response[0].get('data').get('management').get('name')}</b>\n"
        #           f"Должность руков-ля: <b>{response[0].get('data').get('management').get('post')}</b>\n"
        #           f"Статус ЮЛ (действ./не действ.): <b>{response[0].get('data').get('state').get('status')}</b>\n"
        #           f"Код налог-ой инсп-ции: <b>{response[0].get('data').get('address').get('data').get('tax_office')}</b>\n"
        #           f"Основной ОКВЭД: <b>{response[0].get('data').get('okved')}</b>\n"
        #           f"Сведения о лицен-ях: <b>{response[0].get('data').get('licenses')}</b>\n"
        #           f"Система налогооб-ия: <b>{tax_check}</b>\n"
        #           f"Адрес госуд-ой рег-ии: <b>{response[0].get('data').get('address').get('value')}</b>\n"
        #           f"Ближайшее метро: <b>м. {metro_check}</b>\n"
        #           f"Расстояние до метро: <b>{metro_dist}</b>\n")

        return result


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

