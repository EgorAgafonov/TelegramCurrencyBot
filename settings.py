from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')
api_key = os.getenv('API_KEY')

unsorted_keys = {
    "RUB": "рубль",
    "AED": "ОАЭ дерхам",
    "CNY": "юань",
    "EUR": "евро",
    "USD": "доллар",
    "BYN": "беларусский рубль",
    "AMD": "армянский драм",
    "BGN": "болгарский лев",
    "TRY": "турецкая лира",
    "KZT": "казахский тенге",
    "UZS": "узбекский сом"
}
a = unsorted_keys.items()
b = sorted(a)
# print(dict(b))

keys = {
    'AED': 'ОАЭ дерхам',
    'AMD': 'армянский драм',
    'BGN': 'болгарский лев',
    'BYN': 'беларусский рубль',
    'CNY': 'китайский юань',
    'EUR': 'европейский евро',
    'KZT': 'казахстанский тенге',
    'RUB': 'российский рубль',
    'TRY': 'турецкая лира',
    'USD': 'доллар США',
    'UZS': 'узбекский сом'
}

base = 'RUB'
quote = "UZS"

# if base in keys.keys():
#     quote_ticker = base
# else:
#     raise KeyError("Валюта не поддерживается")

try:
    keys[base]
except KeyError:
    raise Exception("Ошибка")

try:
    keys[quote]
except KeyError:
    raise Exception("Ошибка")
