from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')
TOKEN_DADATA = os.getenv("TOKEN_DADATA")
API_KEY = os.getenv('API_KEY')
RECOGN_IMAGE_PATH = os.getenv("INPUT_CHAT_IMAGE") + "input_chat_image.jpg"

keys = {
    'AED': 'ОАЭ дерхам',
    'AMD': 'армянский драм',
    'BGN': 'болгарский лев',
    'BYN': 'беларусский рубль',
    'CNY': 'китайский юань',
    'EUR': 'европейский евро',
    'JPY': 'японская иена',
    'KZT': 'казахстанский тенге',
    'RUB': 'российский рубль',
    'TRY': 'турецкая лира',
    'USD': 'доллар США',
    'UZS': 'узбекский сом',
}

curr_str = ("AED - ОАЭ дерхам\n"
            "AMD - армянский драм\n"
            "BGN - болгарский лев\n"
            "CNY - китайский юань\n"
            "EUR - европейский евро\n"
            "KZT - казахстанский тенге\n"
            "RUB - российский рубль\n"
            "TRY - турецкая лира\n"
            "USD - доллар США\n"
            "UZS - узбекский сом\n"
            "JPY - японская иена\n")

langs_str = ("ru - русский\n"
            "be - беларусский\n"
            "en - английский\n"
            "ch_sim - упрощенный китайский\n"
            "ch_tra - традиционный китайский\n"
            "de - немецкий\n"
            "fr - французский\n"
            "ja - японский\n"
            "uk - украинский\n"
            "tjk - таджикский\n"
            "uz - узбекский\n")