from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')
api_key = os.getenv('API_KEY')

unsorted_currncs = {
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
a = unsorted_currncs.items()
b = sorted(a)
print(dict(b))

currencies = {
  'AED': 'ОАЭ дерхам',
  'AMD': 'армянский драм',
  'BGN': 'болгарский лев',
  'BYN': 'беларусский рубль',
  'CNY': 'юань',
  'EUR': 'евро',
  'KZT': 'казахский тенге',
  'RUB': 'рубль',
  'TRY': 'турецкая лира',
  'USD': 'доллар',
  'UZS': 'узбекский сом'
}
